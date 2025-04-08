#!/usr/bin/env python3
import logging
import re
import subprocess
import sys
from ast import literal_eval
from pathlib import Path
from subprocess import check_output, CalledProcessError, DEVNULL

#### Log manipulator
from multiprocessing import Process, Queue
from queue import Empty

from io import StringIO
from collections import defaultdict
import sys

try:
    from pynput import keyboard
except ImportError:
    keyboard = None

capture_regexes= {
    "d": r".*DEBUG.*",
    "i": r".*INFO.*",
    "w": r".*WARNING.*",
    "e": r".*ERROR.*",
}
capture_regex=r".*"
q = Queue()


def on_key_pressed(key):
    global q
    try:
        char = key.char
    except AttributeError:
        char=key
    if char in capture_regexes:
        q.put(capture_regexes[char])
        print(f": Capturing {capture_regexes[char]}")
    else:
        print(f": Key ignored")

class CaptureOutput:
    def __init__(self, queue):
        self.queue = queue

    def __enter__(self):

        self._stderr = sys.stderr
        self.capture_regex = capture_regex
        sys.stderr = StringIO()
        sys.stderr.fileno = lambda: 2
        sys.stderr.write = self.write_err

        return self

    def __exit__(self, *args):
        sys.stderr = self._stderr

    def write_err(self, err):
        try:
            self.capture_regex = self.queue.get_nowait()
            self._stderr.write(f": Capturing {self.capture_regex}\n")
        except Empty:
            pass
        if not re.match("^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} \d+ ", err) or re.match(self.capture_regex, err):
            self._stderr.write(err)

## /Log manipulator

_logger = logging.getLogger(__name__)

_logger.setLevel(logging.DEBUG)

EXTRA_LOCAL_ADDONS = [
    # Path.home().joinpath("src","odoo-ps", "psbe-internal-easier-life"),
]

IGNORE_ODOO_WARNING_MSGS = [
    "Found deprecated directive @t-esc=%r in template %r. Replace by @t-out",
    "'%s' module not installed. Code autoreload feature is disabled",
    "Attachment indexation of PDF documents is unavailable because the 'pdfminer' "
    "Python library cannot be found on the system. You may install it from "
    "https://pypi.org/project/pdfminer.six/ (e.g. `pip3 install pdfminer.six`)",
]

# exclusively for python waring module used in ORM
IGNORE_PY_WARNING_MSGS = [
    "Field {self} cannot be precomputed as it depends on non-precomputed field {field}",
]


def expand_arg(short_arg):
    short_arg = short_arg if short_arg.startswith("-") else f"-{short_arg}"
    return {
        "-h": "--help",
        "-s": "--save",
        "-c": "--config",
        "-i": "--init",
        "-u": "--update",
        "-P": "--import-partial",
        "-D": "--data-dir",
        "-p": "--http-port",
        "-d": "--database",
        "-r": "--db_user",
        "-w": "--db_password",
        "-l": "--language",
    }.get(short_arg, short_arg)


def get_dev_branch():
    return check_output(["git", "branch", "--show-current"],stderr=DEVNULL).decode("utf-8").strip()


def get_odoo_version(dev_branch):
    odoo_version = re.split("[_-]", dev_branch)[0]
    if not re.match(r"^\d+\.\d+$", odoo_version):
        res = re.search(r"\D\d+\.\d+\D", dev_branch)
        if res:
            odoo_version = res.group(0)
        if not odoo_version:
            for manifest in dev_dir.rglob("__manifest__.py"):
                ver = literal_eval(manifest.read_text()).get("version", "")
                if re.match(r"^\d+\.\d+\.\d+\.\d+", ver):
                    odoo_version = ".".join(ver.split(".")[:2])
                    break
            else:
                print("Odoo version could not be detected")
                exit(2)
    return odoo_version


def get_databases():
    return [
        dbl.split("|")[0].strip(""""' """)
        for dbl in _run_psql("-Alqt0F'|'").split("\0")
        if "|" in dbl and dbl.split("|")[2] != "postgres"
    ]


def get_connection_args():
    return []


def _run_psql(args, db=None):
    if isinstance(args, str):
        args = args.split()
    if db:
        args = ["-d", db] + args
    connection_args = get_connection_args()
    return check_output(["psql", *args]).decode("utf-8")


def query(db, sql):
    args = [
        "-A",  # no wrap
        "-t",  # no headers
        "-q",  # quiet
        "-0",  # null separated records
        "-F",
        "|",  # field separator |
        "-c",
        sql,
    ]
    return [rec.split("|") for rec in _run_psql(args, db).split("\0")]


def parse_argv(argv):
    # target = None
    # value = None
    # args = []
    # i = 0
    # while i < len(sys.argv):
    #     argv = sys.argv[i]
    #     if argv.startswith("--"):
    #         if "=" in arg:
    #             arg,value = argv.split("=")
    #             i+=1
    #         elif i+1<len(sys.argv) and not sys.argv[i+1].startswith("-"):
    #             arg, value = argv, sys.argv[i+1]
    #             i+=2
    #         else:
    #             arg, value = argv, None
    #     elif
    #     args.append((arg,value) if value else arg)
    args_dict = {}
    skip = False
    for arg1, arg2 in zip(argv, argv[1:] + [None], strict=False):
        if skip:
            skip = False
            continue
        if arg1.startswith("--"):
            if "=" in arg1:
                args_dict.update([arg1.split("=")])
            elif arg2 and not arg2.startswith("-"):
                args_dict[arg1.strip("=")] = arg2
                skip = True
            else:
                args_dict[arg1] = None
        elif arg1.startswith("-"):
            args_dict.update({expand_arg(arg): None for arg in arg1[1:]})

            if not arg2.startswith("-"):
                args_dict[expand_arg(arg1[-1])] = arg2
                skip = True
        else:
            args_dict[arg1] = None

    return args_dict


def patch_http(odoo):
    """
    Patch odoo.http.Stream.from_attachment to avoid file not found error
    :return:
    """

    original_from_attachment = odoo.http.Stream.from_attachment

    def from_attachment(attachment):
        try:
            return original_from_attachment(attachment)
        except FileNotFoundError:
            self = odoo.http.Stream(
                mimetype=attachment.mimetype,
                download_name=attachment.name,
                etag=attachment.checksum,
                public=attachment.public,
            )
            odoo.http._logger.debug("File not found for: %s", attachment.name)
            self.type = "data"
            self.data = b""
            self.size = 0

            return self

    odoo.http.from_attachment = from_attachment


def apply_defaults(args_dict, defaults):
    """
    This function applies default values to the arguments dictionary.
    If the argument is not present
    in the arguments dictionary, the default value is used.

    If an argument is present in both the arguments dictionary and the defaults,
    if the default value is a list, it will be merged with the value from the
    arguments dictionary, otherwise 

    Parameters:
    args_dict (dict): A dictionary containing command-line arguments.
    defaults (dict): A dictionary containing default values for command-line arguments.

    Returns:
    dict: The updated dictionary with default values applied.
    """
    for arg_def, def_value in defaults.items():
        if isinstance(def_value, list):
            arg_set = set(tuple(def_value)) | set(tuple(args_dict.get(arg_def, "").split(",")))
            args_dict[arg_def] = ",".join(map(str, (a for a in arg_set if a)))
        else:
            args_dict.setdefault(arg_def, def_value)
    return args_dict


def get_args(args_dict):
    args = []
    for a, v in args_dict.items():
        args.append(a)
        if v is not None:
            args.append(str(v))
    return args


def get_defaults(addons_path, dev_branch, odoo_version, test_mode=False):
    # always use long names
    defaults = {
        "--addons-path": addons_path,
        "--log-level": "debug",
        "--limit-time-real-cron": 900,
        "--limit-time-real": 150,
        "--limit-time-cpu": 150,
        "--workers": 0,
        "--dev": "all",
        "--max-cron-threads": 0,
        "--database": dev_branch,
        "--http-port": int("".join(filter(str.isdigit, odoo_version))[:3] or 80) * 100 + 69,
    }
    if test_mode:
        _logger.info("Applying test mode params")
        defaults["--stop-after-init"] = None
        defaults["--http-port"] += 10
        defaults["--workers"] = 0
        defaults["--max-cron-threads"] = 0
        defaults["--no-http"] = None
        defaults["--log-level"] = "test"
        defaults["--log-handler"] = "odoo.tools.convert:DEBUG"

    return defaults


def get_dev_dir():
    # we assume this is run in the target odoo folder
    dev_dir = Path.cwd()
    if Path(__file__).resolve().parent == dev_dir:
        raise Exception("Run this script from the target odoo folder")
    return dev_dir


def get_addons_path(dev_dir, src_path):
    custom_addons_folders = {
        manifest.parent.parent for manifest in dev_dir.rglob("__manifest__.py")
    }
    addons_path = list(
        map(
            str,
            [
                src_path.joinpath("odoo", "odoo", "addons"),
                src_path.joinpath("odoo", "addons"),
                src_path.joinpath("enterprise"),
                src_path.joinpath("design-themes"),
                *EXTRA_LOCAL_ADDONS,
                *custom_addons_folders,
            ],
        )
    )
    return addons_path


def patch_logging_warning():
    """
    Patch logging to ignore warning messages
    """
    logging_warning = logging.Logger.warning

    def warning(self, msg, *args, **kwargs):
        if (self.name == "py.warnings" and any(m in args[0] for m in IGNORE_PY_WARNING_MSGS)) or (
            self.name != "py.warnings" and msg in IGNORE_ODOO_WARNING_MSGS
        ):
            logging.debug(msg, *args, **kwargs)
        else:
            # print(f"===>>> msg: {msg} , args: {args}, kwargs: {kwargs}")
            logging_warning(self, msg, *args, **kwargs)

    logging.Logger.warning = warning


def create_db(db, databases, repo_name):
    db_template = None
    if repo_name in databases:
        db_template = repo_name
    elif (name := "".join(repo_name.split("-")[1:])) and name in databases:
        db_template = name
    command = ["createdb"]
    if db_template:
        command.extend(["-T", db_template])
    _logger.info(f"Creating database {db}{f' from {db_template}' if db_template else ''}.")
    subprocess.run([*command, db])


def main():
    dev_dir = get_dev_dir()

    try:
        dev_branch = get_dev_branch()
    except CalledProcessError as e:
        _logger.error("Current directory is not a git repository, please run this script from the target odoo folder")
        exit(e.returncode)

    odoo_version = get_odoo_version(dev_branch)
    src_path = Path.home().joinpath("odev", "worktrees", odoo_version)
    # find submodules
    addons_path = get_addons_path(dev_dir, src_path)

    args_dict = parse_argv(sys.argv)
    runner_args = defaultdict(lambda : None)
    for arg in tuple(args_dict.keys()):
        if arg.startswith("--runner-no-"):
            runner_args[arg.split("--runner-no-")[1]] = not args_dict.pop(arg)
        elif arg.startswith("--runner-"):
            runner_args[arg.split("--runner-")[1]] = args_dict.pop(arg) or True

    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        # in debug mode
        _logger.debug("In debug mode, force disabled keyboard shortcuts")
        runner_args["keyboard"] = False

    if runner_args["log-level"]:
        global capture_regex
        capture_regex = capture_regexes.get(runner_args["log-level"],capture_regex)
    defaults = get_defaults(
        addons_path,
        dev_branch,
        odoo_version,
        test_mode=any(arg.startswith("--test") for arg in args_dict),
    )
    databases = get_databases()

    _logger.debug("Databases: %s", databases)

    _logger.debug("Parsed args: %s", get_args(args_dict))

    apply_defaults(args_dict, defaults)

    if tf := args_dict.get("--test-file"):
        module = Path(tf).parent.parent.name
        module_state = query(
            args_dict["--database"],
            f"SELECT state FROM ir_module_module WHERE name = '{module}'",
        )
        if not module_state[0][0]:
            _logger.error(f"Module {module} not found for running test file {tf} on db {args_dict['--database']}")
            exit(3)
        if module_state[0][0] != "installed":
            init_modules = args_dict.get("--init")
            init_list = init_modules and init_modules.split(",") or []
            if module not in init_list:
                init_list.append(module)
            defaults["--init"] = defaults.get("--init", []) + init_list
            apply_defaults(args_dict, defaults)

    if dev_branch not in databases:
        create_db(
            dev_branch,
            databases,
            next(dev_dir.rglob("__manifest__.py")).parent.parent.name,
        )

        args_dict.setdefault(
            "--init", "base"
        )  # if any module is going to be installed, we don't need base

    args = get_args(args_dict)
    _logger.debug("Final args: %s", args)

    sys.argv = args

    patch_logging_warning()
    sys.path.append(f"{src_path}/odoo")
    import odoo
    # Option 3: Shell (not really an option, keep this code uncommented)
    if sys.argv[1] == "shell" or not runner_args["keyboard"]:
        exit(odoo.cli.main())


    if "15.0" < odoo_version < "18.0": patch_http(odoo)

# Option 1:
# Just run the damn thing
#     exit(odoo.cli.main())

# Option 2: Profile all!
#     try:
#         with odoo.tools.profiler.Profiler(db=args_dict.get("--database")) as p:
#             odoo.cli.main()
#     finally:
#         fname = p.format_path(f"/tmp/odoo_profile_{{desc}}_{{time}}.json")
#         print(f"Saving profile to {fname}")
#         with open(fname, "w") as f:
#             f.write(p.json())
#         exit()


## With keyboard hook

# Option 4: Logging manipulator global keys , bad idea
#     if not keyboard:
#         print("pynput module not found, skipping keyboard hook")
#     else:
#         listener=keyboard.Listener(on_press=on_key_pressed)
#         listener.start()


    def worker():
        with CaptureOutput(q):
            odoo.cli.main()

    Process(target=worker,).start()

# Option 5: Keyboard hook within tty, only while having focus
    import termios
    import tty
    import selectors
    # store terminal state
    old_state = termios.tcgetattr(sys.stdin)
    # disable stdin wait for return key before reading
    tty.setcbreak(sys.stdin.fileno())
    # Add an IO listener
    selector = selectors.DefaultSelector()
    # Listen on stdin, without giving any callback
    selector.register(sys.stdin, selectors.EVENT_READ)
    try:
        while True:
            for key, events in selector.select():
                if key.fileobj is sys.stdin:
                    c = key.fileobj.read(1)
                    on_key_pressed(c[0])
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_state)
## /Logging manipulator

if __name__ == "__main__":
    main()

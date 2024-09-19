# !/usr/bin/env python3
import argparse
import ast
import inspect
import json
import logging
import os
import shutil
import sys

# from inspect import getmembers, isclass, ismodule, isfunction, signature
from pathlib import Path
from unittest import TestCase

TEST_CASE_METHODS = [
    method.name
    for method in ast.parse(inspect.getsource(TestCase)).body[0].body
    if isinstance(method, ast.FunctionDef)
]


# data = {
#     "BaseCommon": {
#         "inherits": [],
#         "attributes": {
#             "env": {
#                 "type": "Environment",
#                 "comment": "With disabled mail tracking",
#             },
#             "partner": {
#                 "type": "recordset",
#                 "relation": "res.partner",
#                 "comment": "a new partner",
#             },
#             "currency": {
#                 "type": "recordset",
#                 "relation": "res.currency",
#                 "comment": "company_id.currency_id",
#             },
#         },
#     },
#     "UomCommon": {
#         "inherits": [],
#         "attributes": {
#             "uom_gram": {"type": "recordset", "relation": "uom.uom"},
#             "uom_kgm": {"type": "recordset", "relation": "uom.uom"},
#             "uom_ton": {"type": "recordset", "relation": "uom.uom"},
#             "uom_unit": {"type": "recordset", "relation": "uom.uom"},
#             "uom_dozen": {"type": "recordset", "relation": "uom.uom"},
#             "group_uom": {
#                 "type": "recordset",
#                 "relation": "res.groups",
#                 "comment": "Security group of uom access",
#             },
#             "_enable_uom": {
#                 "type": "method",
#                 "comment": "Enable uom group for current env's user",
#             },
#             "_disable_uom": {
#                 "type": "method",
#                 "comment": "Disable uom group for current env's user",
#             },
#         },
#     },
#     "ProductCommon": {
#         "inherits": ["BaseCommon", "UomCommon"],
#         "does": "Set env's company currency to usd, disable all pricelists.",
#         "attributes": {
#             "currency": {
#                 "type": "recordset",
#                 "relation": "res.currency",
#                 "value": "USD",
#                 "comment": "overrides BaseCommon.currency, also sets it as company currency",
#             },
#             "product_category": {
#                 "type": "recordset",
#                 "relation": "product.category",
#                 "comment": "a new category",
#             },
#             "product": {
#                 "type": "recordset",
#                 "relation": "product.product",
#                 "comment": "a new consumable product, in cls.product_category",
#             },
#             "service_product": {
#                 "type": "recordset",
#                 "relation": "product.product",
#                 "comment": "a new service product, in cls.product_category",
#             },
#             "consumable_product": {
#                 "type": "recordset",
#                 "relation": "product.product",
#                 "comment": "pointer to cls.product",
#             },
#             "pricelist": {
#                 "type": "recordset",
#                 "relation": "product.pricelist",
#                 "comment": "a new pricelist",
#             },
#             "_archive_other_pricelists": {
#                 "type": "method",
#                 "comment": "Archive other pricelists, stupid method, the code should be in setupCLass instead",
#             },
#         },
#     },
#     "ProductAttributesCommon": {
#         "inherits": ["ProductCommon"],
#         "attributes": {
#             "size_attribute": {
#                 "type": "recordset",
#                 "relation": "product.attribute",
#                 "comment": "A new attribute",
#             },
#             "size_attribute_s": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "size_attribute_m": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "size_attribute_l": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "color_attribute": {
#                 "type": "recordset",
#                 "relation": "product.attribute",
#                 "comment": "A new attribute",
#             },
#             "color_attribute_red": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "color_attribute_blue": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "color_attribute_green": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "no_variant_attribute": {
#                 "type": "recordset",
#                 "relation": "product.attribute",
#                 "comment": "A new attribute with no create",
#             },
#             "no_variant_attribute_extra": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "no_variant_attribute_second": {
#                 "type": "recordset",
#                 "relation": "product.attribute.value",
#             },
#             "dynamic_attribute": {
#                 "type": "recordset",
#                 "relation": "product.attribute",
#                 "comment": "A new attribute with dynamic create, values dyn1 and dyn2",
#             },
#         },
#     },
#     "ProductVariantsCommon": {
#         "inherits": ["ProductAttributesCommon"],
#         "attributes": {
#             "product_template_sofa": {
#                 "type": "recordset",
#                 "relation": "product.template",
#                 "comment": "A new product template, with three cls.color_attribute values.",
#             },
#             "cls.product_template_shirt": {
#                 "type": "recordset",
#                 "relation": "product.template",
#                 "comment": "A new product template, with on cls.size_attribute value",
#             },
#         },
#     },
#     "TestProductCommon": {
#         "inherits": ["ProductVariantsCommon"],
#         "attributes": {
#             "uom_dunit": {
#                 "type": "recordset",
#                 "relation": "uom.uom",
#                 "comment": "Deci Unit, 10 x unit",
#             },
#             "product_1": {
#                 "type": "recordset",
#                 "relation": "product.product",
#                 "value": "[PROD-1] Courage",
#                 "comment": "a new consumable product, no categ, uom_dunit",
#             },
#             "product_2": {
#                 "type": "recordset",
#                 "relation": "product.product",
#                 "value": "Wood",
#                 "comment": "a new consumable product, no categ, no nothing",
#             },
#         },
#         "prod_att_1": {
#             "type": "recordset",
#             "relation": "product.attribute",
#             "value": "cls.color_attribute",
#         },
#         "prod_attr1_v1": {
#             "type": "recordset",
#             "relation": "product.attribute.value",
#             "value": "cls.color_attribute_red",
#         },
#         "prod_attr1_v2": {
#             "type": "recordset",
#             "relation": "product.attribute.value",
#             "value": "cls.color_attribute_blue",
#         },
#         "prod_attr1_v3": {
#             "type": "recordset",
#             "relation": "product.attribute.value",
#             "value": "cls.color_attribute_green",
#         },
#         "product_7_template": {
#             "type": "recordset",
#             "relation": "product.template",
#             "value": "cls.product_template_sofa",
#             "comment": "Pointer to cls.product_template_sofa",
#         },
#         "product_7_attr1_v1": {
#             "type": "recordset",
#             "relation": "product.template.attribute.value",
#         },
#         "product_7_attr1_v2": {
#             "type": "recordset",
#             "relation": "product.template.attribute.value",
#         },
#         "product_7_attr1_v3": {
#             "type": "recordset",
#             "relation": "product.template.attribute.value",
#         },
#         "product_7_1": {
#             "type": "recordset",
#             "relation": "product.product",
#             "comment": "Variant of cls.product_7_attr1_v1",
#         },
#         "product_7_2": {
#             "type": "recordset",
#             "relation": "product.product",
#             "comment": "Variant of cls.product_7_attr1_v2",
#         },
#         "product_7_3": {
#             "type": "recordset",
#             "relation": "product.product",
#             "comment": "Variant of cls.product_7_attr1_v3",
#         },
#     },
#     "common2.TestStockCommon": {
#         "inherits": ["TestProductCommon"],
#         "attributes": {
#             "user_stock_user": {
#                 "type": "recordset",
#                 "relation": "res.users",
#                 "value": "pauline",
#                 "comment": "New user with 'stock.group_stock_user' group",
#             },
#             "user_stock_manager": {
#                 "type": "recordset",
#                 "relation": "res.users",
#                 "value": "julie",
#                 "comment": "New user with 'stock.group_stock_manager' group",
#             },
#             "warehouse_1": {
#                 "type": "recordset",
#                 "relation": "stock.warehouse",
#                 "comment": "New warehouse with one step in and out",
#                 "value": "BWH",
#             },
#             "location_1": {
#                 "type": "recordset",
#                 "relation": "stock.location",
#                 "comment": "Internal stock location of cls.warehouse_1",
#                 "value": "cls.warehouse_1.lot_stock_id.id",
#             },
#             "partner_1": {
#                 "type": "recordset",
#                 "relation": "res.partner",
#                 "comment": "new partner",
#             },
#             "product_3": {
#                 "type": "recordset",
#                 "relation": "product.product",
#                 "comment": "New consu product, in dozens",
#                 "value": "Stone",
#             },
#             "existing_inventories": {
#                 "type": "recordset",
#                 "relation": "stock.quant",
#                 "comment": "Stock quants with inventory qty",
#             },
#             "existing_quants": {
#                 "type": "recordset",
#                 "relation": "stock.quant",
#                 "comment": "All existing quands in the universe",
#             },
#             "_create_move": {
#                 "type": "method",
#                 "comment": "Create a stock move as stock manager",
#             },
#         },
#     },
# }

def save_data(data, path, backup=True):
    if isinstance(path, Path):
        # we are using default value, ensure folder exists
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        path = Path(path)
    if backup and path.is_file():
        shutil.copyfile(path, path.with_suffix(".json.bak"))
    with open(path, "w") as data_file:
        json.dump(data, data_file)


def get_available_attributes(test_class, data):
    if test_class not in data:
        return {}
    inherits = list(data[test_class].get("inherits", []))
    attributes = dict(**data[test_class].get("attributes", {}))
    while inherits:
        parent = data.get(inherits.pop())
        if not parent:
            continue
        if parent.get("inherits"):
            inherits.extend(parent["inherits"])
        for attrib, value_dict in parent.get("attributes", {}).items():
            attributes.setdefault(attrib, dict(**value_dict))

    return attributes


# def load_module_tests(addons_path):
#     addons_path = Path(addons_path)
#     for test_init in addons_path.rglob("tests/__init__.py"):
#         module_folder = str(test_init.parent.parent)
#         sys.path.insert(0, module_folder)
#         tests = importlib.import_module("tests")
#         test_files = getmembers(tests, lambda x: ismodule(x))
#         for fname, test_file in test_files:
#             test_classes = getmembers(
#                 test_file, lambda x: isclass(x) and issubclass(x, TestCase)
#             )
#             for cls_name, cls in test_classes:
#                 extracted = {}
#                 parent_members = {}
#                 for base in cls.__bases__:
#                     parent_members.update(dict(getmembers(base)))
#                 for name, attr in getmembers(cls):
#                     if name.startswith("test_"):
#                         break
#                     elif attr == parent_members.get(name):
#                         continue
#                     elif name in ["setUpClass", "setUp"]:
#                         extracted[name] = getmembers(cls, lambda x: x)
#                     elif isfunction(attr) and not name.startswith("__"):
#                         extracted[name] = {"type": "method", "comment": attr.__doc__ or "", "params": str(signature(attr))}
#                 else:
#                     # only add if no test found in this class
#                     data[cls_name] = extracted
#
#         sys.path.pop(0)

def load_module_tests(addons_path):
    """
    Load the tests files from the addons folder and analyse them
    :param addons_path: str
    :return: dict
    """
    res = {}
    addons_path = Path(addons_path)
    for test_init in addons_path.rglob("tests/__init__.py"):
        test_folder = test_init.parent
        logging.debug(f"Loading tests of {test_folder.parent.name}")
        # We could exclude test_* but, there are some test_common file, stupid but true...
        for test_file in test_folder.glob("[!_]*.py"):
            test_file_code = ast.parse(test_file.read_text())
            for cls in filter(
                    lambda x: isinstance(x, ast.ClassDef), test_file_code.body
            ):
                inherits = [
                    base.id if hasattr(base, "id") else base.attr for base in cls.bases
                ]
                extract = {}
                for method in filter(
                        lambda x: isinstance(x, ast.FunctionDef), cls.body
                ):
                    if method.name.startswith("test_"):
                        logging.debug(f"Skipping test {test_file}:{cls}, found a test case.")
                        break
                    elif method.name in ["setUpClass", "setUp"]:
                        body = method.body
                        for node in body:
                            if isinstance(node, ast.Assign):
                                for target in node.targets:
                                    if (
                                            isinstance(target, ast.Attribute)
                                            and isinstance(target.value, ast.Name)
                                            and target.value.id in ["self", "cls"]
                                    ):
                                        extract[node.targets[0].attr] = {
                                            "type": "?",
                                            "comment": "",
                                        }

                    elif method.name in TEST_CASE_METHODS or method.name.startswith(
                            "__"
                    ):
                        continue
                    else:
                        args = [arg.arg for arg in method.args.posonlyargs]
                        args += [arg.arg for arg in method.args.args]
                        args = args[1:]  # except self
                        kwargs = [arg.arg for arg in method.args.kwonlyargs]
                        args_text = ""
                        default_offset = len(args) - len(method.args.defaults)
                        if args:
                            args_text = ", ".join(args[:default_offset])
                            for i, default in enumerate(method.args.defaults):
                                args_text += f", {args[i + default_offset]}={getattr(default, 'value', getattr(default, 'id', 'N/A'))!r}"
                        if kwargs:
                            args_text += ", " + ", ".join(
                                "=".join(
                                    *zip(
                                        kwargs,
                                        map(
                                            lambda x: str(x.value),
                                            method.args.kw_defaults,
                                        ),
                                    )
                                )
                            )

                        if (
                                isinstance(method.body[0], ast.Expr)
                                and isinstance(method.body[0].value, ast.Constant)
                                and isinstance(method.body[0].value.s, str)
                        ):
                            docstring = method.body[0].value.s

                        extract[method.name] = {
                            "type": "method",
                            "comment": docstring.strip() or "",
                        }
                        if args:
                            extract[method.name]["params"] = f"({args_text})"
                else:
                    # only add if no test found in this class, so it is a common class
                    logging.debug(
                        f"Adding /{test_folder.parent.name}.{test_file.with_suffix('').name}:{cls.name} to common tests")

                    key = cls.name
                    if key in res:
                        key = f"{test_file.with_suffix('').name}.{key}"
                        if key in res:
                            key = f"{test_folder.parent.name}.{key}"

                    res[key] = {"inherit": inherits, "attributes": extract}
    return res


def main():
    # todo: make a class for data
    args = argparse.ArgumentParser(
        description="""
The hitchhiker's guide to common tests.
=======================================

Finds what common test classes attributes add.
""",
    )
    args.add_argument("common_test_class_name", nargs="?")
    # todo: make it required
    args.add_argument(
        "-s",
        "--scan",
        help="Scan for common test classes, in the comma separated paths given.",
        # default="/home/odoo/odev/worktrees/17.0/odoo/addons",
    )
    args.add_argument(
        "--data-file",
        "--data",
        "-d",
        help="Path to datafile, default: ~/.config/common_tests.json",
        default=Path.joinpath(Path.home(), ".config", "common_tests.json"),
    )
    args.add_argument("--odoo-version", "-o", default="17.0")
    args.add_argument("--verbose", "-v", action="store_true")

    args = args.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # if data file not exists, create one
    if not os.path.isfile(args.data_file):
        save_data({args.odoo_version: {}}, args.data_file)

    with open(args.data_file, "r") as data_file:
        data = json.load(data_file)

    version_data = data.setdefault(args.odoo_version, {})
    if args.scan:
        for path in args.scan.split(","):
            scanned_data = load_module_tests(path)
            for k, v in scanned_data.items():
                if k not in version_data:
                    version_data[k] = v
                else:
                    version_data[k]["inherit"] = v["inherit"]
                    for attr, value in v["attributes"].items():
                        if attr not in version_data[k]["attributes"]:
                            version_data[k]["attributes"][attr] = value
                        else:
                            for key, val in value.items():
                                version_data[k]["attributes"][attr].setdefault(key, val)
            save_data(data, args.data_file)

    query = args.common_test_class_name
    common_classes = []
    if query in version_data:
        common_classes.append(query)
    else:
        if query:
            print(
                f"Unknown common test class {query}, trying to find it heuristically..."
            )
        else:
            query = ""

        for cls in version_data:
            if query in cls:
                print(f"Found common test class {cls}")
                common_classes.append(cls)

    if len(common_classes) == 0:
        print(f"Could not find common test class {query}")
        sys.exit(1)
    for common_class in common_classes:
        if len(common_classes) > 1:
            print(f"======= {common_class} ========")
        print(json.dumps(get_available_attributes(common_class, version_data), indent=2))




if __name__ == "__main__":
    main()

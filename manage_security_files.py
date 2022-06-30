#!/usr/bin/env python3

import os
import sys
import re
import csv
import logging


def display_menu(title, items):
    print('=' * len(title))
    print('\n'.join(items))
    print('-' * (max(map(len, items)) if items else 0))


def main(args):
    if len(args) > 1:
        raise Exception("Usage: %s [-d|-v] [path_to_module]" % sys.argv[0])
    module_path = args and args[0] or input('Path to module: ')
    os.chdir(module_path)  # raises exception if not found
    module = os.getcwd().split("/")[-1]
    logging.info(f'Processing module {module}')
    models = []
    for folder in os.listdir('.'): 
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file[-3:] == '.py':
                    with open(os.path.join(folder,file)) as py_file:
                        models += re.findall(r"(?:\W_name\s*=\s*['\"])(.*)(?:['\"])", py_file.read())
    logging.debug(f'Found models: {models}')
    os.makedirs('security', mode=0o755, exist_ok=True)
    os.chdir('security')

    acl_header = ["id", "name", "model_id:id", "group_id:id",
                  "perm_read", "perm_write", "perm_create", "perm_unlink"]

    try:
        with open('ir.model.access.csv') as acl_file:
            csv_reader = csv.DictReader(acl_file, fieldnames=acl_header)
            acl_rows = [dict(row) for row in csv_reader][1:]
    except  FileNotFoundError:
        open('ir.model.access.csv', 'w').close()
        acl_rows = []
    logging.debug('found ACLs:\n' + '\n'.join(map(str, acl_rows)))

    while True:
        display_menu("Models Discovered:", [f"[{i + 1}] {model}" for i, model in enumerate(models)])
        try:
            model_no = int(input('Model No, any non-digit to quit:[Quit] '))
        except ValueError:
            break
        model = models[model_no - 1]
        model_id = f"model_{model.replace('.', '_')}"
        logging.info(f'Selected {model} with id {model_id}')

        choice = None
        while choice != 'B':
            model_acls = [acl for acl in filter(lambda x: x['model_id:id'] == model_id, acl_rows)]
            menu_items = [f"[{i + 1}] {row['model_id:id'][6:]} for {row['group_id:id']} as "
                          f"{row['perm_create'] == '1' and 'C' or ''}"
                          f"{row['perm_read'] == '1' and 'R' or ''}"
                          f"{row['perm_write'] == '1' and 'U' or ''}"
                          f"{row['perm_unlink'] == '1' and 'D' or ''}" for i, row in enumerate(model_acls)]

            if menu_items:
                display_menu("Current rights:", menu_items)
                choice = input("(A)dd, (R)emove, (E)dit, (B)ack?[B] ").upper() or "B"
            else:
                print('No current rights for this model')
                choice = 'A'

            if choice == 'A':
                current_groups = set(f"{group}" for group in map(lambda x: x['group_id:id'], acl_rows))
                current_groups = sorted(list(current_groups))
                display_menu("Security Groups", [f"[{i + 1}] {group}" for i, group in enumerate(current_groups)])
                res = input("Select existing group or enter group's xml_id: ")
                try:
                    group_id = current_groups[int(res) - 1]
                except ValueError:
                    group_id = res

                if "." in group_id:
                    group_stem = group_id.split(".")[1][6:]
                else:
                    group_stem = group_id[6:]
                    group_id = ".".join([module, group_id])

                rights = input("Access rights (C)reate, (R)ead, (U)pdate, (D)elete?[CRU] ").upper() or "CRU"
                row = {
                    'id': f"access_{model.replace('.', '_')}_{group_stem}",
                    'name': f"{model}.{group_stem.replace('_', '.')}",
                    "model_id:id": model_id,
                    "group_id:id": group_id,
                    "perm_read": '1' if 'R' in rights else '0',
                    "perm_write": '1' if 'U' in rights else '0',
                    "perm_create": '1' if 'C' in rights else '0',
                    "perm_unlink": '1' if 'D' in rights else '0'
                }
                if row['id'] in map(lambda r: r['id'], acl_rows):
                    logging.warning(
                        'Access rights of this group in current model is already defined, please edit them instead.')
                else:
                    logging.info(f'Adding {row}')
                    acl_rows.append(row)

            elif choice == 'E':
                row_no = int(input("Which line?[1] ") or "1") - 1
                rights = input("New access rights (C)reate, (R)ead, (U)pdate, (D)elete?[CRU] ").upper() or "CRU"
                model_acls[row_no]["perm_read"] = '1' if 'R' in rights else '0'
                model_acls[row_no]["perm_write"] = '1' if 'U' in rights else '0'
                model_acls[row_no]["perm_create"] = '1' if 'C' in rights else '0'
                model_acls[row_no]["perm_unlink"] = '1' if 'D' in rights else '0'
            elif choice == 'R':
                try:
                    row_no = int(input("Which line?[None] ")) - 1
                    acl_rows.remove(model_acls[row_no])
                except ValueError:
                    pass

    confirm = ' '
    while confirm[0] not in 'YN':
        confirm = input('Save Changes (Y)es,(N)o?[N] ').upper() or "N"
    if confirm == 'Y':
        logging.info('Writing to file')
        with open('ir.model.access.csv', 'w') as acl_file:
            csv_writer = csv.DictWriter(acl_file, fieldnames=acl_header)
            csv_writer.writeheader()
            csv_writer.writerows(acl_rows)
    else:
        logging.info('Quit, discarding changes')


if __name__ == '__main__':
    args = sys.argv[1:]

    # logging only takes the first executed log level into account, so we don't need `else`
    if '-d' in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove('-d')

    if '-v' in args:
        logging.basicConfig(level=logging.INFO)
        args.remove('-v')

    logging.basicConfig(level=logging.WARNING)

    main(args)

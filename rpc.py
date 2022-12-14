#!/usr/bin/env python3
"""
optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
"""
import argparse
import base64
import tarfile
import tempfile
import sys
import xmlrpc.client
from pprint import pprint

parser = argparse.ArgumentParser(
    prog='odoo_rpc',
    description='Runs odoo rpc command',
    epilog='''
    Example: %s -p secret mydb res.users search_read "[]" '{"domain":[("login", "ilike", "admin")],"fields":["date_create"]}'
    ''' % __file__
)
parser.add_argument("database")
parser.add_argument("model")
parser.add_argument("method")
parser.add_argument("args")
parser.add_argument("kwargs")
parser.add_argument('-l', '--url', default="http://127.0.0.1:8069/", help='server url, defaults to local host port 8069')
parser.add_argument('-u', '--username', default="admin", help='defaults to admin')
parser.add_argument('-p', '--password', default="admin", help='defaults to admin')
args = parser.parse_args()
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(args.url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(args.url))
db = args.database # or args.url.split('//')[1].split('.')[0]
uid = common.authenticate(db, args.username, args.password, {})
data = models.execute_kw(
     db, uid, args.password, args.model, args.method,eval(args.args), eval(args.kwargs)
)
pprint(data)

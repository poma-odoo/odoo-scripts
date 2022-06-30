#!/usr/bin/env bash
# find . -name *.js
grep -lRF '/** @odoo-module **/' . --include *.js | python3 ~/src/kenedev/tools/convert_es6_modules/js_transpiler.py
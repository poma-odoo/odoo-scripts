#!/usr/bin/env bash
export ODOO_ROOT=$(
    ( test -d "$HOME/git/odoo/odoo/.git" && echo "$HOME/git/odoo" ) ||\
    ( test -d "$HOME/src/odoo/.git" && echo "$HOME/src" ) ||\
    ( find "$HOME" -name .git -type d -path '/*/odoo/.git' 2>/dev/null | head -n1 | sed 's#/odoo/.git$##' )
    )
if [ -z $ODOO_ROOT ]; then
  echo "Odoo root not found in $HOME" 1>&2
  exit 1
fi
echo "$ODOO_ROOT"

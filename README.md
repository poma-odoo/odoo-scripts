# odoo-scripts

## The *o* script
syntax: `o help|install|update|uninstall|clone|o-branch|o-branch-com|o-git|o-module-path|o-get-args|o-prune|o-update-mains|o-rebase-all|o-sync|o-sync-to-ent|o-sync-to-com|o-bin|o-shell|o-test|o-backup|o-restore|o-trans-export|o-trans-update`

clone: clones the repositories and setup git
install: adds o-commands to shell on next start
uninstall: removes o-commands from shell on next start
update: updates odoo main branches (starred ones in the runbot)
o-branch : Prints current active branch if synced
o-branch-com : prints current community branch name
o-git git-command : runs a git command on enterprise and odoo synchronously, and upgrade only if it is on the same branch
o-module-path module_name : prints absolute path of the module 
o-get-args : tries to find odoo config in order from odoo root or home folder otherwise it generates a minimal commandline options for running odoo
o-prune : prunes local branches that are not in the remote
o-update-mains : Pull all main branches branches (master and stable)
o-rebase-all : rebase active branches to their latest version of main branches, for 15.0-z-y, it pulls 15.0 an rebases active branch to it
o-sync repo1 repo2 : create or checkout same branch as current repo1 branch in the repo2 worktree
o-sync-to-ent : create or checkout same branch as current enterprise branch in the community worktree passing -u also sets the upgrade repo
o-sync-to-com : create or checkout same branch as current community branch in the enterprise worktree passing -u also sets the upgrade repo
o-bin : runs odoo
o-shell : runs shell
o-test test-tags : runs tests and exit
o-backup : copies current database to a temporary dbname-backup
o-restore : erase current db and retore backup taken with o-backup
o-trans-export [-i] module [lang]: installs the module and exports pot, or exports po file for module and selected language. -i means inplace, it overwrite the existing file in module 
o-trans-update module: exports a new pot file and upgrade all po files to match it. Overwrites the original files!
o-se -> shortcut for o-sync-ent
o-sc -> shortcut for o-sync-com

all o-* commands can be invoked without 'o-', e.g './o branch' is equal to './o o-branch'

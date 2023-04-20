# odoo-scripts

## The *o* script

### syntax: 

`o o-help|install|update|uninstall|clone|o-branch|o-branch-com|o-git|o-module-path|o-venv|o-get-args|o-prune|o-update-mains|o-rebase-all|o-sync|o-sync-to-ent|o-sync-to-com|o-bin|o-dev|o-shell|o-init|o-upgrade|o-test|o-psql|o-drop|o-backup|o-restore|o-trans-export|o-trans-update`

- **clone**: clones the repositories and setup git
- **install**: adds o-commands to shell on next start
- **uninstall**: removes o-commands from shell on next start
- **update**: updates odoo main branches (starred ones in the runbot)
- **o-branch** : Prints current active branch if synced
- **o-branch-com** : prints current community branch name
- **o-git** git-command : runs a git command on enterprise and odoo synchronously, and upgrade only if it is on the same branch
- **o-module-path** module_name : prints absolute path of the module 
- **o-venv** : enables venv for the branch
- **o-get-args** : tries to find odoo config in order from odoo root or home folder otherwise it generates a minimal commandline options for running odoo
- **o-prune** : prunes local branches that are not in the remote
- **o-update-mains** : Pull all main branches branches (master and stable)
- **o-rebase-all** [branch] : rebase provided branch to their latest version of main branches on all repos, for 15.0-z-y, it pulls 15.0 an rebases the branch onto it. Uses current branch if none given 
- **o-sync** repo1 repo2 : create or checkout same branch as current repo1 branch in the repo2 worktree
- **o-sync-to-ent** : create or checkout same branch as current enterprise branch in the community worktree passing -u also sets the upgrade repo
- **o-sync-to-com** : create or checkout same branch as current community branch in the enterprise worktree passing -u also sets the upgrade repo
- **o-bin** [params]: runs odoo
- **o-dev** [params]: runs odoo-bin with --dev=all
- **o-shell** [params]: runs shell
- **o-kill** : kills all odoo instances
- **o-init** [-v] [module1,module2,...] : initilize modules and exit, if no modules given, it installs l10n_generic_coa with -v the info log are not suppressed
- **o-upgrade** [-v] [module1,mudule2,...] : upgrades selected modules or all if no module provided and exits, with -v the info log are not suppressed
- **o-test** [-a|-e|-c] [-v|-q] test-tags : runs tests and exit, -a,-e,-c: all,enterprise,comunity, -v verbose, no post processing, -q show firstline trace of failed tests only
- **o-psql** : launches psql on current db
- **o-drop** : drops active db
- **o-backup** : copies current database to a temporary dbname-backup
- **o-restore** : erase current db and retore backup taken with o-backup
- **o-backup2** : copies current database to a temporary dbname-backup2, overrights this backup 
- **o-restore2** : erase current db and retore backup taken with o-backup2
- **o-trans-export** [-i] module [lang]: installs the module and exports pot, or exports po file for module and selected language. -i means inplace, it overwrite the existing file in module 
- **o-trans-update** module: exports a new pot file and upgrade all po files to match it. Overwrites the original files!
- **o-se** -> shortcut for o-sync-ent
- **o-sc** -> shortcut for o-sync-com


all o-* commands can be invoked without 'o-', e.g './o branch' is equal to './o o-branch'

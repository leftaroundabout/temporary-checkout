# temporary-checkout
Simple script that abuses git for automatic backups.

This script will clone a git repository into a temporary folder. If you leave without committing and pushing all changes, it will do this automatically for you, giving a timestamped backup (like something in between an automatic backup and a `git stash`).

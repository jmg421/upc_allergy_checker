#!/bin/bash

# Escape any ongoing Git operations
echo "Aborting any ongoing Git operations (rebase, merge, cherry-pick)..."
git rebase --abort &>/dev/null
git merge --abort &>/dev/null
git cherry-pick --abort &>/dev/null

# Stash any uncommitted changes to avoid data loss
echo "Stashing uncommitted changes..."
git stash push -m "Temporary stash before reset" &>/dev/null

# Fetch latest updates from the remote repository
echo "Fetching latest changes from remote..."
git fetch origin

# Reset the branch to the latest remote commit
echo "Resetting to the latest commit from the remote branch..."
git reset --hard origin/master

# Restore stashed changes if needed
echo "Applying stashed changes (if any)..."
git stash pop &>/dev/null || echo "No stashed changes to apply."

echo "You have successfully escaped the Git loop!"


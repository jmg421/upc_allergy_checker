#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Committing changes..." 

git add .
git commit 
echo "Changes committed."

echo "Pushing changes to the repository..."
git push
echo "Changes pushed successfully."


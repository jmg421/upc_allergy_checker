output_file="$(basename "$PWD").txt"

find . \( -path "./venv" -o -path "./__pycache__" -o -name "$output_file" \) -prune -o -type f -print0 | \
    xargs -0 -I {} sh -c '
        if file --mime-type "$1" | grep -q "text/"; then
            echo "##### START $1 #####"
            cat "$1"
            echo "##### END $1 #####"
        fi
    ' _ {} > "$output_file"


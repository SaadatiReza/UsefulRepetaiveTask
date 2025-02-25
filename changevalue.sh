#!/bin/bash

# Input file containing key=value pairs
input_file="input.txt"
# Output file to save the transformed content
output_file="prod.yaml"

# Clear output file before appending new content
> "$output_file"

# Process each line of the input file
while IFS='=' read -r key value; do
  # Trim spaces around key (important for proper comment detection)
  key=$(echo "$key" | xargs)

  # Skip empty lines and lines that start with #
  [[ -z "$key" || "$key" =~ ^# ]] && continue

  # Trim spaces around value
  value=$(echo "$value" | xargs)

  # Remove any leading hyphen (-) from the key
  key=${key#-}

  # Print in the desired format
  echo "  - name: $key" >> "$output_file"
  echo "    value: \"$value\"" >> "$output_file"
done < "$input_file"

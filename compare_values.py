import yaml
import sys
import re

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file) or []

            # Clean 'name' field by removing leading hyphens and spaces
            cleaned_data = []
            for item in data:
                if isinstance(item, dict) and 'name' in item:
                    name = re.sub(r'^-\s*', '', item['name'])
                    value = item.get('value', None)  # Default to None if 'value' is missing
                    cleaned_data.append({'name': name, 'value': value})

            return cleaned_data
    except yaml.YAMLError as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None

def compare_yaml(file1, file2):
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)

    if yaml1 is None or yaml2 is None:
        print("Could not load one or both YAML files due to syntax errors.")
        return []

    yaml1_dict = {item['name']: item['value'] for item in yaml1 if 'name' in item}
    yaml2_dict = {item['name']: item['value'] for item in yaml2 if 'name' in item}

    differences = []

    # Check for missing keys in file2
    for key in sorted(yaml1_dict.keys()):
        if key not in yaml2_dict:
            differences.append(f"'{key}' exists in {file1} with value '{yaml1_dict[key]}' but not in {file2}")
        elif yaml1_dict[key] != yaml2_dict[key]:
            differences.append(f"Value mismatch for '{key}': {file1}='{yaml1_dict[key]}' vs {file2}='{yaml2_dict[key]}'")

    # Check for extra keys in file2
    for key in sorted(yaml2_dict.keys()):
        if key not in yaml1_dict:
            differences.append(f"'{key}' exists in {file2} with value '{yaml2_dict[key]}' but not in {file1}")

    return differences

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_yaml.py <file1.yaml> <file2.yaml>")
        return  # Avoid sys.exit(1) to prevent SystemExit

    file1, file2 = sys.argv[1], sys.argv[2]
    differences = compare_yaml(file1, file2)

    if differences:
        print("Differences found:")
        for diff in differences:
            print("-", diff)
    else:
        print("No differences found.")

if __name__ == "__main__":
    main()

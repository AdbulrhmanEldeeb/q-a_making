import os
import json

# Folder containing JSON files
input_folder = "combine"  # Replace with your folder path
output_file = "combined_output.json"

# List to hold combined data
combined_data = []

# Iterate through all files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):  # Check if the file is a JSON file
        file_path = os.path.join(input_folder, filename)
        try:
            # Read and load the JSON data
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                # Add the data to the combined list
                combined_data.extend(data if isinstance(data, list) else [data])
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

# Write the combined data to a single JSON file
with open(output_file, 'w', encoding='utf-8') as output_json:
    json.dump(combined_data, output_json, indent=4, ensure_ascii=False)

print(f"Combined JSON saved to {output_file}.")

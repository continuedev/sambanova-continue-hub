#!/usr/bin/env python3

import os
import logging
import argparse

# Update me to the latest when you commit new versions
DEFAULT_VERSION="1.0.1"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the models and their capabilities
# Possible roles are: chat, edit, apply, autocomplete
models = {
    "DeepSeek-R1-Distill-Llama": {
        "70B": ["chat", "edit", "apply"]
    },
    "DeepSeek": {
        "R1": ["chat", "edit", "apply"]
    },
    "Llama-3.1": {
        "Tulu-3-405B": ["chat", "edit", "apply"]
    },
    "Meta-Llama-3.1": {
        "8B-Instruct": ["chat", "edit", "apply"],
        "70B-Instruct": ["chat", "edit", "apply"],
        "405B-Instruct": ["chat", "edit", "apply"]
    },
    "Meta-Llama-3.2": {
        "1B-Instruct": ["chat", "edit", "apply"],
        "3B-Instruct": ["chat", "edit", "apply"],
        "11B-Vision-Instruct": ["chat", "edit", "apply"],
        "90B-Vision-Instruct": ["chat", "edit", "apply"]
    },
    "Meta-Llama-3.3": {
        "70B-Instruct": ["chat", "edit", "apply"]
    },
    "Qwen2.5": {
        "Coder-32B-Instruct": ["chat", "edit", "apply", "autocomplete"],
        "72B-Instruct": ["chat", "edit", "apply"]
    },
    "QwQ": {
        "32B-Preview": ["chat", "edit", "apply"]
    }
}

def create_yaml_files(models, version):
    base_path = './blocks/public'

    # Create the directory if it doesn't exist
    try:
        os.makedirs(base_path)
    except FileExistsError:
        pass

    for model_name, model_attributes in models.items():
        for size, supported_roles in model_attributes.items():
            yaml_content = f"""---
name: {model_name} {size}
version: {version}
models:
- name: {model_name} {size}
  provider: sambanova
  model: {model_name}-{size}
  roles:
"""

            for role in supported_roles:
                yaml_content += f"    - {role}\n"

            file_path = os.path.join(base_path, f"{model_name.lower()}-{size.lower()}.yaml")
            try:
                with open(file_path, 'w') as file:
                    file.write(yaml_content)
                logging.info(f"Created YAML file for {model_name} {size}: {file_path}")
            except IOError as e:
                logging.error(f"Failed to write file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate YAML files for models.")
    parser.add_argument('--version', default=DEFAULT_VERSION, help='Version string for the YAML files')

    args = parser.parse_args()
    create_yaml_files(models, args.version)

if __name__ == "__main__":
    main()

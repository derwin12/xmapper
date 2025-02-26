import json


def save_mapping_file(models, groups, mapping, filename="xlights_mapping.xmap"):
    """Save mapping to a file in xLights format.

    Outputs all source models on separate lines first,
    then lists each source model with its corresponding target model.
    """
    with open(filename, 'w') as f:
        # First list all source models
        f.write("false\n")
        f.write(f"{len(models) + len(groups)}\n")
        for model in models:
            f.write(f"{model['name']}\n")
        for group in groups:
            f.write(f"{group['attributes']['name']}\n")

        # Then list all source-target pairs
        for item in mapping:
            for entry in item:
                source = entry["available_model"]["name"]
                target = entry["vendor_model"]["name"]
                f.write(f"{source}\t\t\t{target}\twhite\n")

    print(f"Mapping saved to {filename}")
    return filename


def print_mapping(mapping):
    """Print mapping in a readable format."""
    print("\nxLights Mapping: (Avail == Vendor)")
    print("==================================")

    total_mappings = 0

    for item in mapping:
        for entry in item:
            available_name = entry["available_model"]["name"]
            vendor_name = entry["vendor_model"]["name"]
            combined_score = entry["combined_score"]

            print(f"{available_name}  ==  {vendor_name}  (Score: {combined_score:.2f})")
            total_mappings += 1

    print(f"Total mappings: {total_mappings}")


def parse_model(model_data):
    """Parse a model data string into a dictionary."""
    try:
        # Try parsing as JSON if it's properly formatted
        return json.loads(model_data)
    except json.JSONDecodeError:
        # If not proper JSON, try to extract as Python dict
        try:
            # Handle Python dict literal format
            return eval(model_data)
        except:
            print(f"Error parsing model data: {model_data[:50]}...")
            return {}

if __name__ == "__main__":
            # Example usage
            mapping = [
                [
                    {
                        'available_model': {'DisplayAs': 'Custom', 'name': 'Spiral mini-1',
                                            'ModelType': 'T:Spiral mini'},
                        'vendor_model': {'DisplayAs': 'Custom', 'name': 'NSR Spiral Tree',
                                         'ModelType': 'T:Spiral mini'},
                        'combined_score': 0.6148148148148148,
                        'details': {'name_similarity': 0.5185185185185185, 'type_similarity': 1.0}
                    }
                ]
            ]
            print_mapping(mapping)
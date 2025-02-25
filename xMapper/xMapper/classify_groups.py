

sample_group = {
    "attributes": {
        "selected": "0",
        "name": "Arches",
        "GridSize": "400",
        "layout": "minimalGrid",
        "models": "Arch-1,Arch-2,Arch-3,Arch-4,Arch-5,Arch-6,Arch-7,Arch-8,Arch-9",
        "LayoutGroup": "Default"
    },
    "models": [
        "Arch-1",
        "Arch-2",
        "Arch-3"
    ]
}

sample_models = {
    "Arch-1": {
        "DisplayAs": "Arches",
        "StartSide": "B",
        "Dir": "L",
        "name": "Arch-1",
        "ModelType": "T:Arch"
    },
    "Arch-2": {
        "DisplayAs": "Arches",
        "StartSide": "B",
        "Dir": "L",
        "name": "Arch-2",
        "ModelType": "T:Arch"
    },
    "Arch-3": {
        "DisplayAs": "Custom",
        "StartSide": "B",
        "Dir": "L",
        "name": "Arch-3",
        "ModelType": "Unknown"
    },
    "Arch-4": {
        "DisplayAs": "Arches",
        "StartSide": "B",
        "Dir": "L",
        "name": "Arch-4",
        "ModelType": "T:Arch"
    }
    # Add more models as needed...
}

def get_group_type(group, models):
    """
    Returns the common model type of the group.
    If the group contains mixed model types (excluding "Unknown"), returns None.
    Updates "Unknown" model types to match the rest of the group.
    """
    # Get the list of model names in the group
    model_names = group["models"]

    # If there are no models, return None
    if not model_names:
        return None

    # Create a dictionary to map model names to their types
    model_type_map = {}

    for model in models:
        model_name = model['name']
        model_type = model.get('ModelType', 'Unknown')
        model_type_map[model_name] = model_type

    # Determine the model types for the group
    group_model_types = []
    for name in model_names:
        model_type = model_type_map.get(name, 'Unknown')
        group_model_types.append(model_type)

    # Filter out "Unknown" types to determine the common type
    known_types = [t for t in group_model_types if t != 'Unknown']

    if not known_types:
        # If all types are "Unknown", return "Unknown"
        return None

    # Check if all known types are the same
    common_type = known_types[0]
    for t in known_types:
        if t != common_type:
            # If there are mixed types, return None
            return None

    # Update models with "Unknown" model type to the common type
    for model in models:
        if model.get('ModelType', 'Unknown') == 'Unknown':
            model['ModelType'] = common_type


    return common_type.replace("T:","G:")  # Return the common model type


if __name__ == "__main__":
    print("Before....")
    for model_key, model_details in sample_models.items():
            print("Model ", model_details['name'], ' is of type ', model_details['ModelType'])

    group_type = get_group_type(sample_group, sample_models)
    if group_type:
        sample_group['attributes']['GroupType'] = group_type
        print("The group " + sample_group['attributes']['name'] + " made up of model type.", group_type)
    else:
        sample_group['attributes']['GroupType'] = "Unknown"
        print("The group contains mixed model types.")
    print("After.....")
    for model_key, model_details in sample_models.items():
            print("Model ", model_details['name'], ' is of type ', model_details['ModelType'])
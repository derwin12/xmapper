import json
import re
from difflib import SequenceMatcher


def similar(a, b):
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a, b).ratio()


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


def get_match_score(name1, name2):
    """Get a match score between two names with various matching strategies."""
    # Basic similarity
    basic_score = similar(name1.lower(), name2.lower())

    # Try matching after removing common prefixes
    cleaned1 = re.sub(r'^(Group\s*-\s*)', '', name1)
    cleaned2 = re.sub(r'^(Group\s*-\s*)', '', name2)
    cleaned_score = similar(cleaned1.lower(), cleaned2.lower())

    # Try matching just the base name without numbers/positions
    base1 = re.sub(r'[-_\s]*\d+.*$', '', name1)
    base2 = re.sub(r'[-_\s]*\d+.*$', '', name2)
    base_score = similar(base1.lower(), base2.lower())

    # Return the best score
    return max(basic_score, cleaned_score, base_score)


def create_mapping(set1_models, set1_groups, set2_models, set2_groups, threshold=0.6):
    """Create mapping between two sets of models and groups."""
    mapping = {}

    # Match groups first
    for group1 in set1_groups:
        group1_name = group1.get('attributes', {}).get('name', group1.get('name', ''))
        best_match = None
        best_score = 0

        for group2 in set2_groups:
            group2_name = group2.get('attributes', {}).get('name', group2.get('name', ''))
            score = get_match_score(group1_name, group2_name)

            # Add bonus for matching group types
            group1_type = group1.get('attributes', {}).get('GroupType', group1.get('GroupType', ''))
            group2_type = group2.get('attributes', {}).get('GroupType', group2.get('GroupType', ''))
            if group1_type and group1_type == group2_type:
                score += 0.2

            if score > best_score and score >= threshold:
                best_score = score
                best_match = group2_name

        if best_match:
            mapping[group1_name] = best_match

            # If groups matched, try to match their child models too
            if 'models' in group1.get('attributes', {}) and 'models' in group2.get('attributes', {}):
                g1_models = group1['attributes']['models'].split(',') if isinstance(group1['attributes']['models'],
                                                                                    str) else group1['attributes'][
                    'models']
                g2_models = group2['attributes']['models'].split(',') if isinstance(group2['attributes']['models'],
                                                                                    str) else group2['attributes'][
                    'models']

                # Try to match by position in list first, then by name similarity
                for i, m1 in enumerate(g1_models):
                    if i < len(g2_models):
                        # Position-based match
                        mapping[m1] = g2_models[i]
                    else:
                        # Try name-based match for remaining models
                        for m2 in g2_models:
                            if m2 not in mapping.values() and get_match_score(m1, m2) >= threshold:
                                mapping[m1] = m2
                                break

    # Match individual models
    for model1 in set1_models:
        model1_name = model1.get('name', '')
        if model1_name in mapping:
            continue  # Skip if already mapped via group

        best_match = None
        best_score = 0

        for model2 in set2_models:
            model2_name = model2.get('name', '')
            if model2_name in mapping.values():
                continue  # Skip if already mapped

            score = get_match_score(model1_name, model2_name)

            # Add bonus for matching model types
            model1_type = model1.get('ModelType', '')
            model2_type = model2.get('ModelType', '')
            if model1_type and model1_type == model2_type:
                score += 0.2

            if score > best_score and score >= threshold:
                best_score = score
                best_match = model2_name

        if best_match:
            mapping[model1_name] = best_match

    return mapping


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
        for source, target in mapping.items():
            f.write(f"{source}\t\t\t{target}\twhite\n")

    print(f"Mapping saved to {filename}")
    return filename


def print_mapping(mapping):
    """Print mapping in a readable format."""
    print("\nxLights Mapping:")
    print("===============")
    for source, target in mapping.items():
        print(f"{source}  ==  {target}")
    print(f"Total mappings: {len(mapping)}")


# Example usage
def mapping(set1_model_data, set1_group_data, set2_model_data, set2_group_data):
    # Create the mapping
    mapping = create_mapping(set1_model_data, set1_group_data, set2_model_data, set2_group_data)

    # Print the mapping
    print_mapping(mapping)

    # Save the mapping to a file
    save_mapping_file(set1_model_data, set1_group_data, mapping)


if __name__ == "__main__":
    # Replace these with your actual data strings
    set1_model_data = [{'DisplayAs': 'Custom', 'StartSide': 'B', 'Dir': 'L', 'parm3': '1',
                        'CustomModel': ',,,,,,,,,,,,,,,,,,,,,,,,,,50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,49,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,48,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,47,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,46,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,45,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,44,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,43,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,42,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,41,,,,,,40,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,39,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,38,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,37,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,36,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,35,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,34,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,33,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,26,,,,,25,,,,,,24,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,27,,,,,,,,,,,,,,,,,,,,,,23,,,,32,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,22,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,31,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,28,,,,29,,,,,,30,,,,,,,,,,,,,,,,,,,,,,,21,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,20,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,19,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,18,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,17;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,16,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,3,,,,,2,,,,,,,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,4,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,15,,,,,;,5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,14,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;6,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,13,,,,,,,,,,,,,,,,;,,7,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,12,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,8,,,,,9,,,,,,,,,,,,,,,,,,11,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
                        'CustomModelCompressed': '', 'parm1': '56', 'parm2': '82', 'Depth': '1',
                        'StringType': 'RGB Nodes', 'PixelSize': '2', 'Transparency': '0', 'ModelBrightness': '',
                        'Antialias': '1', 'StrandNames': 'MyCustomModel', 'NodeNames': '', 'PixelCount': '50',
                        'PixelType': '12mm bullet', 'PixelSpacing': '', 'LayoutGroup': 'Default', 'Controller': 'F48',
                        'ModelChain': '>PixStake-R2', 'name': 'Spiral mini-1', 'WorldPosX': '125.4340',
                        'WorldPosY': '18.2550', 'WorldPosZ': '505.1145', 'ScaleX': '0.2162', 'ScaleY': '0.2268',
                        'ScaleZ': '0.0196', 'RotateX': '0.00000000', 'RotateY': '0.00000000', 'RotateZ': '0.00000000',
                        'versionNumber': '7', 'StartChannel': '!F48:9718', 'ModelType': 'T:Spiral mini'}]
    set1_group_data = [{'attributes': {'selected': '0', 'name': 'Group - Arches', 'LayoutGroup': 'Default',
                                       'models': 'Arches-1-Left,Arches-2-Left,Arches-3-LL,Arches-4-L,Arches-5-M,Arches-6-R,Arches-7-RR',
                                       'GridSize': '400', 'layout': 'Single Line', 'GroupType': 'G:Arch'},
                        'models': ['Arches-1-Left', 'Arches-2-Left', 'Arches-3-LL', 'Arches-4-L', 'Arches-5-M',
                                   'Arches-6-R', 'Arches-7-RR']}]

    set2_model_data = [{'DisplayAs': 'Custom', 'StartSide': 'B', 'Dir': 'L', 'parm3': '1',
                        'CustomModel': ',,,,,,,,,,,,,,,,,,,,43,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,9,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,42,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,10,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,41,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,11,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,44,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,8,,,,,,,,,,,,,,,,,,,,,;,,,,,,,40,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,12,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,39,,,,,,,,,,,,,,,,,,,45,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,7,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,13,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;38,,,,,37,,,,,,,,,,,,,,,,,,,,46,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,6,,,,,,,,,,,,,,,,,,,,15,,,,,14;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,50,,,,,,,2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,36,,,,,,,,,,,,,,,,,,,47,,,,,,,,,,,,,1,,,,,,,,,,,,,5,,,,,,,,,,,,,,,,,,,,16,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,48,,,,,,,,,,,,,3,,,,,4,,,,,,,,,,,,,,,,,,,,,17,,,,,,,,,,,,;,,,,,,,,,,,,35,,,,,,,,,,,,,,,,,,,,,,,,,,,49,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,33,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,19,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,34,,,,,,,,,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,18,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,20,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,31,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,21,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,30,,,,29,,,,,,,,,,,,,,,,,,,,23,,,,22,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,28,,,,,,,,,,,,24,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,27,,,,,25,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,26,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
                        'parm1': '85', 'parm2': '41', 'Depth': '1', 'StringType': 'RGB Nodes', 'Transparency': '0',
                        'ModelBrightness': '', 'Antialias': '1', 'StrandNames': '', 'NodeNames': '', 'PixelCount': '50',
                        'PixelType': '12mm bullet', 'PixelSpacing': '', 'LayoutGroup': 'Default',
                        'name': 'Roof Bat Mega-4', 'PixelSize': '3', 'WorldPosX': '793.0977', 'WorldPosY': '330.6117',
                        'WorldPosZ': '0.0000', 'ScaleX': '0.6039', 'ScaleY': '0.4390', 'ScaleZ': '0.6039',
                        'RotateX': '-0.00000000', 'RotateY': '-0.00000000', 'RotateZ': '23.00000000', 'Locked': '1',
                        'versionNumber': '5', 'StartChannel': '>Roof Bat Mega-3:1', 'ModelType': 'T:Bat Mega'}]
    set2_group_data = [{'attributes': {'selected': '0', 'name': 'Arches', 'GridSize': '400', 'layout': 'minimalGrid',
                                       'models': 'Arch-1,Arch-2,Arch-3,Arch-4,Arch-5,Arch-6,Arch-7,Arch-8,Arch-9',
                                       'LayoutGroup': 'Default', 'GroupType': 'G:Arch'},
                        'models': ['Arch-1', 'Arch-2', 'Arch-3', 'Arch-4', 'Arch-5', 'Arch-6', 'Arch-7', 'Arch-8', 'Arch-9']}]

    mapping(set1_model_data, set1_group_data, set2_model_data, set2_group_data)

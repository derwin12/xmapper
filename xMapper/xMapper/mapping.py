import difflib
import json
import re
from difflib import SequenceMatcher

from xMapper.xMapper.mapping_utils import print_mapping, save_mapping_file


def clean_name(name):
    """Clean name by removing special characters and standardizing format."""
    # Remove non-alphanumeric characters and convert to lowercase
    clean = re.sub(r'[^a-zA-Z0-9 ]', '', str(name)).lower()

    # Remove brand names, trademarks, and common abbreviations
    ignore_terms = ['GE', 'EFL', 'Boscoyo', 'Chroma', 'Twinkly', 'IMPRESSION', 'Daycor',
                    'GRP', 'Group', 'SS', 'Showstopper',
                    'PPD', 'PixelTrim', 'PixNode', 'xTreme']
    for term in ignore_terms:
        name = name.replace(term.lower(), '')

    return clean


def similar(name1, name2):
    """Calculate similarity between two names."""
    # Clean names
    clean1 = clean_name(name1)
    clean2 = clean_name(name2)

    # Use SequenceMatcher for similarity
    similarity = difflib.SequenceMatcher(None, clean1, clean2).ratio()
    print("Compare [" + name1 + '] with [' + name2 + ']', similarity)
    return similarity


def match_similar(a, b):
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a, b).ratio()


def string_similarity(s1, s2):
    if not s1 or not s2:
        return 0.0
    clean_s1 = clean_name(s1)
    clean_s2 = clean_name(s2)
    return difflib.SequenceMatcher(None, clean_s1, clean_s2).ratio()


def match_models(available_models, vendor_models, name_weight=0.8, type_weight=0.2, threshold=0.6):
    """Match models between the two sets based on name similarity."""
    model_matches = []

    for avail_model in available_models:
        avail_name = avail_model.get('name', '')
        avail_type = avail_model.get('ModelType', '')

        best_match = None
        best_score = 0
        best_details = {}

        for vendor_model in vendor_models:
            vendor_name = vendor_model.get('name', '')
            vendor_type = vendor_model.get('ModelType', '')

            # Calculate component similarities
            name_sim = string_similarity(avail_name, vendor_name)
            type_sim = string_similarity(avail_type, vendor_type)

            # Calculate weighted score
            combined_score = (name_weight * name_sim) + (type_weight * type_sim)

            if combined_score > best_score:
                best_score = combined_score
                best_match = vendor_model
                best_details = {
                    'name_similarity': name_sim,
                    'type_similarity': type_sim
                }

        if best_match and best_score >= threshold:
            model_matches.append({
                'available_model': avail_model,
                'vendor_model': best_match,
                'combined_score': best_score,
                'details': best_details
            })

    # Sort by combined score
    model_matches.sort(key=lambda x: x['combined_score'], reverse=True)
    return model_matches

def match_groups(available_groups, vendor_groups, name_weight=0.8, type_weight=0.2, threshold=0.6):
    """Match groups between the two sets based on name similarity."""
    group_matches = []
    print("-------------")
    print("Avail", available_groups)
    print("Vendor", vendor_groups)

    for avail_group in available_groups:
        avail_name = avail_group['attributes']['name']
        avail_type = avail_group['attributes']['GroupType']

        best_match = None
        best_score = 0
        best_details = {}

        for vendor_group in vendor_groups:
            vendor_name = vendor_group['attributes']['name']
            vendor_type = vendor_group['attributes']['GroupType']

            # Calculate component similarities
            name_sim = string_similarity(avail_name, vendor_name)
            type_sim = string_similarity(avail_type, vendor_type)
            print("Compare", avail_name, vendor_name, name_sim)
            print("Compare", avail_type, vendor_type, type_sim)

            # Calculate weighted score
            combined_score = (name_weight * name_sim) + (type_weight * type_sim)

            if combined_score > best_score:
                best_score = combined_score
                best_match = vendor_group
                best_details = {
                    'name_similarity': name_sim,
                    'type_similarity': type_sim
                }

        if best_match and best_score >= threshold:
            group_matches.append({
                'available_group': avail_group,
                'vendor_group': best_match,
                'combined_score': best_score,
                'details': best_details
            })

    # Sort by combined score
    group_matches.sort(key=lambda x: x['combined_score'], reverse=True)
    return group_matches

def get_match_score(name1, name2):
    """Get a match score between two names with various matching strategies."""
    # Basic similarity
    basic_score = similar(name1, name2)

    # Try matching after removing common prefixes
    cleaned1 = re.sub(r'^(Group\s*-\s*)', '', name1)
    cleaned2 = re.sub(r'^(Group\s*-\s*)', '', name2)
    cleaned_score = similar(cleaned1, cleaned2)

    # Try matching just the base name without numbers/positions
    base1 = re.sub(r'[-_\s]*\d+.*$', '', name1)
    base2 = re.sub(r'[-_\s]*\d+.*$', '', name2)
    base_score = similar(base1, base2)

    # Return the best score
    return max(basic_score, cleaned_score, base_score)


def create_mapping(available_models, available_groups, vendor_models, vendor_groups, threshold=0.6):
    """Create mapping between two sets of models and groups."""
    mapping = []
    print("Available", available_models)
    print('Vendor', vendor_models)

    # First pass: Map exact model name matches
    model_matches = match_models(available_models, vendor_models)
    print('Model Matches', model_matches)

    if model_matches:
        mapping.append(model_matches)

    print('==========MODELS==================')
    print(mapping)

    print("Available GRP", available_groups)
    print('Vendor GRP', vendor_groups)

    # Second pass: Map exact group name matches
    group_matches = match_groups(available_groups, vendor_groups)
    print('Group Matches', group_matches)

    if group_matches:
        mapping.append(group_matches)

    return mapping

    for group1 in available_groups:
        group1_name = group1.get('attributes', {}).get('name', group1.get('name', ''))
        best_match = None
        best_score = 0

        for group2 in vendor_groups:
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
    for model1 in available_models:
        model1_name = model1.get('name', '')
        if model1_name in mapping:
            continue  # Skip if already mapped via group

        best_match = None
        best_score = 0

        for model2 in vendor_models:
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


def mapping(available_model_data, available_group_data, vendor_model_data, vendor_group_data):
    # Create the mapping
    mapping = create_mapping(available_model_data, available_group_data, vendor_model_data, vendor_group_data)

    # Print the mapping
    print_mapping(mapping)

    # Save the mapping to a file
    save_mapping_file(available_model_data, available_group_data, mapping)


if __name__ == "__main__":
    # Replace these with your actual data strings
    available_model_data = [{'DisplayAs': 'Custom', 'name': 'Spiral mini-1', 'ModelType': 'T:Spiral mini'}]
    available_group_data = [{'attributes': {'name': 'Group - Arches',
                                            'models': 'Arches-1-Left,Arches-2-Left,Arches-3-LL,Arches-4-L,Arches-5-M,Arches-6-R,Arches-7-RR',
                                            'GroupType': 'G:Arch'},
                             'models': ['Arches-1-Left', 'Arches-2-Left', 'Arches-3-LL', 'Arches-4-L', 'Arches-5-M',
                                        'Arches-6-R', 'Arches-7-RR']}]

    vendor_model_data = [{'DisplayAs': 'Custom', 'name': 'Roof Bat Mega-4', 'ModelType': 'T:Bat Mega'},
                         {'DisplayAs': 'Custom', 'name': 'NSR Spiral Tree', 'ModelType': 'T:Spiral mini'}]
    vendor_group_data = [{'attributes': {'name': 'Arches',
                                         'models': 'Arch-1,Arch-2,Arch-3,Arch-4,Arch-5,Arch-6,Arch-7,Arch-8,Arch-9',
                                         'GroupType': 'G:Arch'},
                          'models': ['Arch-1', 'Arch-2', 'Arch-3', 'Arch-4', 'Arch-5', 'Arch-6', 'Arch-7', 'Arch-8',
                                     'Arch-9']}]

    mapping(available_model_data, available_group_data, vendor_model_data, vendor_group_data)

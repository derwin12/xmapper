from data_types import MODEL_TYPES
from classify_custom import classify_custom
import re


def close_match(key, name, display_as, description):
    # Preprocess the key and the text fields by removing spaces and underscores
    def preprocess(text):
        return re.sub(r'[\s_]+', '', text).lower()  # Remove spaces and underscores, and convert to lowercase

    key_processed = preprocess(key)
    name_processed = preprocess(name)
    display_as_processed = preprocess(display_as)
    description_processed = preprocess(description)

    # Check if the processed key matches any of the processed fields
    return key_processed in name_processed or key_processed in display_as_processed or key_processed in description_processed


def classify_model(model, cache, vendor_models):
    name = model.get("name", "").lower()
    display_as = model.get("DisplayAs", "").lower()
    description = model.get("description", "").lower()
    pixel_count = int(model.get("parm2", 0))

    #print("Classify: ", model['name'] + " - " + model['DisplayAs'])
    # if name in cache:
    #   print('Found in cache ', model['name'], cache[name])
    #  return cache[name]

    # Handle Trees first
    #print(name, display_as)
    if (display_as == 'tree 360'):
        if('TreeSpiralRotations' in model):
            cache[name] = "T:Spiral_Tree"
            return "T:Spiral_Tree"

        if('parm2' in model):
            if(int(model['parm2']) < 50):
                cache[name] = "T:Tree"
                return "T:Tree"

        cache[name] = "T:Mega_Tree"
        return "T:Mega_Tree"

    if (display_as == 'arches'):
        if ('LayerSizes' in model):
            values = [x.strip() for x in model["LayerSizes"].split(",")]
            if (len(values) >= 2):
                cache[name] = "T:TripleArch"
                return "T:TripleArch"

    if 'Description' in model:
        if model['Description'][:2] == "T:":
            return model['Description']

    if (display_as == 'custom'):
            #print("Search custom models")
            cat = classify_custom(model, vendor_models)
            if (cat != ""):
                cache['name'] = cat
                return cat

    # Match based on name and model_type
    for key, model_type in MODEL_TYPES.items():
        if close_match(key, name, display_as, description):
            cache[name] = model_type
            #print("Close name match to", model_type)
            return model_type
        # else:
        #   print('Failed search', key, ' not found in ', name, display_as, description)

    # Fuzzy Exact Match
    # Model Type
    # -- refine this
    # Description
    # single lines/strands horizontal/vertical
    # Custom Models .. need a repo of custom models
    #   submodels?
    #   pixel counts?
    #   model data?
    #   states?
    # Check for Group models so "Arches Group" likely contains arches.
    # Aliases
    # Additional heuristics for classification
    if "matrix" in display_as and pixel_count > 100:
        cache[name] = "T:Matrix"
        return "T:Matrix"
    if "tree" in display_as:
        if pixel_count > 100:
            cache[name] = "T:Tree_Mega"
            return "T:Tree_Mega"
        elif pixel_count > 50:
            cache[name] = "T:Tree_Mini"
            return "T:Tree_Mini"
        elif "spiral" in display_as or "spiral" in name:
            cache[name] = "T:Tree_Spiral"
            return "T:Tree_Spiral"
        cache[name] = "T:Tree"
        return "T:Tree"
    if "icicle" in display_as:
        cache[name] = "T:Icicles"
        return "T:Icicles"

    cache[name] = "Unknown"
    return "Unknown"

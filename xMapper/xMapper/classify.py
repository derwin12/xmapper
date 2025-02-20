
from data_types import MODEL_TYPES

def classify_model(model, cache):
    name = model.get("name", "").lower()
    display_as = model.get("DisplayAs", "").lower()
    description = model.get("description", "").lower()
    pixel_count = int(model.get("parm2", 0))

    print("Classify: ", model['name'] + " - " + model['DisplayAs'])
    #if name in cache:
     #   print('Found in cache ', model['name'], cache[name])
      #  return cache[name]

    for key, model_type in MODEL_TYPES.items():
        if key in name or key in display_as or key in description:
            cache[name] = model_type
            return model_type

    # Fuzzy Exact Match
    # Model Type
    # -- refine this
    # Description
    # single lines/strands horizontal/vertical
    # Custom Models ..
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
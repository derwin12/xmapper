import re
from fuzzywuzzy import fuzz

def fuzzy_match(str1, str2, threshold=80):
    """
    Perform a partial fuzzy match between two strings.

    Args:
        str1 (str): The first string to compare.
        str2 (str): The second string to compare.
        threshold (int): The similarity threshold (0-100). Default is 80.

    Returns:
        bool: True if one string is a partial match of the other, False otherwise.
    """
    similarity_ratio = fuzz.partial_ratio(str1, str2)
    return similarity_ratio >= threshold

def classify_custom(model):
    print("Custom ... looking for ", model['name'])
    mstr = model['name'].lower()
    mstr_stripped = re.sub(r'[^a-z]', '', mstr)
    #print('Fuzzy match ', model['name'], 'teddy', fuzzy_match(model['name'], 'teddy'))
    if (fuzzy_match(model['name'], 'teddy')):
        return 'T:Teddy'

    # check for clues in the name
    #print('Fuzzy match ', model['name'], 'spinner', fuzzy_match(model['name'], 'spinner'))
    if (fuzzy_match(model['name'], 'spinner')):
        return 'T:Spinner'

    return ""
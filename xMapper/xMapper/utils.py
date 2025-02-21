import re
from fuzzywuzzy import fuzz

def normalize_string(s):
    # Remove non-alphanumeric characters and convert to lowercase
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

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
    str1_normalized = normalize_string(str1)
    str2_normalized = normalize_string(str2)
    similarity_ratio = fuzz.partial_ratio(str1_normalized, str2_normalized)
    return similarity_ratio >= threshold
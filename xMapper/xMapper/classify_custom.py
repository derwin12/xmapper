import re
from utils import fuzzy_match

def classify_custom(model):
    print("Custom ... looking for ", model['name'])
    mstr = model['name'].lower()
    mstr_stripped = re.sub(r'[^a-z]', '', mstr)
    #print('Fuzzy match ', model['name'], 'teddy', fuzzy_match(model['name'], 'teddy'))
    if (fuzzy_match(model['name'], 'teddy')):
        return 'T:Teddy'

    # check for clues in the name
    #print('Fuzzy match ', model['name'], 'cane', fuzzy_match(model['name'], 'cane'))
    if (fuzzy_match(model['name'], 'spinner')):
        return 'T:Spinner'
    if (fuzzy_match(model['name'], 'cane')):
        return 'T:CandyCane'
    if (fuzzy_match(model['name'], 'flake')):
        return 'T:Snowflake'
    if (fuzzy_match(model['name'], 'bulb')): # AND has faces TODO
        return 'T:Singing'

    return ""
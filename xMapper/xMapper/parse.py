import xml.etree.ElementTree as ET
from classify import classify_model
import json
import os


from data_types import MODEL_TYPES
from views import extract_models

CACHE_FILE = "model_classifications.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file, indent=4)


def parse_models(xml_string):
    root = ET.fromstring(xml_string)
    models = []
    cache = load_cache()

    models_parent = root.find("models")
    if models_parent is None:
        raise ValueError("No <models> element found in XML")

    for model in models_parent.findall("model"):
        model_data = {attr: model.get(attr) for attr in model.attrib}  # Store attributes
        # active = model.find("Active")
        if ('Active' in model_data):
            print("Skipping inactive ", model_data['name'])
            continue
        controller = model.find("ControllerConnection")
        if controller is not None:
            model_data["ControllerProtocol"] = controller.get("Protocol")  # Store controller protocol

        print("Working on ....", model_data['name'])
        model_data["ModelType"] = classify_model(model_data, cache)  # Add model classification
        models.append(model_data)

    save_cache(cache)
    return models


def print_model_categories(models):
    print("\nModel and Category:")

    for model in sorted(models, key=lambda m: m['name']):
        print(f"Model Name: {model['name']}, DisplayAs: {model['DisplayAs']}, Category: {model['ModelType']}")


def print_unknown_model_categories(models):
    print("\nUnknown Models:")

    for model in sorted(models, key=lambda m: m['name']):
        if 'ModelType' in model:
            if (model['ModelType'] == "Unknown"):
                print(f"Model Name: {model['name']}, DisplayAs: {model['DisplayAs']}, Category: {model['ModelType']}")


def dump_model_keys_and_values(model):
    """
    Dumps all key-value pairs for a given model.

    Args:
        model (dict): A dictionary representing a model.
    """
    print("Dumping model keys and values:")
    for key, value in model.items():
        print(f"{key}: {value}")


# Read and parse the XML file
def read_xml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()
    return xml_content


if __name__ == "__main__":
    # source_xml_path = "c:/users/Daryl/PycharmProjects/xmapper/samples/simple/source/xlights_rgbeffects.xml"
    source_xml_path = "F:/ShowFolderQA/xlights_rgbeffects.xml"

    models_xml = read_xml_file(source_xml_path)
    # models_xml = extract_models(source_xml_path)
    parsed_models = parse_models(models_xml)
    # dump_model_keys_and_values(models[0])

    print_model_categories(parsed_models)
    print_unknown_model_categories(parsed_models)

import xml.etree.ElementTree as ET
from classify import classify_model
import json
import os

from custom_models import load_xmodel_files
from xMapper.xMapper.classify_groups import get_group_type
from xMapper.xMapper.parse_groups import parse_groups, dump_group_keys_and_values, print_group_types

xml_data = '''
<xrgb>
<models>
    <model DisplayAs="Custom" StartSide="B" Dir="L" parm3="1" CustomModel=",,,,,,,,,,,,,,,,,,,,,,,,,,50,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,49,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,48,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,47,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,46,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,45,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,44,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,43,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,42,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,41,,,,,,40,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,39,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,38,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,37,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,36,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,35,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,34,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,33,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,26,,,,,25,,,,,,24,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,27,,,,,,,,,,,,,,,,,,,,,,23,,,,32,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,22,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,31,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,28,,,,29,,,,,,30,,,,,,,,,,,,,,,,,,,,,,,21,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,20,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,19,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,18,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,17;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,16,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,3,,,,,2,,,,,,,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,4,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,15,,,,,;,5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,14,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;6,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,13,,,,,,,,,,,,,,,,;,,7,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,12,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,8,,,,,9,,,,,,,,,,,,,,11,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,10,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,," CustomModelCompressed="" parm1="56" parm2="82" Depth="1" StringType="RGB Nodes" PixelSize="2" Transparency="0" ModelBrightness="" Antialias="1" StrandNames="MyCustomModel" NodeNames="" PixelCount="50" PixelType="12mm bullet" PixelSpacing="" LayoutGroup="Default" Controller="F48" ModelChain="&gt;PixStake-R2" name="Spiral mini-1" WorldPosX="125.4340" WorldPosY="18.2550" WorldPosZ="505.1145" ScaleX="0.2162" ScaleY="0.2268" ScaleZ="0.0196" RotateX="0.00000000" RotateY="0.00000000" RotateZ="0.00000000" versionNumber="7" StartChannel="!F48:9718">
      <stateInfo Name="Shadow" CustomColors="1" Type="NodeRange" s1="8-15,29-33,42-45,49-50" s1-Color="#ffffff" s1-Name="1" s2="7,16,28,34,41,46,48" s2-Color="#727272" s2-Name="2" s3="1-6,17-27,35-40,47" s3-Color="#1e1e1e" s3-Name="3"/>
      <faceInfo Name="Shadow" CustomColors="" Eyes-Closed="" Eyes-Closed-Color="" Eyes-Closed2="" Eyes-Closed2-Color="" Eyes-Closed3="" Eyes-Closed3-Color="" Eyes-Open="" Eyes-Open-Color="" Eyes-Open2="" Eyes-Open2-Color="" Eyes-Open3="" Eyes-Open3-Color="" FaceOutline="1-50" FaceOutline-Color="" FaceOutline2="" FaceOutline2-Color="" Mouth-AI="" Mouth-AI-Color="" Mouth-AI2="" Mouth-AI2-Color="" Mouth-E="" Mouth-E-Color="" Mouth-E2="" Mouth-E2-Color="" Mouth-FV="" Mouth-FV-Color="" Mouth-FV2="" Mouth-FV2-Color="" Mouth-L="" Mouth-L-Color="" Mouth-L2="" Mouth-L2-Color="" Mouth-MBP="" Mouth-MBP-Color="" Mouth-MBP2="" Mouth-MBP2-Color="" Mouth-O="" Mouth-O-Color="" Mouth-O2="" Mouth-O2-Color="" Mouth-U="" Mouth-U-Color="" Mouth-U2="" Mouth-U2-Color="" Mouth-WQ="" Mouth-WQ-Color="" Mouth-WQ2="" Mouth-WQ2-Color="" Mouth-etc="" Mouth-etc-Color="" Mouth-etc2="" Mouth-etc2-Color="" Mouth-rest="" Mouth-rest-Color="" Mouth-rest2="" Mouth-rest2-Color="" Type="NodeRange"/>
      <subModel name="Spiral" layout="horizontal" type="ranges" bufferstyle="Default" line0="1-50">
        <ControllerConnection/>
      </subModel>
      <subModel name="Backside" layout="horizontal" type="ranges" bufferstyle="Default" line0="1-6,,,,,,,,,,,,18-27,,,,,,,,,36-41,,,,,46-50">
        <ControllerConnection/>
      </subModel>
      <subModel name="Shadow" layout="horizontal" type="ranges" bufferstyle="Default" line0="1-50">
        <ControllerConnection/>
      </subModel>
      <ControllerConnection Port="17" Protocol="ws2811"/>
    </model>
</models>    
</xrgb>
'''

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


def parse_models(xml_string, vendor_models):
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
            #print("Skipping inactive ", model_data['name'])
            continue

        #print("Working on ....", model_data['name'])
        model_data["ModelType"] = classify_model(model_data, cache, vendor_models)  # Add model classification
        models.append(model_data)

    save_cache(cache)
    return models


def print_model_categories(models):
    print("\nModel and Category:")

    for model in sorted(models, key=lambda m: m['name']):
        print(f"Model Name: {model['name']}, DisplayAs: {model['DisplayAs']}, Category: {model['ModelType']}")
        print(model)


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
    #source_xml_path = "c:/users/Daryl/PycharmProjects/xmapper/samples/simple/source/xlights_rgbeffects.xml"
    print(os.getcwd())
    source_xml_path = 'c:/users/Daryl/PycharmProjects/xmapper/samples/simple/source/v1/xlights_rgbeffects.xml'
    #source_xml_path = "F:/ShowFolderQA/xlights_rgbeffects.xml"
    source_xml = read_xml_file(source_xml_path)

    print(os.getcwd())
    directory_path = "../../samples/Vendor Models"
    print(f"Scanning directory: {directory_path}")
    vendor_models = load_xmodel_files(directory_path)


    # models_xml = extract_models(source_xml_path)
    parsed_models = parse_models(source_xml, vendor_models)
    # dump_model_keys_and_values(models[0])

    #print_model_categories(parsed_models)
    #print(parsed_models[0])
    #print_unknown_model_categories(parsed_models)

    parsed_groups = parse_groups(source_xml)
    for group in parsed_groups:
        group_type = get_group_type(group, parsed_models)
        if group_type is None:
            group_type = 'G:Unknown'
        group['attributes']['GroupType'] = group_type

    #dump_group_keys_and_values(parsed_groups[0])
    print_group_types(parsed_groups, False)

    print(parsed_models[0])
    print(parsed_groups[0])
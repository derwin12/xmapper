import xml.etree.ElementTree as ET
import unittest
from classify import classify_model
import json
import os
from data_types import MODEL_TYPES
from views import extract_models

CACHE_FILE = "model_classifications.json"

xml_data = '''
  <models>
    <model DisplayAs="Candy Canes" StringType="RGB Nodes" StartSide="B" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm3="1" name="Candy Canes" parm2="18" Controller="No Controller" LayoutGroup="Default" parm1="1" WorldPosX="486.4577" WorldPosY="379.9518" WorldPosZ="0.0000" X2="32.963867" Y2="0.000031" Z2="0.000000" RotateX="0.00000000" Height="0.868422" Angle="0" versionNumber="7" StartChannel="151">
      <ControllerConnection Protocol="ws2811"/>
    </model>
    <model StringType="RGB Nodes" StartSide="B" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm2="50" parm3="1" name="Tree" parm1="16" DisplayAs="Tree 360" Controller="No Controller" LayoutGroup="Default" WorldPosX="768.6085" WorldPosY="614.2108" WorldPosZ="0.0000" ScaleX="0.9214" ScaleY="0.7628" ScaleZ="0.9214" RotateX="0.00000000" RotateY="0.00000000" RotateZ="0.00000000" versionNumber="7" StartChannel="5299">
      <ControllerConnection Protocol="ws2811"/>
    </model>
    <model DisplayAs="Arches" StringType="RGB Nodes" StartSide="B" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm1="1" parm2="50" parm3="1" name="Arches" Controller="No Controller" LayoutGroup="Default" WorldPosX="103.0362" WorldPosY="601.1566" WorldPosZ="0.0000" X2="122.313232" Y2="-5.204773" Z2="0.000000" RotateX="0.00000000" Height="1.000000" Angle="0" versionNumber="7" StartChannel="1">
      <ControllerConnection Protocol="ws2811"/>
    </model>
    <model StringType="RGB Nodes" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm2="50" parm3="1" name="Matrix" StartSide="T" DisplayAs="Horiz Matrix" parm1="16" Controller="No Controller" LayoutGroup="Default" WorldPosX="434.9277" WorldPosY="624.8735" WorldPosZ="0.0000" ScaleX="3.8029" ScaleY="4.7342" ScaleZ="0.0000" RotateX="0.00000000" RotateY="0.00000000" RotateZ="0.00000000" versionNumber="7" StartChannel="499">
      <ControllerConnection Protocol="ws2811"/>
    </model>
    <model DisplayAs="Icicles" StringType="RGB Nodes" StartSide="B" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm1="1" parm3="1" name="Icicles" parm2="80" DropPattern="3,4,5,4" Controller="No Controller" LayoutGroup="Default" WorldPosX="234.8916" WorldPosY="425.9277" WorldPosZ="0.0000" X2="185.638489" Y2="5.204803" Z2="0.000000" RotateX="0.00000000" Height="-0.500000" Shear="0.000000" versionNumber="7" StartChannel="259">
      <ControllerConnection Protocol="ws2811"/>
    </model>
    <model DisplayAs="Candy Canes" StringType="RGB Nodes" StartSide="B" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm3="1" name="Candy Canes 2" parm2="18" Controller="No Controller" LayoutGroup="Default" parm1="1" WorldPosX="559.3253" WorldPosY="497.0602" WorldPosZ="0.0000" X2="85.879456" Y2="1.734924" Z2="0.000000" RotateX="0.00000000" Height="1.000000" Angle="0" versionNumber="7" StartChannel="205">
      <ControllerConnection Protocol="ws2811"/>
    </model>
    <model StringType="RGB Nodes" Dir="L" Antialias="1" PixelSize="2" Transparency="0" parm2="50" parm3="1" name="Matrix-2" StartSide="T" DisplayAs="Horiz Matrix" parm1="16" Controller="No Controller" LayoutGroup="Default" Description="T:Matrix_Column" WorldPosX="108.5121" WorldPosY="423.5904" WorldPosZ="0.0000" ScaleX="0.7395" ScaleY="7.4488" ScaleZ="0.0204" RotateX="0.00000000" RotateY="0.00000000" RotateZ="0.00000000" versionNumber="7" StartChannel="2899">
      <ControllerConnection Protocol="ws2811"/>
    </model>
  </models>
'''

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
        controller = model.find("ControllerConnection")
        if controller is not None:
            model_data["ControllerProtocol"] = controller.get("Protocol")  # Store controller protocol

        model_data["ModelType"] = classify_model(model_data, cache)  # Add model classification
        models.append(model_data)

    save_cache(cache)
    return models

def print_model_categories(models):
    for model in models:
        print(f"Model Name: {model['name']}, DisplayAs: {model['DisplayAs']}, Category: {model['ModelType']}")

def print_unknown_model_categories(models):
    print("\nUnknown Models:")
    for model in models:
        if 'ModelType' in model:
            if( model['ModelType'] == "Unknown" ):
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


class TestParseModels(unittest.TestCase):
    def test_parse_models(self):
        models = parse_models(xml_data)
        self.assertEqual(len(models), 7)

        # Test first model
        self.assertEqual(models[0]["name"], "Candy Canes")
        self.assertEqual(models[0]["ModelType"], "T:CandyCane")

        # Test second model
        self.assertEqual(models[1]["name"], "Tree")
        self.assertEqual(models[1]["ModelType"], "T:Tree")

# Read and parse the XML file
def read_xml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()
    return xml_content

if __name__ == "__main__":
    import sys

    if "--test" in sys.argv:
        unittest.main()

    source_xml_path = "c:/users/Daryl/PycharmProjects/xmapper/samples/simple/source/xlights_rgbeffects.xml"

    models_xml = read_xml_file(source_xml_path)
    #models_xml = extract_models(source_xml_path)
    models = parse_models(models_xml)
    #dump_model_keys_and_values(models[0])

    print_unknown_model_categories(models_xml)





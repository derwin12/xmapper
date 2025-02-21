import os
import xml.etree.ElementTree as ET

def parse_xmodel(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract main model attributes
    model_data = {key: root.get(key, "") for key in root.keys()}
    model_data["submodels"] = []

    # Extract submodel data
    for submodel in root.findall("subModel"):
        submodel_data = {key: submodel.get(key, "") for key in submodel.keys()}
        model_data["submodels"].append(submodel_data)

    return model_data

def load_xmodel_files(directory):
    xmodel_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".xmodel"):
            file_path = os.path.join(directory, filename)
            model_name = os.path.splitext(filename)[0]
            xmodel_data[model_name] = parse_xmodel(file_path)
    return xmodel_data


# ======= Run the Script =======
if __name__ == "__main__":
    # Change this path to the directory where your .xmodel files are stored
    directory_path = "../../samples/Vendor Models"

    print(f"Scanning directory: {directory_path}")

    model_structure = load_xmodel_files(directory_path)

    # Print extracted models in a readable format
    if model_structure:
        print("\nExtracted Model Data:")
        for name, data in model_structure.items():
            print(f"Model: {name}")
            print(f"Attributes: {data}")
            print("Submodels:")
            for sub in data["submodels"]:
                print(f"  {sub}")
    else:
        print("No valid .xmodel files found.")

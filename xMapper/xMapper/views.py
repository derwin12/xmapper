from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import os
from flask import render_template

def home(request):
    if request.method == "POST":
        source_xml_path = "c:/users/Daryl/PycharmProjects/xmapper/samples/simple/source/xlights_rgbeffects.xml"
        target_xml_path = "c:/users/Daryl/PycharmProjects/xmapper/samples/simple/target/xlights_rgbeffects.xml"

        source_models = extract_models(source_xml_path)
        target_models = extract_models(target_xml_path)
        print(source_models)
        print(target_models)

        mapped_models = get_mapped_models(source_models, target_models)
        print(mapped_models)

        formatted_res = format_result(mapped_models)
        return render(request, "result.html", {"result": source_models, "result2": target_models, "mapped": mapped_models, "res":formatted_res })  # Pass result to template

    return render(request, "home.html")  # Show initial page


def get_mapped_models(source_models, target_models):
    """Finds models that exist in both source and target lists."""
    source_set = {model["DisplayAs"] for model in source_models}
    target_set = {model["DisplayAs"] for model in target_models}

    model_list = []
    for model in source_models:
        model_list.append(f"{model["DisplayAs"]}")

    mapped = []
    for model in source_models:
        if model["DisplayAs"] in target_set:
            target_model = next(target for target in target_models if target["DisplayAs"] == model["DisplayAs"])
            mapped.append(f"[{model['DisplayAs']},{model['DisplayAs']}]")

    return [model_list, mapped]


def extract_models(xml_file):
    """Reads an XML file and extracts model details including DisplayAs and name."""
    try:
        tree = ET.parse(xml_file)  # Parse the XML file
        root = tree.getroot()

        models = []

        # Iterate over all 'model' elements and extract attributes
        for model in root.findall(".//model"):
            model_data = {
                "name": model.get("name"),
                "DisplayAs": model.get("DisplayAs")
            }
            models.append(model_data)

        return models
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return []

def format_result(result):
        first_list = result[0]
        second_list = result[1]

        # Prepare the final output list
        output = []

        # Add each item from the first list
        for item in first_list:
            output.append(item)

        # Add each pair from the second list (removing the brackets and splitting by comma)
        for pair in second_list:
            # Clean up the brackets and split the string
            cleaned_pair = pair.strip('[]').split(',')
            output.append(f"{cleaned_pair[0]}\t{cleaned_pair[1]}")

        return '\n'.join(output)

import os

from xMapper.xMapper import mapping
from xMapper.xMapper.classify_groups import get_group_type
from xMapper.xMapper.custom_models import load_xmodel_files
from xMapper.xMapper.parse import parse_models
from xMapper.xMapper.parse_groups import parse_groups, print_group_types
from xMapper.xMapper.utils import read_xml_file

print(os.getcwd())
source_xml_path = 'c:/users/Daryl/PycharmProjects/xmapper/samples/simple/source/v1/xlights_rgbeffects.xml'
# source_xml_path = "F:/ShowFolderQA/xlights_rgbeffects.xml"
source_xml = read_xml_file(source_xml_path)

#print(os.getcwd())
directory_path = "../../samples/Vendor Models"
#print(f"Scanning directory: {directory_path}")
vendor_models = load_xmodel_files(directory_path)

# models_xml = extract_models(source_xml_path)
src_parsed_models = parse_models(source_xml, vendor_models)
# dump_model_keys_and_values(models[0])

# print_model_categories(parsed_models)
# print(parsed_models[0])
# print_unknown_model_categories(parsed_models)

src_parsed_groups = parse_groups(source_xml)
for group in src_parsed_groups:
    group_type = get_group_type(group, src_parsed_models)
    if group_type is None:
        group_type = 'G:Unknown'
    group['attributes']['GroupType'] = group_type

#print_group_types(src_parsed_groups, False)

print(src_parsed_models[0])
print(src_parsed_groups[0])

########################################
vendor_xml_path = "F:/ShowFolderQA/xlights_rgbeffects.xml"
vendor_xml = read_xml_file(vendor_xml_path)

vendor_parsed_models = parse_models(vendor_xml, vendor_models)

vendor_parsed_groups = parse_groups(vendor_xml)
for group in vendor_parsed_groups:
    group_type = get_group_type(group, vendor_parsed_models)
    if group_type is None:
        group_type = 'G:Unknown'
    group['attributes']['GroupType'] = group_type

#print_group_types(vendor_parsed_groups, False)

print(vendor_parsed_models[0])
print(vendor_parsed_groups[0])

mapping.mapping(src_parsed_models, src_parsed_groups, vendor_parsed_models, vendor_parsed_groups)
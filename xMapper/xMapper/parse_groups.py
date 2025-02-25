import xml.etree.ElementTree as ET
from utils import read_xml_file

import os

xml_data ='''
<xrgb>
  <models>
    <model DisplayAs="Custom" StartSide="B" Dir="L" parm3="1" CustomModel=",,,,,,,,,,,,,,,,,,,,43,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,9,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,42,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,10,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,41,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,11,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,44,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,8,,,,,,,,,,,,,,,,,,,,,;,,,,,,,40,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,12,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,39,,,,,,,,,,,,,,,,,,,45,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,7,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,13,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;38,,,,,37,,,,,,,,,,,,,,,,,,,,46,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,6,,,,,,,,,,,,,,,,,,,,15,,,,,14;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,50,,,,,,,2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,36,,,,,,,,,,,,,,,,,,,47,,,,,,,,,,,,,1,,,,,,,,,,,,,5,,,,,,,,,,,,,,,,,,,,16,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,48,,,,,,,,,,,,,3,,,,,4,,,,,,,,,,,,,,,,,,,,,17,,,,,,,,,,,,;,,,,,,,,,,,,35,,,,,,,,,,,,,,,,,,,,,,,,,,,49,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,33,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,19,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,34,,,,,,,,,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,18,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,20,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,31,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,21,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,30,,,,29,,,,,,,,,,,,,,,,,,,,23,,,,22,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,28,,,,,,,,,,,,24,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,27,,,,,25,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,26,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,," parm1="85" parm2="41" Depth="1" StringType="RGB Nodes" Transparency="0" ModelBrightness="" Antialias="1" StrandNames="" NodeNames="" PixelCount="50" PixelType="12mm bullet" PixelSpacing="" LayoutGroup="Default" name="Roof Bat Mega-4" PixelSize="3" WorldPosX="793.0977" WorldPosY="330.6117" WorldPosZ="0.0000" ScaleX="0.6039" ScaleY="0.4390" ScaleZ="0.6039" RotateX="-0.00000000" RotateY="-0.00000000" RotateZ="23.00000000" Locked="1" versionNumber="5" StartChannel="&gt;Roof Bat Mega-3:1">
      <ControllerConnection/>
    </model>
  </models>
  <effects version="0006"/>
  <palettes/>
  <modelGroups>
    <modelGroup selected="0" name="Arches" GridSize="400" layout="minimalGrid" models="Arch-1,Arch-2,Arch-3,Arch-4,Arch-5,Arch-6,Arch-7,Arch-8,Arch-9" LayoutGroup="Default">
      <ControllerConnection/>
    </modelGroup>
    <modelGroup selected="0" name="Roof Upper" GridSize="400" layout="minimalGrid" models="Roof Peak,Gutter Top,Icicles 1,Icicles 2,Icicles 3,Icicles 4" LayoutGroup="Default"/>
    <modelGroup selected="0" name="Roof Lower" models="Gutter Bottom,Icicles 5,Icicles 6,Icicles 7,Icicles 8,Icicles 9,Roof Lower 1,Roof Lower 2,Roof Lower 3" GridSize="400" layout="minimalGrid" LayoutGroup="Default"/>
    <modelGroup selected="0" name="Snowflakes" GridSize="400" layout="minimalGrid" models="Column Spider-1,Column Spider-2,Roof Bat-1,Roof Spider-2,Roof Bat Mega-3,Roof Bat Mega-4,Roof Spider-5,Roof Bat-6,Roof Bat Mega-7,Roof Bat-8,Web-1,Web-2" LayoutGroup="Default">
      <ControllerConnection/>
    </modelGroup>
    <modelGroup selected="0" name="Stars on Trees" models="Mini Tree Star-1,Mini Tree Star-2,Mini Tree Star-3,Mini Tree Star-4,Mini Tree Star-5,Mini Tree Star-6,Mini Tree Star-7,Mini Tree Star-8" GridSize="400" layout="minimalGrid" LayoutGroup="Default">
      <ControllerConnection/>
    </modelGroup>
    <modelGroup selected="0" name="Wreath Rings" models="Wreath/Inner,Wreath/Middle,Wreath/Outer" GridSize="400" layout="minimalGrid" LayoutGroup="Default">
      <ControllerConnection/>
    </modelGroup>
    <modelGroup selected="0" GridSize="400" layout="minimalGrid" name="ALL Stars" models="Megatree Star,Mini Tree Star-1,Mini Tree Star-2,Mini Tree Star-3,Mini Tree Star-4,Mini Tree Star-5,Mini Tree Star-6,Mini Tree Star-7,Mini Tree Star-8" LayoutGroup="Default"/>
    <modelGroup selected="0" name="ALL House Decorations" GridSize="400" layout="minimalGrid" models="Cat,Door Ghost,46 MegaSpinner-1,46 MegaSpinner-2,Web-1,Web-2,Spinner 1,Spinner 2,Spinner 3,Spinner 4,Roof Bat-1,Roof Spider-2,Roof Bat Mega-3,Roof Bat Mega-4,Roof Spider-5,Roof Bat-6,Roof Bat Mega-7,Roof Bat-8,Wreath,Column Spider-1,Column Spider-2" LayoutGroup="Default">
      <ControllerConnection/>
    </modelGroup>
    <modelGroup selected="0" name="Cats" layout="minimalGrid" GridSize="400" LayoutGroup="Default" models="Cat"/>
  </modelGroups>
  <layoutGroups/>
  <perspectives current="Theater">
    <perspective name="Theater" settings="layout2|name=ModelPreview;caption=Model Preview;state=6293501;dir=1;layer=0;row=0;pos=3;prop=100000;bestw=250;besth=250;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=1514;floaty=558;floatw=401;floath=463|name=HousePreview;caption=House Preview;state=6293501;dir=1;layer=0;row=0;pos=1;prop=100000;bestw=250;besth=250;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=1912;floaty=-8;floatw=1936;floath=1096|name=EffectAssist;caption=Effect Assist;state=2099198;dir=4;layer=0;row=1;pos=0;prop=158290;bestw=250;besth=250;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=299;floaty=600;floatw=675;floath=1089|name=DisplayElements;caption=Display Elements;state=6293500;dir=1;layer=1;row=0;pos=1;prop=100000;bestw=600;besth=400;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=723;floaty=226;floatw=496;floath=333|name=Perspectives;caption=Perspectives;state=2099196;dir=1;layer=1;row=0;pos=3;prop=41710;bestw=160;besth=130;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=1788;floaty=216;floatw=280;floath=325|name=Effect;caption=Effect Settings;state=2099196;dir=4;layer=2;row=0;pos=0;prop=100000;bestw=386;besth=703;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-175;floaty=365;floatw=552;floath=624|name=SelectEffect;caption=Select Effects;state=2099198;dir=4;layer=1;row=0;pos=5;prop=100000;bestw=359;besth=233;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=EffectDropper;caption=Effects;state=2099198;dir=1;layer=0;row=0;pos=0;prop=100000;bestw=1100;besth=550;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=ValueCurveDropper;caption=Value Curves;state=2099198;dir=1;layer=0;row=0;pos=1;prop=100000;bestw=40;besth=40;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-865;floaty=0;floatw=448;floath=232|name=ColourDropper;caption=Colours;state=2099198;dir=1;layer=0;row=0;pos=1;prop=100000;bestw=40;besth=40;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-433;floaty=1;floatw=429;floath=299|name=Jukebox;caption=Jukebox;state=2099198;dir=1;layer=0;row=0;pos=4;prop=100000;bestw=590;besth=1180;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=Color;caption=Color;state=2099196;dir=1;layer=1;row=0;pos=0;prop=100000;bestw=256;besth=303;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-84;floaty=171;floatw=505;floath=342|name=LayerTiming;caption=Layer Blending;state=2099196;dir=1;layer=1;row=0;pos=2;prop=100000;bestw=240;besth=215;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=595;floaty=132;floatw=398;floath=340|name=LayerSettings;caption=Layer Settings;state=2099196;dir=4;layer=2;row=0;pos=1;prop=100000;bestw=267;besth=385;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-27;floaty=702;floatw=533;floath=488|name=SequenceVideo;caption=Sequence Video;state=2099199;dir=4;layer=0;row=0;pos=0;prop=100000;bestw=280;besth=169;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=26;floaty=26;floatw=296;floath=208|name=Main Sequencer;caption=Main Sequencer;state=768;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=118;besth=50;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|dock_size(5,0,0)=120|dock_size(1,1,0)=136|dock_size(4,2,0)=388|" version="2.0"/>
  </perspectives>
  <settings>
  </settings>
  <view_objects>
    <view_object DisplayAs="Gridlines" LayoutGroup="Default" name="Gridlines" GridLineSpacing="50" GridWidth="2000.0" GridHeight="1000.0" Active="1" WorldPosX="0.0000" WorldPosY="0.0000" WorldPosZ="0.0000" ScaleX="1.0000" ScaleY="1.0000" ScaleZ="1.0000" RotateX="-90.00000000" RotateY="-0.00000000" RotateZ="0.00000000" versionNumber="5"/>
  </view_objects>
  <colors>
  </colors>
  <Viewpoints/>
</xrgb>
'''

def print_group_types(groups, show_unknown):
    print("Groups...")
    for group in groups:
        if group['attributes']['GroupType'] != 'G:Unknown' or show_unknown:
            print('Group:', group['attributes']['name'], group['attributes']['GroupType'], '** Made up of Models:', group['attributes']['models'])

def parse_groups(xml_string):
    root = ET.fromstring(xml_string)
    groups = []

    groups_parent = root.find("modelGroups")
    if groups_parent is None:
        raise ValueError("No <models> element found in XML")

    for model_group in groups_parent.findall("modelGroup"):
        #group_data = {attr: groups.get(attr) for attr in groups.attrib}  # Store attributes
        attributes = model_group.attrib
        if ('Active' in attributes):
            print("Skipping inactive ", attributes['name'])
            continue

        #print("Working on ....", attributes['name'])
        models = attributes.get("models", "").split(",") if attributes.get("models") else []

        #model_data["ModelType"] = classify_model(model_data, cache, vendor_models)  # Add model classification
        group_data = {
                "attributes": attributes,
                "models": models
        }
        groups.append(group_data)

    return groups

def dump_group_keys_and_values(groups):
    """
    Dumps all key-value pairs for a given model.

    Args:
        groups (dict): A dictionary representing a model.
    """
    print("Dumping group keys and values:")
    for key, value in groups.items():
        print(f"{key}: {value}")

# If group contains all of one model type then store as G:<modeltype>

if __name__ == "__main__":
    print(os.getcwd())
    source_xml_path = '../../samples/simple/source/v1/xlights_rgbeffects.xml'
    #source_xml_path = "F:/ShowFolderQA/xlights_rgbeffects.xml"

    groups_xml = read_xml_file(source_xml_path)

    parsed_groups = parse_groups(groups_xml)
    dump_group_keys_and_values(parsed_groups[0])

    for group in parsed_groups:
        print(group)
import unittest
from classify import close_match
from parse import parse_models

xml_data = '''
<xrgb>
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
</xrgb>
'''


class TestParseModels(unittest.TestCase):
    def test_parse_models(self):
        models = parse_models(xml_data)
        self.assertEqual(len(models), 7)

        # Test first model
        self.assertEqual(models[0]["name"], "Candy Canes")
        self.assertEqual(models[0]["ModelType"], "T:CandyCane")

        # Test second model
        self.assertEqual(models[1]["name"], "Tree")
        self.assertEqual(models[1]["ModelType"], "T:Mega_Tree")


class TestCloseMatch(unittest.TestCase):
    def test_exact_match_in_name(self):
        """Test when key matches name exactly."""
        result = close_match("test", "test", "display", "desc")
        self.assertTrue(result)

    def test_match_with_spaces(self):
        """Test when key matches name with spaces."""
        result = close_match("testkey", "test key", "display", "desc")
        self.assertTrue(result)

    def test_match_with_underscores(self):
        """Test when key matches display_as with underscores."""
        result = close_match("mykey", "name", "my_key", "desc")
        self.assertTrue(result)

    def test_match_in_description(self):
        """Test when key matches part of description."""
        result = close_match("info", "name", "display", "some info here")
        self.assertTrue(result)

    def test_case_insensitivity(self):
        """Test case insensitivity in matching."""
        result = close_match("TEST", "test", "display", "desc")
        self.assertTrue(result)

    def test_no_match(self):
        """Test when key doesn't match any field."""
        result = close_match("key", "name", "display", "description")
        self.assertFalse(result)

    def test_empty_key(self):
        """Test when key is empty."""
        result = close_match("", "name", "display", "description")
        self.assertTrue(result)  # Empty string is in everything after preprocessing

    def test_all_fields_with_spaces_and_underscores(self):
        """Test complex case with spaces and underscores in all fields."""
        result = close_match("abc", "a b c", "a_b_c", "abc_def")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

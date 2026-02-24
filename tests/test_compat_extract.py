"""Unit tests for idfkit.compat._extract (AST extraction)."""

from __future__ import annotations

from idfkit.compat._extract import extract_literals
from idfkit.compat._models import LiteralKind


class TestExtractAddCalls:
    """Tests for extracting .add() call patterns."""

    def test_add_simple(self) -> None:
        source = 'doc.add("Zone", "MyZone")\n'
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 1
        assert obj_types[0].value == "Zone"
        assert obj_types[0].line == 1

    def test_add_with_kwargs(self) -> None:
        source = 'doc.add("Material", "Mat1", roughness="MediumSmooth", thickness=0.1)\n'
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        choices = [lit for lit in literals if lit.kind == LiteralKind.CHOICE_VALUE]

        assert len(obj_types) == 1
        assert obj_types[0].value == "Material"

        assert len(choices) == 1
        assert choices[0].value == "MediumSmooth"
        assert choices[0].obj_type == "Material"
        assert choices[0].field_name == "roughness"

    def test_add_with_dict_arg(self) -> None:
        source = 'doc.add("Material", "Mat1", {"roughness": "Smooth", "thickness": 0.1})\n'
        literals = extract_literals(source)
        choices = [lit for lit in literals if lit.kind == LiteralKind.CHOICE_VALUE]

        assert len(choices) == 1
        assert choices[0].value == "Smooth"
        assert choices[0].obj_type == "Material"
        assert choices[0].field_name == "roughness"

    def test_add_with_dict_no_name(self) -> None:
        source = 'doc.add("SimulationControl", {"run_simulation_for_sizing_periods": "Yes"})\n'
        literals = extract_literals(source)
        choices = [lit for lit in literals if lit.kind == LiteralKind.CHOICE_VALUE]

        assert len(choices) == 1
        assert choices[0].value == "Yes"
        assert choices[0].field_name == "run_simulation_for_sizing_periods"

    def test_add_no_string_arg(self) -> None:
        source = "my_set.add(42)\n"
        literals = extract_literals(source)
        assert len(literals) == 0

    def test_add_dynamic_string_ignored(self) -> None:
        source = 'obj_type = "Zone"\ndoc.add(obj_type)\n'
        literals = extract_literals(source)
        # Only constant strings should be extracted
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 0

    def test_multiple_add_calls(self) -> None:
        source = """
doc.add("Zone", "Zone1")
doc.add("Material", "Mat1", roughness="Smooth")
doc.add("Construction", "Con1", outside_layer="Mat1")
"""
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 3
        assert {lit.value for lit in obj_types} == {"Zone", "Material", "Construction"}

    def test_add_preserves_line_numbers(self) -> None:
        source = """# Line 1
# Line 2
doc.add("Zone", "Z1")
# Line 4
doc.add("Material", "M1")
"""
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert obj_types[0].line == 3
        assert obj_types[1].line == 5

    def test_add_with_colon_object_type(self) -> None:
        source = 'doc.add("BuildingSurface:Detailed", "Wall1")\n'
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 1
        assert obj_types[0].value == "BuildingSurface:Detailed"


class TestExtractSubscripts:
    """Tests for extracting subscript access patterns."""

    def test_subscript_with_idfkit_import(self) -> None:
        source = """from idfkit import load_idf
zones = doc["Zone"]
"""
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 1
        assert obj_types[0].value == "Zone"

    def test_subscript_without_idfkit_import(self) -> None:
        source = 'zones = doc["Zone"]\n'
        literals = extract_literals(source)
        # No idfkit import, so subscripts should not be extracted
        assert len(literals) == 0

    def test_subscript_with_import_idfkit(self) -> None:
        source = """import idfkit
zones = model["Zone"]
"""
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 1
        assert obj_types[0].value == "Zone"

    def test_subscript_integer_ignored(self) -> None:
        source = """from idfkit import load_idf
x = items[0]
"""
        literals = extract_literals(source)
        assert len(literals) == 0


class TestExtractMixed:
    """Tests for mixed patterns."""

    def test_add_and_subscript(self) -> None:
        source = """from idfkit import new_document
doc = new_document()
doc.add("Zone", "Office")
zones = doc["Zone"]
"""
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        # Two references to "Zone": one from .add(), one from subscript
        assert len(obj_types) == 2
        values = [lit.value for lit in obj_types]
        assert values.count("Zone") == 2

    def test_fstring_ignored(self) -> None:
        source = """from idfkit import new_document
name = "Zone"
doc.add(f"My{name}", "Z1")
"""
        literals = extract_literals(source)
        obj_types = [lit for lit in literals if lit.kind == LiteralKind.OBJECT_TYPE]
        assert len(obj_types) == 0

    def test_empty_file(self) -> None:
        assert extract_literals("") == []

    def test_no_relevant_code(self) -> None:
        source = 'x = 1\ny = "hello"\nprint(x + y)\n'
        assert extract_literals(source) == []

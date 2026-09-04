from __future__ import annotations

from idfkit import (
    FieldDescription,
    IDFDocument,
    IDFObject,
    ObjectDescription,
    ValidationError,
    ValidationResult,
)
from idfkit.simulation import simulate

doc: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
result: ValidationResult = ...  # type: ignore[assignment]
v: ValidationResult = ...  # type: ignore[assignment]
err: ValidationError = ...  # type: ignore[assignment]
warn: ValidationError = ...  # type: ignore[assignment]
issues: list[ValidationError] = ...  # type: ignore[assignment]
issue: ValidationError = ...  # type: ignore[assignment]
desc: ObjectDescription = ...  # type: ignore[assignment]
field: FieldDescription = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import load_idf, validate_document, get_schema

doc = load_idf("building.idf")
result = validate_document(doc)
if not result.is_valid:
    for err in result.errors:
        print(err)
# --8<-- [end:quickstart]


# --8<-- [start:schema-methods]
from idfkit import get_schema

schema = get_schema((25, 2, 0))

schema.get_object_schema("Zone")  # raw JSON-Schema dict
schema.get_field_names("Zone")  # Python-style field names
schema.get_required_fields("Zone")
schema.get_field_type("Zone", "x_origin")  # "real", "alpha", "choice", ...
schema.get_field_default("Material", "thickness")
schema.get_group("HVACTemplate:Zone:VAV")  # "HVAC Templates"
schema.has_name("Zone")  # True
schema.is_extensible("BuildingSurface:Detailed")
schema.is_reference_field("Zone", "Floor Area")
schema.get_field_object_list("BuildingSurface:Detailed", "zone_name")
# ['ZoneNames']  — what reference list this field accepts
schema.get_types_providing_reference("ZoneNames")
# ['Zone', 'ZoneList'] — what types satisfy that reference
schema.object_types  # every registered type
"Zone" in schema  # bool
# --8<-- [end:schema-methods]


# --8<-- [start:validate]
from idfkit import validate_document

result = validate_document(doc)
print(result)  # human summary

# Drill in
for err in result.errors:
    print(err.code, err.obj_type, err.obj_name, err.field, err.message)

for warn in result.warnings:
    print(warn)
# --8<-- [end:validate]


# --8<-- [start:validate-gate]
if not validate_document(doc):
    raise SystemExit("Refusing to simulate an invalid model")
# --8<-- [end:validate-gate]


# --8<-- [start:scope]
# Skip range checks during a parametric sweep where you know values are temporarily out of bounds
result = validate_document(doc, check_ranges=False)

# Validate only materials and constructions
result = validate_document(doc, object_types=["Material", "Construction"])

# Skip reference integrity (e.g. before you've finished adding referenced objects)
result = validate_document(doc, check_references=False)
# --8<-- [end:scope]


# --8<-- [start:validate-object]
from idfkit import get_schema, validate_object

zone = doc["Zone"]["Office"]
schema = get_schema(doc.version)  # validate_object requires a schema
issues = validate_object(zone, schema)
for issue in issues:
    print(issue)
# --8<-- [end:validate-object]


# --8<-- [start:introspect]
desc = doc.describe("Zone")
print(desc.memo)  # human description from EnergyPlus docs
for field in desc.fields:
    print(field.name, field.field_type, field.required, field.default, field.minimum, field.maximum)
# --8<-- [end:introspect]


# --8<-- [start:mistake-validate-good]
v = validate_document(doc)
if not v.is_valid:
    for err in v.errors:
        print(err)
    raise SystemExit("Fix errors before simulating")
result = simulate(doc, "weather.epw")
# --8<-- [end:mistake-validate-good]


# --8<-- [start:mistake-schema-good]
if "fictional_field" in doc.schema.get_field_names("Zone"):
    zone.fictional_field = 1.0
# --8<-- [end:mistake-schema-good]


# --8<-- [start:mistake-version-good]
validate_document(doc)  # uses doc.schema automatically
# --8<-- [end:mistake-version-good]

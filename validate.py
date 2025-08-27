#!/usr/bin/env python3
import json
from pathlib import Path
import click
from jsonschema import Draft202012Validator, FormatChecker


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option("--schema", "schema_path", type=click.Path(exists=True, path_type=Path),
              default=Path("specs/address-register.schema.json"), show_default=True,
              help="Path to JSON Schema for address features")
@click.option("--schema-target", type=click.Choice(["collection", "feature", "properties"], case_sensitive=False),
              default="collection", show_default=True,
              help="What the input represents for validation")
def main(input_path: Path, schema_path: Path, schema_target: str):
    """Validate input against the schema.

    Targets:
    - collection: GeoJSON FeatureCollection with address features
    - feature: GeoJSON Feature with address properties and Point geometry
    - properties: properties object only (no geometry)
    """
    with schema_path.open() as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    with input_path.open() as f:
        data = json.load(f)

    errors = []
    if schema_target == "collection":
        if data.get("type") != "FeatureCollection":
            click.echo("Input is not a GeoJSON FeatureCollection", err=True)
            raise SystemExit(2)
        # Validate entire collection against $defs.FeatureCollection
        for e in validator.iter_errors(data):
            errors.append(e.message)
    elif schema_target == "feature":
        if data.get("type") != "Feature":
            click.echo("Input is not a GeoJSON Feature", err=True)
            raise SystemExit(2)
        # Validate feature by pointing into $defs.Feature via $ref root
        # The root schema is FeatureCollection, but it has $defs.Feature
        feature_schema = schema["$defs"]["Feature"]
        feature_validator = Draft202012Validator(feature_schema, format_checker=FormatChecker())
        for e in feature_validator.iter_errors(data):
            errors.append(e.message)
    else:  # properties
        props_schema = schema["$defs"]["AddressProperties"]
        props_validator = Draft202012Validator(props_schema, format_checker=FormatChecker())
        for e in props_validator.iter_errors(data):
            errors.append(e.message)

    if errors:
        click.echo("Validation failed:\n" + "\n".join(f"- {msg}" for msg in errors), err=True)
        raise SystemExit(1)
    click.echo("Validation OK")


if __name__ == "__main__":
    main()

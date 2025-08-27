#!/usr/bin/env python3
import json
from pathlib import Path
import click
from jsonschema import Draft7Validator


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option("--schema", "schema_path", type=click.Path(exists=True, path_type=Path),
              default=Path("specs/address-register.schema.json"), show_default=True,
              help="Path to JSON Schema for address features")
def main(input_path: Path, schema_path: Path):
    """Validate a GeoJSON FeatureCollection of address features against the schema."""
    with schema_path.open() as f:
        schema = json.load(f)
    validator = Draft7Validator(schema)

    with input_path.open() as f:
        data = json.load(f)

    if data.get("type") != "FeatureCollection":
        click.echo("Input is not a GeoJSON FeatureCollection", err=True)
        raise SystemExit(2)

    errors = []
    for i, feat in enumerate(data.get("features", [])):
        for e in validator.iter_errors(feat.get("properties", {})):
            errors.append(f"feature[{i}] property error: {e.message}")
        # Validate geometry is present and a Point
        geom = feat.get("geometry")
        if not geom or geom.get("type") != "Point":
            errors.append(f"feature[{i}] geometry must be a Point")

    if errors:
        click.echo("Validation failed:\n" + "\n".join(errors), err=True)
        raise SystemExit(1)
    click.echo("Validation OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path
import click


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
def main(input_path: Path):
    """Basic QC checks: duplicate house numbers per street_id within a ULB."""
    with input_path.open() as f:
        data = json.load(f)

    seen = defaultdict(set)
    dups = []
    for i, feat in enumerate(data.get("features", [])):
        props = feat.get("properties", {})
        ulb = props.get("ulb_lgd")
        street_id = props.get("street_id", props.get("street_name"))
        house_no = props.get("house_number")
        key = (ulb, street_id)
        if (house_no in seen[key]):
            dups.append((i, ulb, street_id, house_no))
        else:
            seen[key].add(house_no)

    if dups:
        click.echo("Duplicate house numbers found:")
        for i, ulb, street_id, house_no in dups:
            click.echo(f" - feature[{i}] ULB={ulb} street={street_id} house={house_no}")
        raise SystemExit(1)
    click.echo("QC OK: no duplicates per street")


if __name__ == "__main__":
    main()

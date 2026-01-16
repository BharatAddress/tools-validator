![CI](https://github.com/BharatAddress/tools-validator/actions/workflows/ci.yml/badge.svg)
![CodeQL](https://github.com/BharatAddress/tools-validator/actions/workflows/codeql.yml/badge.svg)

# Bharat Address Validator (CLI)

CLI to validate CSV or GeoJSON against the Bharat Address schema (JSON Schema draft 2020-12) and run basic QC rules.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python validate.py data/sample.geojson --schema specs/address-register.schema.json --schema-target collection
python check_qc.py data/sample.geojson
```

## Usage notes
- The authoritative schema lives in `BharatAddress/specs`; this repo includes a synced copy for CI examples.
- The validator supports three targets via `--schema-target`: `collection`, `feature`, or `properties`.
- QC checks are intentionally small and can be extended for local rules.

## Repo layout
- `validate.py`: schema validation entrypoint.
- `check_qc.py`: basic QC checks.
- `specs/`: synced schema copy for tests.

## Who should use this
- Data teams validating pilot datasets.
- Tool builders integrating schema checks.

## Links
- Specs: https://github.com/BharatAddress/specs
- Docs: https://bharataddress.github.io

## License
See `LICENSE`.

## Contributor Guide
- Central guidelines: https://github.com/BharatAddress/.github/blob/main/AGENTS.md

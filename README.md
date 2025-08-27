# Bharat Address Validator (CLI)

CLI to validate CSV or GeoJSON against the Bharat Address schema and run basic QC rules.

Usage:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python validate.py data/sample.geojson --schema specs/address-register.schema.json
python check_qc.py data/sample.geojson
```

Notes:
- The authoritative schema lives in the `specs` repo; this repo includes a synced copy for CI examples.

#!/usr/bin/env python3
import csv
import io
import time
from os import getenv
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile
import json

db_zip_path = Path(getenv("DB_ZIP", "GeoLite2-Country-CSV.zip"))
rules_path = Path(getenv("RULES_PATH", Path(__file__).parent.parent / "by-country"))

action_map = {
    "allow": "Allow access to networks in {}",
    "deny": "Deny access to networks in {}",
    "ask": "Ask before accessing networks in {}",
}


dbs = {}

run_time = time.time()

with ZipFile(db_zip_path) as db_zip:
    for n in db_zip.namelist():
        for member in ["IPv4", "IPv6", "Locations-en"]:
            if n.endswith(f"{member}.csv"):
                print(f"Reading {n}...")
                with db_zip.open(n, "r") as f:
                    dbs[member] = list(csv.DictReader(io.TextIOWrapper(f)))
                break

geoname_mapping = {int(r["geoname_id"]): r for r in dbs["Locations-en"]}
if 0 not in geoname_mapping:
    geoname_mapping[0] = {"country_iso_code": "ZZ", "country_name": "Unknown"}

country_blocks = {}

for m in ["IPv4", "IPv6"]:
    for row in dbs[m]:
        geoname_id = 0 if row["geoname_id"] == "" else int(row["geoname_id"])
        country_blocks.setdefault(geoname_id, []).append(row["network"])

if rules_path.exists():
    rmtree(rules_path)
rules_path.mkdir()

for k, v in country_blocks.items():
    gm = geoname_mapping.get(k, geoname_mapping[0])
    cc = gm["country_iso_code"].lower() or f"{gm['continent_code'].lower()}-other"
    cn = gm["country_name"] or f"{gm['continent_name']} (Other)"
    for action, description_fmt in action_map.items():
        rule_file = f"{cc}-{action}.lsrules"
        rule = {
            "name": f"{cn} ({action.capitalize()})",
            "description": description_fmt.format(cn),
            "rules": [
                {
                    "action": action,
                    "process": "any",
                    "owner": "any",
                    "creationDate": 1670703966.0,
                    "modificationDate": run_time,
                    "remote-addresses": v,
                }
            ],
        }
        print(f"Writing {rule_file}...")
        with open(rules_path / rule_file, "w") as f:
            json.dump(rule, f, indent=4)

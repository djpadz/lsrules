#!/usr/bin/env python3

import sys
import time
from pathlib import Path


import yaml
import json

here = Path(__file__).parent
rule_root_path = here.parent

run_time = time.time()

for filename in sys.argv[1:]:
    p = Path(filename)
    with open(filename) as f:
        data = yaml.safe_load(f)
        rule_path = rule_root_path / data["path"]
        print(f"{filename} → ../{rule_path.relative_to(rule_root_path)}")
        rules = data["rules"].copy()
        for rule in rules:
            rule["creationDate"] = 1670609717.8541021
            rule["modificationDate"] = run_time
        ruleset = {
            "description": data["description"],
            "name": data["name"],
            "rules": rules,
        }
        with open(rule_path, "w") as f2:
            json.dump(ruleset, f2, indent=4)

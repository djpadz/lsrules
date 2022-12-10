#!/usr/bin/env python3
from os import getenv

import requests

GEOIP_CONFIG = getenv("GEOIP_CONFIG", "/usr/local/etc/GeoIP.conf")
DOWNLOAD_URL_FMT = (
    "https://download.maxmind.com/app/geoip_download?"
    "edition_id=GeoLite2-Country-CSV&license_key={}&suffix=zip"
)
OUTFILE = "GeoLite2-Country-CSV.zip"

license_key = None
with open(GEOIP_CONFIG, "r") as f:
    for line in f:
        if line.startswith("LicenseKey"):
            license_key = line.split()[1].strip()
            break
if license_key is None:
    raise ValueError("LicenseKey not found in GeoIP.conf")

url = DOWNLOAD_URL_FMT.format(license_key)
r = requests.get(url)
with open(OUTFILE, "wb") as f:
    f.write(r.content)
print(f"Downloaded to {OUTFILE}.")

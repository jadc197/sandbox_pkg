#!/usr/bin/env python3

import json
import urllib.request
from datetime import date, datetime, timezone

API_URL = "https://endoflife.date/api/python.json"


def main():
    with urllib.request.urlopen(API_URL, timeout=30) as response:
        releases = json.load(response)

    today = datetime.now(timezone.utc).date()

    supported = []

    for release in releases:
        eol = release.get("eol")

        if eol is False or eol is None:
            supported.append(release["cycle"])
            continue

        eol_date = date.fromisoformat(eol)

        if eol_date >= today:
            supported.append(release["cycle"])

    supported.sort(
        key=lambda version: tuple(map(int, version.split(".")))
    )

    print(json.dumps(supported, indent=2))


if __name__ == "__main__":
    main()
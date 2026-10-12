
import json
import urllib.request
from datetime import date, datetime, timezone


API_URL = "https://endoflife.date/api/python.json"


def get_non_eol_python_versions():
    """Return Python versions that have not yet reached EOL."""

    with urllib.request.urlopen(API_URL, timeout=30) as response:
        releases = json.load(response)

    today = datetime.now(timezone.utc).date()

    versions = []

    for release in releases:
        eol = release.get("eol")

        if eol is False or eol is None:
            versions.append(release["cycle"])
            continue

        eol_date = date.fromisoformat(eol)

        if eol_date >= today:
            versions.append(release["cycle"])

    versions.sort(
        key=lambda version: tuple(map(int, version.split(".")))
    )

    return versions


def main():
    """Print the resulting versions as JSON."""
    print(json.dumps(get_non_eol_python_versions(), indent=2))


if __name__ == "__main__":
    main()
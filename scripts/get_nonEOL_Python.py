import json
import urllib.request
from datetime import date, datetime, timezone

API_URL = "https://endoflife.date/api/python.json"


def get_python_releases():
    """Fetch Python release data from the endoflife.date API.

    Returns
    -------
    list[dict]
        Release records returned by the API.
    """
    with urllib.request.urlopen(API_URL, timeout=30) as response:
        return json.load(response)


def get_non_eol_python_versions(releases=None):
    """Return numerically sorted versions that have not reached EOL.

    Parameters
    ----------
    releases : list[dict] or None, optional
        Release records to process. Fetches the API data if None.

    Returns
    -------
    list[str]
        Versions that have not reached EOL, including releases with
        an unknown EOL status.
    """
    if releases is None:
        releases = get_python_releases()

    today = datetime.now(timezone.utc).date()
    versions = []

    for release in releases:
        eol = release.get("eol")

        if eol is False or eol is None or date.fromisoformat(eol) >= today:
            versions.append(release["cycle"])

    return sorted(
        versions,
        key=lambda version: tuple(map(int, version.split("."))),
    )


def main():
    """Print non-EOL Python versions as JSON."""
    print(json.dumps(get_non_eol_python_versions(), indent=2))


if __name__ == "__main__":
    main()

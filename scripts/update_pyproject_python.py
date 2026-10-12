#!/usr/bin/env python3

from datetime import date, datetime, timezone
from pathlib import Path

import tomlkit

from get_nonEOL_Python import get_non_eol_python_versions, get_python_releases


ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_FILE = ROOT / "pyproject.toml"


def update_pyproject():
    """Update Python compatibility metadata in pyproject.toml."""

    releases = get_python_releases()
    non_eol_versions = get_non_eol_python_versions()

    if not non_eol_versions:
        raise RuntimeError("No non-EOL Python versions were found.")

    today = datetime.now(timezone.utc).date()

    # Build a set of versions explicitly confirmed to be EOL.
    eol_versions = set()

    for release in releases:
        version = release["cycle"]
        eol = release.get("eol")

        if eol is False or eol is None:
            continue

        if date.fromisoformat(eol) < today:
            eol_versions.add(version)

    document = tomlkit.parse(PYPROJECT_FILE.read_text(encoding="utf-8"))
    project = document["project"]

    # Set the minimum required Python version.
    minimum_version = non_eol_versions[0]
    project["requires-python"] = f">={minimum_version}"

    # Remove classifiers only when the API explicitly confirms EOL.
    classifiers = project["classifiers"]

    project["classifiers"] = [
        classifier
        for classifier in classifiers
        if not (
            classifier.startswith("Programming Language :: Python :: ")
            and classifier.removeprefix(
                "Programming Language :: Python :: "
            ) in eol_versions
        )
    ]

    PYPROJECT_FILE.write_text(
        tomlkit.dumps(document),
        encoding="utf-8",
    )

    print(f"Updated requires-python to >={minimum_version}")
    print(f"Removed classifiers for EOL versions: {sorted(eol_versions)}")


if __name__ == "__main__":
    update_pyproject()
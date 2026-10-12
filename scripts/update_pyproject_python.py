#!/usr/bin/env python3

import json
import re
from pathlib import Path

import tomlkit


ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_FILE = ROOT / "pyproject.toml"
PYTHON_VERSIONS_FILE = ROOT / "non_eol_python.json"


def main():
    # Read the list of Python versions that have not reached EOL.
    with PYTHON_VERSIONS_FILE.open(encoding="utf-8") as file:
        versions = json.load(file)

    # Consider Python 3 releases only.
    versions = [
        version
        for version in versions
        if re.fullmatch(r"3\.\d+", version)
    ]

    if not versions:
        raise ValueError("No eligible Python 3 versions were found.")

    # Determine the oldest eligible Python version.
    versions.sort(
        key=lambda version: tuple(map(int, version.split(".")))
    )
    minimum_version = versions[0]

    # Parse pyproject.toml while preserving its formatting and comments.
    with PYPROJECT_FILE.open(encoding="utf-8") as file:
        document = tomlkit.parse(file.read())

    project = document["project"]

    # Update the minimum supported Python version.
    project["requires-python"] = f">={minimum_version}"

    # Remove Python 3 version classifiers for EOL releases.
    classifiers = project["classifiers"]

    retained_classifiers = [
        classifier
        for classifier in classifiers
        if not (
            classifier.startswith("Programming Language :: Python :: 3.")
            and classifier.rsplit(" :: ", 1)[-1] not in versions
        )
    ]

    project["classifiers"] = retained_classifiers

    # Save the updated configuration.
    with PYPROJECT_FILE.open("w", encoding="utf-8") as file:
        file.write(tomlkit.dumps(document))

    print(f"Updated requires-python to >={minimum_version}")


if __name__ == "__main__":
    main()

import re
from pathlib import Path

import tomlkit

from get_nonEOL_Python import get_non_eol_python_versions


ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_FILE = ROOT / "pyproject.toml"


def main():
    # Get Python versions directly from the API helper.
    versions = get_non_eol_python_versions()

    # Keep Python 3 releases only.
    versions = [
        version
        for version in versions
        if re.fullmatch(r"3\.\d+", version)
    ]

    if not versions:
        raise ValueError("No eligible Python 3 versions were found.")

    minimum_version = versions[0]

    # Read the existing project configuration.
    with PYPROJECT_FILE.open(encoding="utf-8") as file:
        document = tomlkit.parse(file.read())

    project = document["project"]

    # Update the minimum Python version.
    project["requires-python"] = f">={minimum_version}"

    # Remove Python 3 version classifiers for EOL releases.
    classifiers = project["classifiers"]

    project["classifiers"] = [
        classifier
        for classifier in classifiers
        if not (
            classifier.startswith("Programming Language :: Python :: 3.")
            and classifier.rsplit(" :: ", 1)[-1] not in versions
        )
    ]

    # Write the updated configuration.
    with PYPROJECT_FILE.open("w", encoding="utf-8") as file:
        file.write(tomlkit.dumps(document))

    print(f"Updated requires-python to >={minimum_version}")


if __name__ == "__main__":
    main()
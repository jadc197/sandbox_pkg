from pathlib import Path

import tomlkit

from get_nonEOL_Python import (
    get_non_eol_python_versions,
    get_python_releases,
)


ROOT = Path(__file__).resolve().parent#.parent
PYPROJECT_FILE = ROOT / "pyproject.toml"

PYTHON_CLASSIFIER_PREFIX = "Programming Language :: Python :: "


def update_pyproject():
    """Update Python compatibility metadata in pyproject.toml."""
    releases = get_python_releases()
    versions = get_non_eol_python_versions(releases)

    if not versions:
        raise RuntimeError("No non-EOL Python versions were found.")

    api_versions = {release["cycle"] for release in releases}
    eol_versions = api_versions - set(versions)

    document = tomlkit.parse(
        PYPROJECT_FILE.read_text(encoding="utf-8")
    )
    project = document["project"]

    project["requires-python"] = f">={versions[0]}"

    classifiers = project["classifiers"]

    for i in range(len(classifiers) - 1, -1, -1):
        classifier = classifiers[i]

        if classifier.startswith(PYTHON_CLASSIFIER_PREFIX):
            version = classifier[len(PYTHON_CLASSIFIER_PREFIX):]

            if version not in api_versions or version in eol_versions:
                del classifiers[i]

    PYPROJECT_FILE.write_text(
        tomlkit.dumps(document),
        encoding="utf-8",
    )

    print(f"Updated requires-python to >={versions[0]}")
    print(f"EOL versions detected: {sorted(eol_versions)}")


if __name__ == "__main__":
    update_pyproject()

# /// script
# [tool.fair-mappings]
# name = "Python Metadata to FAIR Mappings Schema"
# description = """A script that generates metadata describing a Mapping Specification implemented \
# in a Python script. See discussion in https://github.com/mapping-commons/fair-mappings-schema/pull/10."""
# [tool.fair-mappings.author]
# name = "Charles Tapley Hoyt"
# orcid = "0000-0003-4423-4370"
# email = "cthoyt@gmail.com"
# [tool.fair-mappings.subject_source]
# name = "Python Metadata"
# [tool.fair-mappings.object_source]
# name = "FAIR Mappings Schema"
# ///

"""Extract metadata from Python script.

Run this script by passing the URL to a script on GitHub like in:

.. code-block:: console

    $ python -m fair_mappings_schema.annotate_script --url https://github.com/cthoyt/fair-mappings-schema/raw/refs/heads/software-description/src/fair_mappings_schema/annotate_script.py
    author:
      name: Charles Tapley Hoyt
      orcid: 0000-0003-4423-4370
      type: Person
    content_url: https://github.com/cthoyt/fair-mappings-schema/raw/refs/heads/software-description/src/fair_mappings_schema/annotate_script.py
    description: A script that generates metadata describing a Mapping Specification implemented
      in a Python script. See discussion in https://github.com/mapping-commons/fair-mappings-schema/pull/10.
    license: Apache-2.0
    mapping_method: Python script
    name: Python Metadata to FAIR Mappings Schema
    object_source:
      name: FAIR Mappings Schema
    subject_source:
      name: Python Metadata
    type: other

"""

import re
from typing import Any

from fair_mappings_schema.datamodel.fair_mappings_schema_pydantic import (
    MappingSpecification,
    Person,
    MappingSpecificationTypeEnum,
)
import click
import requests
from pystow.utils import model_dump_yaml
import tomllib

__all__ = ["get_python_script"]


def get_python_script(script_url: str) -> MappingSpecification:
    """Get a mapping specification from a package."""
    data = dict(
        content_url=script_url,
        # TODO add explicit way of saying it's code
        type=MappingSpecificationTypeEnum.other,
        mapping_method="Python script",
    )
    data.update(_get_package_data(script_url))
    data.update(_get_script_data(script_url))
    return MappingSpecification.model_validate(data)


def _get_package_data(script_url: str, branch: str = "main") -> dict[str, Any]:
    owner, repo = _get_repository(script_url)
    pyproject_toml_url = (
        f"https://github.com/{owner}/{repo}/raw/refs/heads/{branch}/pyproject.toml"
    )
    pyproject_toml_res = requests.get(pyproject_toml_url, timeout=5)
    if pyproject_toml_res.status_code != 200:
        return {}  # there's no package data
    pyproject_toml_data = tomllib.loads(pyproject_toml_res.text)
    project = pyproject_toml_data["project"]
    urls = pyproject_toml_data.get("urls", {})
    documentation = urls.get("documentation") or urls.get("Documentation")
    return dict(
        name=project["name"],
        version=project.get("version"),
        description=project.get("description"),
        license=project.get("license"),
        author=_get_person(project, "authors"),
        documentation=documentation,
    )


def _get_script_data(script_url: str) -> dict[str, Any]:
    """Get a mapping specification from a package."""
    res = requests.get(script_url, timeout=5)
    res.raise_for_status()
    dd = extract_script_toml(res.text)
    if not dd:
        return {}
    rv = dd.get("tool", {}).get("fair-mappings")
    if rv.get("author"):
        if rv["author"]["email"]:
            del rv["author"]["email"]  # TODO
        rv["author"] = Person.model_validate(rv["author"])
    return rv


def _get_person(project: dict[str, Any], key: str) -> Person | None:
    people = project.get(key)
    if not people:
        return None
    person = people[0]
    name = person["name"]
    # TODO add email to person model
    # TODO see if we can recognize ORCiD here more officially
    orcid = person.get("orcid")
    if orcid:
        orcid = orcid.removeprefix("https://orcid.com")
        orcid = orcid.removeprefix("http://orcid.com")
    return Person(name=name, orcid=orcid)


def _get_repository(url: str) -> tuple[str, str]:
    """Get a mapping specification from a package."""
    if url.startswith("https://github.com/"):
        url = url.removeprefix("https://github.com/")
    if url.startswith("http://github.com/"):
        url = url.removeprefix("http://github.com/")

    parts = url.split("/")
    if len(parts) == 1:
        raise ValueError(f"no repository given, just an owner: {url}")
    owner, repo, *_ = parts
    return owner, repo


TOML_PATTERN = re.compile(
    r"^#\s/// script\s*\n"  # opening marker
    r"((?:#[^\n]*\n)*?)"  # captured comment lines
    r"#\s///\s*$",  # closing marker
    re.MULTILINE,
)


def extract_script_toml(source: str) -> dict[str, Any] | None:
    """Extract the raw TOML string from a `# /// script` ... `# ///` block."""
    match = TOML_PATTERN.search(source)
    if not match:
        return None

    # Strip the leading `# ` (or `#`) from every line
    toml_lines = []
    for line in match.group(1).splitlines():
        # Remove exactly one leading `# ` or `#`
        toml_lines.append(re.sub(r"^#( ?)", "", line))

    return tomllib.loads("\n".join(toml_lines))


DEMO_URLS = [
    "https://github.com/cthoyt/fair-mappings-schema/raw/refs/heads/software-description/src/fair_mappings_schema/annotate_script.py",
    "https://github.com/data-literacy-alliance/oerbservatory/raw/refs/heads/main/src/oerbservatory/sources/dalia.py",
    "https://github.com/data-literacy-alliance/oerbservatory/raw/refs/heads/main/src/oerbservatory/sources/tess.py",
]


def fix_github_url(url: str) -> str:
    """Ensure that a GitHub URL is downloadable."""
    return url.replace("/blob/", "/raw/refs/heads/")


@click.command()
@click.option("--url", help="URL to a script on GitHub")
def main(url: str | None) -> None:
    """Get mapping specification YAML from a URL to a packaged Python script on GitHub."""
    if url is not None:
        url = fix_github_url(url)
        model = get_python_script(url)
        click.echo(model_dump_yaml(model, exclude_none=True))
    else:
        click.secho("Demo Mode, since no --url given", fg="green")
        for url in DEMO_URLS:
            model = get_python_script(url)
            click.echo(model_dump_yaml(model, exclude_none=True))


if __name__ == "__main__":
    main()

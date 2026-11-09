# FAIR Mappings Schema

[![Build and test](https://github.com/mapping-commons/fair-mappings-schema/actions/workflows/main.yaml/badge.svg)](https://github.com/mapping-commons/fair-mappings-schema/actions/workflows/main.yaml)
[![Docs](https://github.com/mapping-commons/fair-mappings-schema/actions/workflows/deploy-docs.yaml/badge.svg)](https://mapping-commons.github.io/fair-mappings-schema)
[![PyPI](https://img.shields.io/pypi/v/fair-mappings)](https://pypi.org/project/fair-mappings/)
[![Python versions](https://img.shields.io/pypi/pyversions/fair-mappings)](https://pypi.org/project/fair-mappings/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24086059.svg)](https://doi.org/10.5281/zenodo.24086059)
[![Built with LinkML](https://img.shields.io/badge/built%20with-LinkML-1d4f91)](https://linkml.io)
[![License](https://img.shields.io/github/license/mapping-commons/fair-mappings-schema)](https://github.com/mapping-commons/fair-mappings-schema/blob/main/LICENSE)

A minimal metadata schema for describing **mapping specifications** — SSSOM mapping sets,
LinkML-Map transformations, R2RML, XSLT and the like — so that they can be found, cited, assessed and
reused. It records _what_ a mapping specification is, who made it, what it maps between and where to
get it. It does not model the individual mappings themselves.

The schema is developed by the
[RDA FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/) and written in
[LinkML](https://linkml.io), so JSON Schema, Python classes, OWL and SHACL can all be generated from it.

**Documentation:** <https://mapping-commons.github.io/fair-mappings-schema>

## What it describes

| Class | Describes |
|---|---|
| `MappingSpecification` | A mapping artefact: identifier, type, version, license, method, documentation and where to download it |
| `Source` | What is being mapped from (`subject_source`) or to (`object_source`): an ontology, vocabulary, schema, database or API |
| `Agent` | Who was involved, as `author`, `creator` or `reviewer`: a `Person` (ORCID), an `Organization` (ROR) or a piece of `Software` |

Supported specification types: `sssom`, `linkml_map`, `r2rml`, `rml`, `yarrrml`, `sparql`, `xslt`,
`shacl` and `other`.

A minimal mapping specification:

```yaml
id: https://example.org/mappings/anatomy
name: Anatomy ontology A to B
type: sssom
version: "3.0.0"
license: https://creativecommons.org/publicdomain/zero/1.0/
mapping_method: semi-automated matching followed by manual review
content_url: https://example.org/mappings/anatomy.sssom.tsv
author:
  - id: orcid:0000-0002-1825-0097
    type: Person
    name: Ada Curator
creator:
  - id: example:exomatch
    type: Software
    name: exomatch
    version: "0.4.2"
subject_source:
  name: Example Anatomy Ontology A
  type: ontology
  version: "2024-05-01"
object_source:
  name: Example Anatomy Ontology B
  type: ontology
  version: "2024-05-20"
```

## Installation

```bash
pip install fair-mappings
```

This installs the schema, the generated Python data model and the `fair-mappings` command line tool.
Python 3.10 or newer is required.

## Usage

### Command line

Extract a FAIR Mappings description from an existing SSSOM mapping set or LinkML-Map transformation:

```console
$ fair-mappings parse -I sssom hp-mp.sssom.tsv
Wrote hp-mp.fms.yml
```

```yaml
id: https://w3id.org/sssom/mappings/hp-mp
name: HP to MP mappings
description: Phenotype mappings between the Human Phenotype Ontology and the Mammalian
  Phenotype Ontology
license: https://creativecommons.org/licenses/by/4.0/
type: sssom
subject_source:
  id: obo:hp
object_source:
  id: obo:mp
```

Validate a description against the schema. With `-I`, the source document is converted first, so you can
check an SSSOM file directly:

```console
$ fair-mappings validate hp-mp.fms.yml
OK: hp-mp.fms.yml is valid.

$ fair-mappings validate -I sssom hp-mp.sssom.tsv
OK: hp-mp.sssom.tsv is valid.
```

`validate` exits non-zero and prints the errors to stderr when an instance is invalid, so it can be used
in CI. Run `fair-mappings --help` for all options.

### Python

```python
from fair_mappings_schema import load_mapping, validate_instance

spec = load_mapping("hp-mp.sssom.tsv", "sssom")  # a MappingSpecification dict
errors = validate_instance(spec)                 # [] if valid
```

`parse_sssom_tsv` also accepts an iterable of lines, so the metadata header of a remote mapping set
can be read from a streamed response without downloading the whole file.

## Identifiers

| | |
|---|---|
| Schema | [`https://w3id.org/fair-map/schema`](https://w3id.org/fair-map/schema) |
| Schema source | [`https://w3id.org/fair-map/schema.yaml`](https://w3id.org/fair-map/schema.yaml) |
| Prefix | `fairmap` → `https://w3id.org/fair-map/`, e.g. `fairmap:MappingSpecification` |

## Development

The project uses [uv](https://docs.astral.sh/uv/) and the command runner
[just](https://github.com/casey/just):

```bash
git clone https://github.com/mapping-commons/fair-mappings-schema
cd fair-mappings-schema
uv sync --dev
just test       # schema checks, Python tests and example validation
just gen-doc    # regenerate the documentation
just testdoc    # build and serve the docs locally
```

Run `just` to list all recipes. The schema lives in
[`src/fair_mappings_schema/schema/fair_mappings_schema.yaml`](https://github.com/mapping-commons/fair-mappings-schema/blob/main/src/fair_mappings_schema/schema/fair_mappings_schema.yaml);
the Python data model in `src/fair_mappings_schema/datamodel/` is generated from it with
`just gen-python` and should not be edited by hand.

Contributions are welcome. See
[CONTRIBUTING.md](https://github.com/mapping-commons/fair-mappings-schema/blob/main/CONTRIBUTING.md)
and the [issue tracker](https://github.com/mapping-commons/fair-mappings-schema/issues).

## Citing

If you use the FAIR Mappings Schema, please cite it through its Zenodo record:
[doi:10.5281/zenodo.24086059](https://doi.org/10.5281/zenodo.24086059).

## Related work

- [RDA FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/): use cases,
  recommendations and the conceptual model this schema implements
- [SSSOM](https://mapping-commons.github.io/sssom/): the Simple Standard for Sharing Ontological Mappings
- [LinkML-Map](https://linkml.io/linkml-map/): schema mappings with executable transformation rules
- [Semantic Mapping Vocabulary (semapv)](https://mapping-commons.github.io/semantic-mapping-vocabulary/)

## License

[Apache License 2.0](https://github.com/mapping-commons/fair-mappings-schema/blob/main/LICENSE).

This project was generated from
[linkml-project-copier](https://github.com/dalito/linkml-project-copier)
([doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)).

# FAIR Mappings Schema

A minimal metadata schema for describing FAIR mapping specifications between data sources.

## Overview

The FAIR Mappings Schema provides a standardized way to describe mappings between different data sources such as ontologies, databases, vocabularies, and schemas. It captures essential metadata about mapping specifications including provenance, licensing, and the sources being mapped.

This schema is developed as part of the [RDA FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/) effort to improve the findability, accessibility, interoperability, and reusability of semantic mappings.

## Key Features

- **Source Description**: Describe subject and object sources with their types, versions, and access URLs
- **Provenance Tracking**: Record authors, creators, reviewers, and publication dates
- **Mapping Specification system agnostic**: Can be used, or easily mapped to, SSSOM, R2RML, RML, SPARQL, YARRRML, XSLT, SHACL, and other mapping formats.

## Example

```yaml
---
publication_date: "2024-01-15"
license: CC-BY-4.0
version: "1.0.0"
description: Mappings between disease ontologies DO and MONDO
type: sssom
mapping_method: manual curation
documentation: https://example.org/do-mondo-mappings/docs
content_url: https://example.org/mappings/do-mondo.sssom.tsv
subject_source:
  name: Disease Ontology
  version: "2024-01-01"
  type: ontology
  documentation: https://disease-ontology.org/
  content_url: http://purl.obolibrary.org/obo/doid.owl
  content_type: application/rdf+xml
object_source:
  name: Mondo Disease Ontology
  version: "2024-01-10"
  type: ontology
  documentation: https://mondo.monarchinitiative.org/
  content_url: http://purl.obolibrary.org/obo/mondo.owl
  content_type: application/rdf+xml
```

## Documentation

- [Schema Elements](elements/index.md) - Documentation for all schema classes, slots, and enums.

## Quick Links

- [RDA FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/)
- [GitHub Repository](https://github.com/mapping-commons/fair-mappings-schema)

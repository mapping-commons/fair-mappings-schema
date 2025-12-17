# About FAIR Mappings Schema

## Background

Semantic mappings between ontologies, vocabularies, databases, and other data sources are essential for data integration and interoperability. However, these mappings are often poorly documented, difficult to discover, and lack the metadata needed to assess their quality and provenance.

The FAIR Mappings Schema addresses this gap by providing a minimal but comprehensive metadata model for describing mapping specifications in a way that adheres to [FAIR principles](https://www.go-fair.org/fair-principles/) (Findable, Accessible, Interoperable, Reusable).

## RDA FAIR Mappings Working Group

This schema is developed by the [RDA FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/), which brings together researchers, practitioners, and standards developers to establish best practices for creating and sharing FAIR mappings.

The working group aims to:

- Define metadata standards for mapping specifications
- Promote interoperability between different mapping formats
- Build a community around mapping best practices

## Schema Design

The schema is built using [LinkML](https://linkml.io/), a flexible modeling language that generates multiple representations including JSON Schema, Python dataclasses, and RDF/OWL.

### Core Concepts

- **MappingSpecification**: The central class representing a mapping between sources
- **Source**: A data source (ontology, database, vocabulary, schema, or API) from which entities are drawn
- **Agent**: An entity (person, organization, or software) that contributes to creating mappings

## Contributing

Contributions are welcome. Please visit the [GitHub repository](https://github.com/mapping-commons/fair-mappings-schema) to report issues or submit pull requests.

## License

This project is licensed under Apache-2.0.

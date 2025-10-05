# Auto generated from fair_mappings_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-10-06T00:35:53
# Schema: fair-mappings-schema
#
# id: https://w3id.org/mapping-commons/fair-mappings-schema
# description: A minimal metadata schema for FAIR mapping specifications
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Namespaces
PATO = CurieNamespace('PATO', 'http://purl.obolibrary.org/obo/PATO_')
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/')
EXAMPLE = CurieNamespace('example', 'https://example.org/')
FAIR_MAPPINGS_SCHEMA = CurieNamespace('fair_mappings_schema', 'https://w3id.org/mapping-commons/fair-mappings-schema/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = FAIR_MAPPINGS_SCHEMA


# Types

# Class references



@dataclass(repr=False)
class Agent(YAMLRoot):
    """
    An entity that can create or contribute to a digital object, such as an author or creator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA["Agent"]
    class_class_curie: ClassVar[str] = "fair_mappings_schema:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA.Agent

    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    type: Optional[Union[str, "AgentTypeEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.type is not None and not isinstance(self.type, AgentTypeEnum):
            self.type = AgentTypeEnum(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Source(YAMLRoot):
    """
    A data source from which entities are drawn, such as a database, ontology, or vocabulary.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA["Source"]
    class_class_curie: ClassVar[str] = "fair_mappings_schema:Source"
    class_name: ClassVar[str] = "Source"
    class_model_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA.Source

    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    type: Optional[Union[str, "SourceTypeEnum"]] = None
    documentation: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.type is not None and not isinstance(self.type, SourceTypeEnum):
            self.type = SourceTypeEnum(self.type)

        if self.documentation is not None and not isinstance(self.documentation, str):
            self.documentation = str(self.documentation)

        if self.content is not None and not isinstance(self.content, str):
            self.content = str(self.content)

        if self.content_type is not None and not isinstance(self.content_type, str):
            self.content_type = str(self.content_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MappingSpecification(YAMLRoot):
    """
    A formal description of correspondences between entities in a source and a target, expressed as rules, functions,
    or mapping statements.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA["MappingSpecification"]
    class_class_curie: ClassVar[str] = "fair_mappings_schema:MappingSpecification"
    class_name: ClassVar[str] = "MappingSpecification"
    class_model_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA.MappingSpecification

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[Union[dict, Agent]] = None
    creator: Optional[Union[dict, Agent]] = None
    reviewer: Optional[Union[dict, Agent]] = None
    publication_date: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None
    type: Optional[Union[str, "MappingSpecificationTypeEnum"]] = None
    mapping_method: Optional[str] = None
    documentation: Optional[str] = None
    content: Optional[str] = None
    subject_source: Optional[Union[dict, Source]] = None
    object_source: Optional[Union[dict, Source]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.author is not None and not isinstance(self.author, Agent):
            self.author = Agent(**as_dict(self.author))

        if self.creator is not None and not isinstance(self.creator, Agent):
            self.creator = Agent(**as_dict(self.creator))

        if self.reviewer is not None and not isinstance(self.reviewer, Agent):
            self.reviewer = Agent(**as_dict(self.reviewer))

        if self.publication_date is not None and not isinstance(self.publication_date, str):
            self.publication_date = str(self.publication_date)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.type is not None and not isinstance(self.type, MappingSpecificationTypeEnum):
            self.type = MappingSpecificationTypeEnum(self.type)

        if self.mapping_method is not None and not isinstance(self.mapping_method, str):
            self.mapping_method = str(self.mapping_method)

        if self.documentation is not None and not isinstance(self.documentation, str):
            self.documentation = str(self.documentation)

        if self.content is not None and not isinstance(self.content, str):
            self.content = str(self.content)

        if self.subject_source is not None and not isinstance(self.subject_source, Source):
            self.subject_source = Source(**as_dict(self.subject_source))

        if self.object_source is not None and not isinstance(self.object_source, Source):
            self.object_source = Source(**as_dict(self.object_source))

        super().__post_init__(**kwargs)


# Enumerations
class AgentTypeEnum(EnumDefinitionImpl):
    """
    Types of agents that can contribute to a mapping specification
    """
    person = PermissibleValue(
        text="person",
        description="An individual person")
    organization = PermissibleValue(
        text="organization",
        description="An organization or institution")
    software = PermissibleValue(
        text="software",
        description="A software tool or system")

    _defn = EnumDefinition(
        name="AgentTypeEnum",
        description="Types of agents that can contribute to a mapping specification",
    )

class SourceTypeEnum(EnumDefinitionImpl):
    """
    Types of data sources
    """
    owl_ontology = PermissibleValue(
        text="owl_ontology",
        description="An ontology in OWL format")
    database = PermissibleValue(
        text="database",
        description="A relational or other database")
    skos_vocabulary = PermissibleValue(
        text="skos_vocabulary",
        description="A SKOS vocabulary or terminology")
    rdf_vocabulary = PermissibleValue(
        text="rdf_vocabulary",
        description="An RDF vocabulary or schema")
    schema = PermissibleValue(
        text="schema",
        description="A data schema or model")
    api = PermissibleValue(
        text="api",
        description="An API or web service")
    other = PermissibleValue(
        text="other",
        description="Other type of source")

    _defn = EnumDefinition(
        name="SourceTypeEnum",
        description="Types of data sources",
    )

class MappingSpecificationTypeEnum(EnumDefinitionImpl):
    """
    Types of mapping specifications
    """
    sssom = PermissibleValue(
        text="sssom",
        description="Simple Standard for Sharing Ontological Mappings")
    r2rml = PermissibleValue(
        text="r2rml",
        description="RDB to RDF Mapping Language")
    rml = PermissibleValue(
        text="rml",
        description="RDF Mapping Language")
    sparql = PermissibleValue(
        text="sparql",
        description="SPARQL-based mapping")
    other = PermissibleValue(
        text="other",
        description="Other type of mapping specification")

    _defn = EnumDefinition(
        name="MappingSpecificationTypeEnum",
        description="Types of mapping specifications",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=FAIR_MAPPINGS_SCHEMA.id, name="id", curie=FAIR_MAPPINGS_SCHEMA.curie('id'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.id, domain=None, range=Optional[str])

slots.name = Slot(uri=FAIR_MAPPINGS_SCHEMA.name, name="name", curie=FAIR_MAPPINGS_SCHEMA.curie('name'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.name, domain=None, range=Optional[str])

slots.creator = Slot(uri=FAIR_MAPPINGS_SCHEMA.creator, name="creator", curie=FAIR_MAPPINGS_SCHEMA.curie('creator'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.creator, domain=None, range=Optional[Union[dict, Agent]])

slots.author = Slot(uri=FAIR_MAPPINGS_SCHEMA.author, name="author", curie=FAIR_MAPPINGS_SCHEMA.curie('author'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.author, domain=None, range=Optional[Union[dict, Agent]])

slots.reviewer = Slot(uri=FAIR_MAPPINGS_SCHEMA.reviewer, name="reviewer", curie=FAIR_MAPPINGS_SCHEMA.curie('reviewer'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.reviewer, domain=None, range=Optional[Union[dict, Agent]])

slots.mapping_tool = Slot(uri=FAIR_MAPPINGS_SCHEMA.mapping_tool, name="mapping_tool", curie=FAIR_MAPPINGS_SCHEMA.curie('mapping_tool'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.mapping_tool, domain=None, range=Optional[Union[dict, Agent]])

slots.publication_date = Slot(uri=FAIR_MAPPINGS_SCHEMA.publication_date, name="publication_date", curie=FAIR_MAPPINGS_SCHEMA.curie('publication_date'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.publication_date, domain=None, range=Optional[str])

slots.license = Slot(uri=FAIR_MAPPINGS_SCHEMA.license, name="license", curie=FAIR_MAPPINGS_SCHEMA.curie('license'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.license, domain=None, range=Optional[str])

slots.version = Slot(uri=FAIR_MAPPINGS_SCHEMA.version, name="version", curie=FAIR_MAPPINGS_SCHEMA.curie('version'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.version, domain=None, range=Optional[str])

slots.description = Slot(uri=FAIR_MAPPINGS_SCHEMA.description, name="description", curie=FAIR_MAPPINGS_SCHEMA.curie('description'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.description, domain=None, range=Optional[str])

slots.type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.type, domain=None, range=Optional[str])

slots.mapping_method = Slot(uri=FAIR_MAPPINGS_SCHEMA.mapping_method, name="mapping_method", curie=FAIR_MAPPINGS_SCHEMA.curie('mapping_method'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.mapping_method, domain=None, range=Optional[str])

slots.documentation = Slot(uri=FAIR_MAPPINGS_SCHEMA.documentation, name="documentation", curie=FAIR_MAPPINGS_SCHEMA.curie('documentation'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.documentation, domain=None, range=Optional[str])

slots.content = Slot(uri=FAIR_MAPPINGS_SCHEMA.content, name="content", curie=FAIR_MAPPINGS_SCHEMA.curie('content'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.content, domain=None, range=Optional[str])

slots.content_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.content_type, name="content_type", curie=FAIR_MAPPINGS_SCHEMA.curie('content_type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.content_type, domain=None, range=Optional[str])

slots.subject_source = Slot(uri=FAIR_MAPPINGS_SCHEMA.subject_source, name="subject_source", curie=FAIR_MAPPINGS_SCHEMA.curie('subject_source'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.subject_source, domain=None, range=Optional[Union[dict, Source]])

slots.object_source = Slot(uri=FAIR_MAPPINGS_SCHEMA.object_source, name="object_source", curie=FAIR_MAPPINGS_SCHEMA.curie('object_source'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.object_source, domain=None, range=Optional[Union[dict, Source]])

slots.Agent_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="Agent_type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.Agent_type, domain=Agent, range=Optional[Union[str, "AgentTypeEnum"]])

slots.Source_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="Source_type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.Source_type, domain=Source, range=Optional[Union[str, "SourceTypeEnum"]])

slots.MappingSpecification_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="MappingSpecification_type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.MappingSpecification_type, domain=MappingSpecification, range=Optional[Union[str, "MappingSpecificationTypeEnum"]])

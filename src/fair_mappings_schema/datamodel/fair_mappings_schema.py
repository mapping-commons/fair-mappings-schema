# Auto generated from fair_mappings_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-10-06T23:29:58
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
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Person(Agent):
    """
    An individual person who contributes to a mapping specification
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA["Person"]
    class_class_curie: ClassVar[str] = "fair_mappings_schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA.Person

    orcid: Optional[str] = None
    affiliation: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.orcid is not None and not isinstance(self.orcid, str):
            self.orcid = str(self.orcid)

        if self.affiliation is not None and not isinstance(self.affiliation, str):
            self.affiliation = str(self.affiliation)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


@dataclass(repr=False)
class Organization(Agent):
    """
    An organization or institution that contributes to a mapping specification
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA["Organization"]
    class_class_curie: ClassVar[str] = "fair_mappings_schema:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA.Organization

    ror_id: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ror_id is not None and not isinstance(self.ror_id, str):
            self.ror_id = str(self.ror_id)

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


@dataclass(repr=False)
class Software(Agent):
    """
    A software tool or system used in creating mappings
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA["Software"]
    class_class_curie: ClassVar[str] = "fair_mappings_schema:Software"
    class_name: ClassVar[str] = "Software"
    class_model_uri: ClassVar[URIRef] = FAIR_MAPPINGS_SCHEMA.Software

    version: Optional[str] = None
    repository_url: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.repository_url is not None and not isinstance(self.repository_url, str):
            self.repository_url = str(self.repository_url)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


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
    content_url: Optional[str] = None
    content_type: Optional[str] = None
    metadata_url: Optional[str] = None
    metadata_type: Optional[str] = None

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

        if self.content_url is not None and not isinstance(self.content_url, str):
            self.content_url = str(self.content_url)

        if self.content_type is not None and not isinstance(self.content_type, str):
            self.content_type = str(self.content_type)

        if self.metadata_url is not None and not isinstance(self.metadata_url, str):
            self.metadata_url = str(self.metadata_url)

        if self.metadata_type is not None and not isinstance(self.metadata_type, str):
            self.metadata_type = str(self.metadata_type)

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
    content_url: Optional[str] = None
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

        if self.content_url is not None and not isinstance(self.content_url, str):
            self.content_url = str(self.content_url)

        if self.subject_source is not None and not isinstance(self.subject_source, Source):
            self.subject_source = Source(**as_dict(self.subject_source))

        if self.object_source is not None and not isinstance(self.object_source, Source):
            self.object_source = Source(**as_dict(self.object_source))

        super().__post_init__(**kwargs)


# Enumerations
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
    yarrrml = PermissibleValue(
        text="yarrrml",
        description="YARRRML mapping file")
    xslt = PermissibleValue(
        text="xslt",
        description="XSLT-based mapping")
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

slots.content_url = Slot(uri=FAIR_MAPPINGS_SCHEMA.content_url, name="content_url", curie=FAIR_MAPPINGS_SCHEMA.curie('content_url'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.content_url, domain=None, range=Optional[str])

slots.content_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.content_type, name="content_type", curie=FAIR_MAPPINGS_SCHEMA.curie('content_type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.content_type, domain=None, range=Optional[str])

slots.metadata_url = Slot(uri=FAIR_MAPPINGS_SCHEMA.metadata_url, name="metadata_url", curie=FAIR_MAPPINGS_SCHEMA.curie('metadata_url'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.metadata_url, domain=None, range=Optional[str])

slots.metadata_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.metadata_type, name="metadata_type", curie=FAIR_MAPPINGS_SCHEMA.curie('metadata_type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.metadata_type, domain=None, range=Optional[str])

slots.subject_source = Slot(uri=FAIR_MAPPINGS_SCHEMA.subject_source, name="subject_source", curie=FAIR_MAPPINGS_SCHEMA.curie('subject_source'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.subject_source, domain=None, range=Optional[Union[dict, Source]])

slots.object_source = Slot(uri=FAIR_MAPPINGS_SCHEMA.object_source, name="object_source", curie=FAIR_MAPPINGS_SCHEMA.curie('object_source'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.object_source, domain=None, range=Optional[Union[dict, Source]])

slots.orcid = Slot(uri=FAIR_MAPPINGS_SCHEMA.orcid, name="orcid", curie=FAIR_MAPPINGS_SCHEMA.curie('orcid'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.orcid, domain=None, range=Optional[str])

slots.affiliation = Slot(uri=FAIR_MAPPINGS_SCHEMA.affiliation, name="affiliation", curie=FAIR_MAPPINGS_SCHEMA.curie('affiliation'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.affiliation, domain=None, range=Optional[str])

slots.ror_id = Slot(uri=FAIR_MAPPINGS_SCHEMA.ror_id, name="ror_id", curie=FAIR_MAPPINGS_SCHEMA.curie('ror_id'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.ror_id, domain=None, range=Optional[str])

slots.url = Slot(uri=FAIR_MAPPINGS_SCHEMA.url, name="url", curie=FAIR_MAPPINGS_SCHEMA.curie('url'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.url, domain=None, range=Optional[str])

slots.repository_url = Slot(uri=FAIR_MAPPINGS_SCHEMA.repository_url, name="repository_url", curie=FAIR_MAPPINGS_SCHEMA.curie('repository_url'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.repository_url, domain=None, range=Optional[str])

slots.Agent_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="Agent_type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.Agent_type, domain=Agent, range=Optional[str])

slots.Source_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="Source_type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.Source_type, domain=Source, range=Optional[Union[str, "SourceTypeEnum"]])

slots.MappingSpecification_type = Slot(uri=FAIR_MAPPINGS_SCHEMA.type, name="MappingSpecification_type", curie=FAIR_MAPPINGS_SCHEMA.curie('type'),
                   model_uri=FAIR_MAPPINGS_SCHEMA.MappingSpecification_type, domain=MappingSpecification, range=Optional[Union[str, "MappingSpecificationTypeEnum"]])

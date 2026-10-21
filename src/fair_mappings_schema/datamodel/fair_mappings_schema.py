# Auto generated from fair_mappings_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-10-21T19:47:20
# Schema: fair-mappings-schema
#
# id: https://w3id.org/fair-map/schema
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
FAIRMAP = CurieNamespace('fairmap', 'https://w3id.org/fair-map/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = FAIRMAP


# Types

# Class references



@dataclass(repr=False)
class Agent(YAMLRoot):
    """
    An entity that can create or contribute to a digital object, such as an author or creator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FAIRMAP["Agent"]
    class_class_curie: ClassVar[str] = "fairmap:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = FAIRMAP.Agent

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

    class_class_uri: ClassVar[URIRef] = FAIRMAP["Person"]
    class_class_curie: ClassVar[str] = "fairmap:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = FAIRMAP.Person

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

    class_class_uri: ClassVar[URIRef] = FAIRMAP["Organization"]
    class_class_curie: ClassVar[str] = "fairmap:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = FAIRMAP.Organization

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

    class_class_uri: ClassVar[URIRef] = FAIRMAP["Software"]
    class_class_curie: ClassVar[str] = "fairmap:Software"
    class_name: ClassVar[str] = "Software"
    class_model_uri: ClassVar[URIRef] = FAIRMAP.Software

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

    class_class_uri: ClassVar[URIRef] = FAIRMAP["Source"]
    class_class_curie: ClassVar[str] = "fairmap:Source"
    class_name: ClassVar[str] = "Source"
    class_model_uri: ClassVar[URIRef] = FAIRMAP.Source

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

    class_class_uri: ClassVar[URIRef] = FAIRMAP["MappingSpecification"]
    class_class_curie: ClassVar[str] = "fairmap:MappingSpecification"
    class_name: ClassVar[str] = "MappingSpecification"
    class_model_uri: ClassVar[URIRef] = FAIRMAP.MappingSpecification

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]] = empty_list()
    creator: Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]] = empty_list()
    reviewer: Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]] = empty_list()
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

        if not isinstance(self.author, list):
            self.author = [self.author] if self.author is not None else []
        self.author = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.author]

        if not isinstance(self.creator, list):
            self.creator = [self.creator] if self.creator is not None else []
        self.creator = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.creator]

        if not isinstance(self.reviewer, list):
            self.reviewer = [self.reviewer] if self.reviewer is not None else []
        self.reviewer = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.reviewer]

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
    ontology = PermissibleValue(
        text="ontology",
        description="A conceptualization or formal representation of a domain, such as an OWL ontology.")
    database = PermissibleValue(
        text="database",
        description="A relational or other database")
    vocabulary = PermissibleValue(
        text="vocabulary",
        description="A controlled vocabulary or thesaurus, such as a SKOS vocabulary or an RDFS vocabulary.")
    schema = PermissibleValue(
        text="schema",
        description="A data schema or model, such as an XML Schema or JSON Schema.")
    api = PermissibleValue(
        text="api",
        description="An API or web service.")
    other = PermissibleValue(
        text="other",
        description="Other type of source.")

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
    shacl = PermissibleValue(
        text="shacl",
        description="SHACL-based mapping")
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

slots.id = Slot(uri=FAIRMAP.id, name="id", curie=FAIRMAP.curie('id'),
                   model_uri=FAIRMAP.id, domain=None, range=Optional[str])

slots.name = Slot(uri=FAIRMAP.name, name="name", curie=FAIRMAP.curie('name'),
                   model_uri=FAIRMAP.name, domain=None, range=Optional[str])

slots.creator = Slot(uri=FAIRMAP.creator, name="creator", curie=FAIRMAP.curie('creator'),
                   model_uri=FAIRMAP.creator, domain=None, range=Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]])

slots.author = Slot(uri=FAIRMAP.author, name="author", curie=FAIRMAP.curie('author'),
                   model_uri=FAIRMAP.author, domain=None, range=Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]])

slots.reviewer = Slot(uri=FAIRMAP.reviewer, name="reviewer", curie=FAIRMAP.curie('reviewer'),
                   model_uri=FAIRMAP.reviewer, domain=None, range=Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]])

slots.mapping_tool = Slot(uri=FAIRMAP.mapping_tool, name="mapping_tool", curie=FAIRMAP.curie('mapping_tool'),
                   model_uri=FAIRMAP.mapping_tool, domain=None, range=Optional[Union[dict, Agent]])

slots.publication_date = Slot(uri=FAIRMAP.publication_date, name="publication_date", curie=FAIRMAP.curie('publication_date'),
                   model_uri=FAIRMAP.publication_date, domain=None, range=Optional[str])

slots.license = Slot(uri=FAIRMAP.license, name="license", curie=FAIRMAP.curie('license'),
                   model_uri=FAIRMAP.license, domain=None, range=Optional[str])

slots.version = Slot(uri=FAIRMAP.version, name="version", curie=FAIRMAP.curie('version'),
                   model_uri=FAIRMAP.version, domain=None, range=Optional[str])

slots.description = Slot(uri=FAIRMAP.description, name="description", curie=FAIRMAP.curie('description'),
                   model_uri=FAIRMAP.description, domain=None, range=Optional[str])

slots.type = Slot(uri=FAIRMAP.type, name="type", curie=FAIRMAP.curie('type'),
                   model_uri=FAIRMAP.type, domain=None, range=Optional[str])

slots.mapping_method = Slot(uri=FAIRMAP.mapping_method, name="mapping_method", curie=FAIRMAP.curie('mapping_method'),
                   model_uri=FAIRMAP.mapping_method, domain=None, range=Optional[str])

slots.documentation = Slot(uri=FAIRMAP.documentation, name="documentation", curie=FAIRMAP.curie('documentation'),
                   model_uri=FAIRMAP.documentation, domain=None, range=Optional[str])

slots.content_url = Slot(uri=FAIRMAP.content_url, name="content_url", curie=FAIRMAP.curie('content_url'),
                   model_uri=FAIRMAP.content_url, domain=None, range=Optional[str])

slots.content_type = Slot(uri=FAIRMAP.content_type, name="content_type", curie=FAIRMAP.curie('content_type'),
                   model_uri=FAIRMAP.content_type, domain=None, range=Optional[str])

slots.metadata_url = Slot(uri=FAIRMAP.metadata_url, name="metadata_url", curie=FAIRMAP.curie('metadata_url'),
                   model_uri=FAIRMAP.metadata_url, domain=None, range=Optional[str])

slots.metadata_type = Slot(uri=FAIRMAP.metadata_type, name="metadata_type", curie=FAIRMAP.curie('metadata_type'),
                   model_uri=FAIRMAP.metadata_type, domain=None, range=Optional[str])

slots.subject_source = Slot(uri=FAIRMAP.subject_source, name="subject_source", curie=FAIRMAP.curie('subject_source'),
                   model_uri=FAIRMAP.subject_source, domain=None, range=Optional[Union[dict, Source]])

slots.object_source = Slot(uri=FAIRMAP.object_source, name="object_source", curie=FAIRMAP.curie('object_source'),
                   model_uri=FAIRMAP.object_source, domain=None, range=Optional[Union[dict, Source]])

slots.orcid = Slot(uri=FAIRMAP.orcid, name="orcid", curie=FAIRMAP.curie('orcid'),
                   model_uri=FAIRMAP.orcid, domain=None, range=Optional[str])

slots.affiliation = Slot(uri=FAIRMAP.affiliation, name="affiliation", curie=FAIRMAP.curie('affiliation'),
                   model_uri=FAIRMAP.affiliation, domain=None, range=Optional[str])

slots.ror_id = Slot(uri=FAIRMAP.ror_id, name="ror_id", curie=FAIRMAP.curie('ror_id'),
                   model_uri=FAIRMAP.ror_id, domain=None, range=Optional[str])

slots.url = Slot(uri=FAIRMAP.url, name="url", curie=FAIRMAP.curie('url'),
                   model_uri=FAIRMAP.url, domain=None, range=Optional[str])

slots.repository_url = Slot(uri=FAIRMAP.repository_url, name="repository_url", curie=FAIRMAP.curie('repository_url'),
                   model_uri=FAIRMAP.repository_url, domain=None, range=Optional[str])

slots.Agent_type = Slot(uri=FAIRMAP.type, name="Agent_type", curie=FAIRMAP.curie('type'),
                   model_uri=FAIRMAP.Agent_type, domain=Agent, range=Optional[str])

slots.Source_type = Slot(uri=FAIRMAP.type, name="Source_type", curie=FAIRMAP.curie('type'),
                   model_uri=FAIRMAP.Source_type, domain=Source, range=Optional[Union[str, "SourceTypeEnum"]])

slots.MappingSpecification_type = Slot(uri=FAIRMAP.type, name="MappingSpecification_type", curie=FAIRMAP.curie('type'),
                   model_uri=FAIRMAP.MappingSpecification_type, domain=MappingSpecification, range=Optional[Union[str, "MappingSpecificationTypeEnum"]])

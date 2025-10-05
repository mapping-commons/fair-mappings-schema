from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'fair_mappings_schema',
     'default_range': 'string',
     'description': 'A minimal metadata schema for FAIR mapping specifications',
     'id': 'https://w3id.org/mapping-commons/fair-mappings-schema',
     'imports': ['linkml:types'],
     'license': 'Apache-2.0',
     'name': 'fair-mappings-schema',
     'prefixes': {'PATO': {'prefix_prefix': 'PATO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/PATO_'},
                  'biolink': {'prefix_prefix': 'biolink',
                              'prefix_reference': 'https://w3id.org/biolink/'},
                  'example': {'prefix_prefix': 'example',
                              'prefix_reference': 'https://example.org/'},
                  'fair_mappings_schema': {'prefix_prefix': 'fair_mappings_schema',
                                           'prefix_reference': 'https://w3id.org/mapping-commons/fair-mappings-schema/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://mapping-commons.github.io/fair-mappings-schema'],
     'source_file': 'src/fair_mappings_schema/schema/fair_mappings_schema.yaml',
     'title': 'fair-mappings-schema'} )

class AgentTypeEnum(str, Enum):
    """
    Types of agents that can contribute to a mapping specification
    """
    person = "person"
    """
    An individual person
    """
    organization = "organization"
    """
    An organization or institution
    """
    software = "software"
    """
    A software tool or system
    """


class SourceTypeEnum(str, Enum):
    """
    Types of data sources
    """
    owl_ontology = "owl_ontology"
    """
    An ontology in OWL format
    """
    database = "database"
    """
    A relational or other database
    """
    skos_vocabulary = "skos_vocabulary"
    """
    A SKOS vocabulary or terminology
    """
    rdf_vocabulary = "rdf_vocabulary"
    """
    An RDF vocabulary or schema
    """
    schema = "schema"
    """
    A data schema or model
    """
    api = "api"
    """
    An API or web service
    """
    other = "other"
    """
    Other type of source
    """


class MappingSpecificationTypeEnum(str, Enum):
    """
    Types of mapping specifications
    """
    sssom = "sssom"
    """
    Simple Standard for Sharing Ontological Mappings
    """
    r2rml = "r2rml"
    """
    RDB to RDF Mapping Language
    """
    rml = "rml"
    """
    RDF Mapping Language
    """
    sparql = "sparql"
    """
    SPARQL-based mapping
    """
    custom = "custom"
    """
    Custom mapping format
    """



class Agent(ConfiguredBaseModel):
    """
    An entity that can create or contribute to a digital object, such as an author or creator.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema',
         'slot_usage': {'type': {'name': 'type', 'range': 'AgentTypeEnum'}}})

    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    version: Optional[str] = Field(default=None, description="""Version of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Optional[AgentTypeEnum] = Field(default=None, description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })


class Source(ConfiguredBaseModel):
    """
    A data source from which entities are drawn, such as a database, ontology, or vocabulary.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema',
         'slot_usage': {'type': {'name': 'type', 'range': 'SourceTypeEnum'}}})

    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    version: Optional[str] = Field(default=None, description="""Version of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Optional[SourceTypeEnum] = Field(default=None, description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    documentation: Optional[str] = Field(default=None, description="""URL or reference to documentation for the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'documentation', 'domain_of': ['Source', 'MappingSpecification']} })
    content: Optional[str] = Field(default=None, description="""Reference to the actual content of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'content', 'domain_of': ['Source', 'MappingSpecification']} })
    content_type: Optional[str] = Field(default=None, description="""The type of the content of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'content_type', 'domain_of': ['Source']} })


class MappingSpecification(ConfiguredBaseModel):
    """
    A formal description of correspondences between entities in a source and a target, expressed as rules, functions, or mapping statements.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema',
         'slot_usage': {'type': {'name': 'type',
                                 'range': 'MappingSpecificationTypeEnum'}},
         'tree_root': True})

    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    description: Optional[str] = Field(default=None, description="""A brief description of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['MappingSpecification']} })
    author: Optional[Agent] = Field(default=None, description="""Author of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'author', 'domain_of': ['MappingSpecification']} })
    creator: Optional[Agent] = Field(default=None, description="""Creator of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'creator', 'domain_of': ['MappingSpecification']} })
    reviewer: Optional[Agent] = Field(default=None, description="""Reviewer of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'reviewer', 'domain_of': ['MappingSpecification']} })
    publication_date: Optional[str] = Field(default=None, description="""Date of publication of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'publication_date', 'domain_of': ['MappingSpecification']} })
    license: Optional[str] = Field(default=None, description="""License under which the mapping specification is released""", json_schema_extra = { "linkml_meta": {'alias': 'license', 'domain_of': ['MappingSpecification']} })
    version: Optional[str] = Field(default=None, description="""Version of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Optional[MappingSpecificationTypeEnum] = Field(default=None, description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    mapping_method: Optional[str] = Field(default=None, description="""Method used to create the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'mapping_method', 'domain_of': ['MappingSpecification']} })
    documentation: Optional[str] = Field(default=None, description="""URL or reference to documentation for the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'documentation', 'domain_of': ['Source', 'MappingSpecification']} })
    content: Optional[str] = Field(default=None, description="""Reference to the actual content of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'content', 'domain_of': ['Source', 'MappingSpecification']} })
    subject_source: Optional[Source] = Field(default=None, description="""The source from which the subject entities are drawn""", json_schema_extra = { "linkml_meta": {'alias': 'subject_source', 'domain_of': ['MappingSpecification']} })
    object_source: Optional[Source] = Field(default=None, description="""The source from which the object entities are drawn""", json_schema_extra = { "linkml_meta": {'alias': 'object_source', 'domain_of': ['MappingSpecification']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Agent.model_rebuild()
Source.model_rebuild()
MappingSpecification.model_rebuild()


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
     'title': 'FAIR Mappings Schema'} )

class SourceTypeEnum(str, Enum):
    """
    Types of data sources
    """
    ontology = "ontology"
    """
    A conceptualization or formal representation of a domain, such as an OWL ontology.
    """
    database = "database"
    """
    A relational or other database
    """
    vocabulary = "vocabulary"
    """
    A controlled vocabulary or thesaurus, such as a SKOS vocabulary or an RDFS vocabulary.
    """
    schema = "schema"
    """
    A data schema or model, such as an XML Schema or JSON Schema.
    """
    api = "api"
    """
    An API or web service.
    """
    other = "other"
    """
    Other type of source.
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
    yarrrml = "yarrrml"
    """
    YARRRML mapping file
    """
    xslt = "xslt"
    """
    XSLT-based mapping
    """
    shacl = "shacl"
    """
    SHACL-based mapping
    """
    other = "other"
    """
    Other type of mapping specification
    """



class Agent(ConfiguredBaseModel):
    """
    An entity that can create or contribute to a digital object, such as an author or creator.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema',
         'slot_usage': {'type': {'designates_type': True,
                                 'name': 'type',
                                 'range': 'string'}}})

    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Literal["Agent"] = Field(default="Agent", description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'designates_type': True,
         'domain_of': ['Agent', 'Source', 'MappingSpecification']} })


class Person(Agent):
    """
    An individual person who contributes to a mapping specification
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema'})

    orcid: Optional[str] = Field(default=None, description="""ORCID identifier for a person""", json_schema_extra = { "linkml_meta": {'alias': 'orcid', 'domain_of': ['Person']} })
    affiliation: Optional[str] = Field(default=None, description="""Institutional affiliation of a person""", json_schema_extra = { "linkml_meta": {'alias': 'affiliation', 'domain_of': ['Person']} })
    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Literal["Person"] = Field(default="Person", description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'designates_type': True,
         'domain_of': ['Agent', 'Source', 'MappingSpecification']} })


class Organization(Agent):
    """
    An organization or institution that contributes to a mapping specification
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema'})

    ror_id: Optional[str] = Field(default=None, description="""ROR (Research Organization Registry) identifier""", json_schema_extra = { "linkml_meta": {'alias': 'ror_id', 'domain_of': ['Organization']} })
    url: Optional[str] = Field(default=None, description="""URL or web address""", json_schema_extra = { "linkml_meta": {'alias': 'url', 'domain_of': ['Organization']} })
    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Literal["Organization"] = Field(default="Organization", description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'designates_type': True,
         'domain_of': ['Agent', 'Source', 'MappingSpecification']} })


class Software(Agent):
    """
    A software tool or system used in creating mappings
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema'})

    version: Optional[str] = Field(default=None, description="""Version of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'version',
         'domain_of': ['Software', 'Source', 'MappingSpecification']} })
    repository_url: Optional[str] = Field(default=None, description="""URL to a code repository""", json_schema_extra = { "linkml_meta": {'alias': 'repository_url', 'domain_of': ['Software']} })
    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    type: Literal["Software"] = Field(default="Software", description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'designates_type': True,
         'domain_of': ['Agent', 'Source', 'MappingSpecification']} })


class Source(ConfiguredBaseModel):
    """
    A data source from which entities are drawn, such as a database, ontology, or vocabulary.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/mapping-commons/fair-mappings-schema',
         'slot_usage': {'type': {'name': 'type', 'range': 'SourceTypeEnum'}}})

    id: Optional[str] = Field(default=None, description="""Identifier for the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    name: Optional[str] = Field(default=None, description="""Name of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    version: Optional[str] = Field(default=None, description="""Version of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'version',
         'domain_of': ['Software', 'Source', 'MappingSpecification']} })
    type: Optional[SourceTypeEnum] = Field(default=None, description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    documentation: Optional[str] = Field(default=None, description="""URL or reference to documentation for the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'documentation', 'domain_of': ['Source', 'MappingSpecification']} })
    content_url: Optional[str] = Field(default=None, description="""Reference to the actual content of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'content_url', 'domain_of': ['Source', 'MappingSpecification']} })
    content_type: Optional[str] = Field(default=None, description="""The type of the content of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'content_type', 'domain_of': ['Source']} })
    metadata_url: Optional[str] = Field(default=None, description="""Reference to metadata about the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'metadata_url', 'domain_of': ['Source']} })
    metadata_type: Optional[str] = Field(default=None, description="""The type of the metadata about the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'metadata_type', 'domain_of': ['Source']} })


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
    author: Optional[Union[Agent,Person,Organization,Software]] = Field(default=None, description="""Author of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'author', 'domain_of': ['MappingSpecification']} })
    creator: Optional[Union[Agent,Person,Organization,Software]] = Field(default=None, description="""Creator of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'creator', 'domain_of': ['MappingSpecification']} })
    reviewer: Optional[Union[Agent,Person,Organization,Software]] = Field(default=None, description="""Reviewer of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'reviewer', 'domain_of': ['MappingSpecification']} })
    publication_date: Optional[str] = Field(default=None, description="""Date of publication of the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'publication_date', 'domain_of': ['MappingSpecification']} })
    license: Optional[str] = Field(default=None, description="""License under which the mapping specification is released""", json_schema_extra = { "linkml_meta": {'alias': 'license', 'domain_of': ['MappingSpecification']} })
    version: Optional[str] = Field(default=None, description="""Version of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'version',
         'domain_of': ['Software', 'Source', 'MappingSpecification']} })
    type: Optional[MappingSpecificationTypeEnum] = Field(default=None, description="""Type of the information entity""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Agent', 'Source', 'MappingSpecification']} })
    mapping_method: Optional[str] = Field(default=None, description="""Method used to create the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'mapping_method', 'domain_of': ['MappingSpecification']} })
    documentation: Optional[str] = Field(default=None, description="""URL or reference to documentation for the mapping specification""", json_schema_extra = { "linkml_meta": {'alias': 'documentation', 'domain_of': ['Source', 'MappingSpecification']} })
    content_url: Optional[str] = Field(default=None, description="""Reference to the actual content of the digital object""", json_schema_extra = { "linkml_meta": {'alias': 'content_url', 'domain_of': ['Source', 'MappingSpecification']} })
    subject_source: Optional[Source] = Field(default=None, description="""The source from which the subject entities are drawn""", json_schema_extra = { "linkml_meta": {'alias': 'subject_source', 'domain_of': ['MappingSpecification']} })
    object_source: Optional[Source] = Field(default=None, description="""The source from which the object entities are drawn""", json_schema_extra = { "linkml_meta": {'alias': 'object_source', 'domain_of': ['MappingSpecification']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Agent.model_rebuild()
Person.model_rebuild()
Organization.model_rebuild()
Software.model_rebuild()
Source.model_rebuild()
MappingSpecification.model_rebuild()


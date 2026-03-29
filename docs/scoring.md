# FAIR Scoring

The FAIR Mappings Schema includes a built-in scoring system that measures how completely a mapping specification describes itself. The more metadata you provide, the higher your score.

## The basic idea

Every field (slot) in a `MappingSpecification` has a **weight** from 0 to 5 that reflects how important it is for FAIRness. If you fill in a field, you earn its weight. If you leave it empty, you earn nothing. Your final FAIR score is the percentage of total possible points you actually earned.

```
FAIR score = total points earned / total points possible
```

A score of 1.0 means you filled in everything. A score of 0.0 means the specification is empty.

## Simple fields

Most fields are straightforward: they are either present or absent. For example:

| Field | Weight | You filled it in? | Points earned |
|---|---|---|---|
| id | 5 | Yes | 5 |
| license | 5 | Yes | 5 |
| version | 4 | No | 0 |
| description | 3 | Yes | 3 |

In this example you earned 13 out of 17 possible points from these four fields.

## Complex fields (nested objects)

Some fields like `author`, `creator`, `subject_source`, and `object_source` are not simple text values -- they are nested objects with their own sub-fields. For these, you don't just get full credit for filling them in. Instead, the score depends on **how completely** you filled in the nested object.

This is controlled by an **aggregation function** -- a formula that calculates a completeness ratio (0 to 1) based on which sub-fields are present.

### Example: the `author` field

The `author` field has weight **3** and the aggregation function:

```
(id*5 + name*1 + type*2) / 8
```

This means the `author` object has three sub-fields (`id`, `name`, `type`), each with their own importance weight. The formula works like this:

1. For each sub-field, substitute **1** if present, **0** if absent
2. Evaluate the formula to get a completeness ratio (0 to 1)
3. Multiply the completeness ratio by the field's weight to get points earned

**Scenario**: You provide an author with an `id` and a `name`, but no `type`:

```
completeness = (1*5 + 1*1 + 0*2) / 8 = 6/8 = 0.75
points earned = 3 (author weight) x 0.75 = 2.25
```

If you had filled in all three sub-fields:

```
completeness = (1*5 + 1*1 + 1*2) / 8 = 8/8 = 1.0
points earned = 3 x 1.0 = 3.0
```

### Example: the `subject_source` field

The `subject_source` field has weight **5** and the aggregation function:

```
(id*5 + name*2 + version*4 + type*2 + documentation*1 + content_url*0
 + content_type*0 + metadata_url*0 + metadata_type*0) / 14
```

Notice that some sub-fields like `content_url` and `metadata_url` have weight 0 -- they don't affect the score at all. The most important sub-fields are `id` (5) and `version` (4).

**Scenario**: You provide a source with `id`, `name`, and `version`:

```
completeness = (1*5 + 1*2 + 1*4 + 0*2 + 0*1 + 0*0 + 0*0 + 0*0 + 0*0) / 14
             = 11/14 = 0.786
points earned = 5 x 0.786 = 3.93
```

## Full weight table

### MappingSpecification (top-level)

| Field | Weight | Type |
|---|---|---|
| id | 5 | simple |
| license | 5 | simple |
| subject_source | 5 | complex (Source) |
| object_source | 5 | complex (Source) |
| version | 4 | simple |
| creator | 4 | complex (Agent) |
| description | 3 | simple |
| author | 3 | complex (Agent) |
| type | 2 | simple |
| name | 2 | simple |
| publication_date | 2 | simple |
| mapping_method | 2 | simple |
| documentation | 2 | simple |
| content_url | 0 | simple |
| reviewer | 0 | complex (Agent) |

### Agent sub-fields (used by author, creator, reviewer)

| Field | Weight in aggregation |
|---|---|
| id | 5 |
| type | 2 |
| name | 1 |

### Source sub-fields (used by subject_source, object_source)

| Field | Weight in aggregation |
|---|---|
| id | 5 |
| version | 4 |
| name | 2 |
| type | 2 |
| documentation | 1 |
| content_url | 0 |
| content_type | 0 |
| metadata_url | 0 |
| metadata_type | 0 |

## Worked example

Given this mapping specification:

```yaml
id: "https://example.org/my-mapping"
license: "CC-BY-4.0"
version: "1.0"
type: sssom
author:
  id: "https://orcid.org/0000-0001-1234-5678"
  name: "Jane Doe"
subject_source:
  id: "http://purl.obolibrary.org/obo/doid.owl"
  name: "Disease Ontology"
  version: "2024-01-01"
  type: ontology
```

The scoring works out as follows:

| Field | Weight | Earned | Calculation |
|---|---|---|---|
| id | 5 | 5.0 | present |
| license | 5 | 5.0 | present |
| version | 4 | 4.0 | present |
| type | 2 | 2.0 | present |
| author | 3 | 2.25 | (1\*5 + 1\*1 + 0\*2)/8 = 0.75, then 3 x 0.75 |
| subject_source | 5 | 4.64 | (1\*5 + 1\*2 + 1\*4 + 1\*2 + 0\*1 + ...)/14 = 0.929, then 5 x 0.929 |
| object_source | 5 | 0.0 | absent |
| creator | 4 | 0.0 | absent |
| description | 3 | 0.0 | absent |
| name | 2 | 0.0 | absent |
| publication_date | 2 | 0.0 | absent |
| mapping_method | 2 | 0.0 | absent |
| documentation | 2 | 0.0 | absent |
| content_url | 0 | 0.0 | absent (weight 0 anyway) |
| reviewer | 0 | 0.0 | absent (weight 0 anyway) |
| **Total** | **44** | **22.89** | |

```
FAIR score = 22.89 / 44 = 0.52
```

This specification is about halfway there -- adding an `object_source`, `creator`, and `description` would significantly improve the score.

## Using the CLI

You can score a mapping specification file from the command line:

```bash
fair-mappings score my-mapping.yaml
```

This prints a detailed breakdown of the score for each field along with the overall FAIR score.

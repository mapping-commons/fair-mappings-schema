"""Generate a single Mermaid class diagram covering every class in the schema.

LinkML's gen-mermaid-class-diagram writes one diagram per class, and gen-erdiagram
cannot show inheritance, so neither gives a whole-model picture.

Usage: python scripts/gen_class_diagram.py SCHEMA_YAML > OUTPUT_MD
"""

import sys

from linkml_runtime.utils.schemaview import SchemaView


def _cardinality(slot) -> str:
    low = "1" if slot.required else "0"
    high = "*" if slot.multivalued else "1"
    return low if low == high else f"{low}..{high}"


def class_diagram(schema_path: str) -> str:
    sv = SchemaView(schema_path)
    classes = sorted(sv.all_classes(imports=False))
    enums = set(sv.all_enums(imports=False))
    lines = ["classDiagram"]
    relations = []

    for name in classes:
        cls = sv.get_class(name)
        lines.append(f"    class {name} {{")
        if cls.abstract:
            lines.append("        <<abstract>>")
        for slot in sv.class_induced_slots(name):
            # Only slots the class declares itself; inherited ones show on the parent.
            if cls.is_a and slot.name in sv.class_slots(cls.is_a):
                continue
            rng = slot.range or sv.schema.default_range
            if rng in classes:
                relations.append(
                    f'    {name} --> "{_cardinality(slot)}" {rng} : {slot.name}'
                )
                continue
            suffix = "[]" if slot.multivalued else ""
            lines.append(f"        {rng}{suffix} {slot.name}")
            if rng in enums:
                relations.append(f"    {name} ..> {rng} : {slot.name}")
        lines.append("    }")
        if cls.is_a:
            relations.append(f"    {cls.is_a} <|-- {name}")

    for name in sorted(enums):
        lines.append(f"    class {name} {{")
        lines.append("        <<enumeration>>")
        for value in sv.get_enum(name).permissible_values:
            lines.append(f"        {value}")
        lines.append("    }")

    return "\n".join(["```mermaid", *lines, *relations, "```", ""])


if __name__ == "__main__":
    sys.stdout.write(class_diagram(sys.argv[1]))

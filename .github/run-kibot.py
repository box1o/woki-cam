#!/usr/bin/env python3
"""Run the pinned KiBot with a temporary KiCad 10 body-style compatibility fix."""

import sys
from io import StringIO
from importlib.util import find_spec, module_from_spec


def patch_source(source):
    # sexpdata represents quoted names as str and unquoted atoms as Symbol.
    # Preserve both token types: e.g. bare demorgan and quoted style names.
    replacements = (
        ("comp.body_styles = [v.value() for v in i[1:]]",
         "comp.body_styles = i[1:]"),
        ("_symbol('body_styles', [Symbol(v) for v in s.body_styles])",
         "_symbol('body_styles', s.body_styles)"),
    )
    for original, replacement in replacements:
        if source.count(original) != 1:
            raise RuntimeError(
                "Unexpected KiBot schematic parser; recheck/remove the KiCad 10 workaround."
            )
        source = source.replace(original, replacement)
    return source


def load_compatible_parser():
    # Patch only this process; do not edit installed packages or design files.
    name = "kibot.kicad.v6_sch"
    if name in sys.modules:
        raise RuntimeError("KiBot schematic parser loaded before compatibility fix")
    spec = find_spec(name)
    source = patch_source(spec.loader.get_source(name))
    parser = module_from_spec(spec)
    sys.modules[name] = parser
    exec(compile(source, spec.origin, "exec"), parser.__dict__)
    return parser


def check_body_styles(parser):
    marker = parser.Symbol("body_styles")
    styles = [parser.Symbol("demorgan"), "Outbound", 'Inbound "alternate"']
    component = parser.LibComponent.load(
        [parser.Symbol("symbol"), "Woki:Test", [marker, *styles]], "test"
    )
    reloaded = parser.LibComponent.load(
        parser.load(StringIO(parser.dumps(component.write(False))))[0], "test"
    )
    if component.body_styles != styles or reloaded.body_styles != styles:
        raise RuntimeError("KiBot no longer preserves KiCad 10 body-style tokens")


if __name__ == "__main__":
    check_body_styles(load_compatible_parser())
    if sys.argv[1:] != ["--check-compatibility"]:
        from kibot.__main__ import main
        sys.exit(main())

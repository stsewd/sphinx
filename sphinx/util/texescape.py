"""
    sphinx.util.texescape
    ~~~~~~~~~~~~~~~~~~~~~

    TeX escaping helper.

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from typing import Callable, Dict

tex_replacements = [
    # map TeX special chars
    ('$', r'\$'),
    ('%', r'\%'),
    ('&', r'\&'),
    ('#', r'\#'),
    ('_', r'\_'),
    ('{', r'\{'),
    ('}', r'\}'),
    ('\\', r'\textbackslash{}'),
    ('~', r'\textasciitilde{}'),
    ('^', r'\textasciicircum{}'),
    # map chars to avoid mis-interpretation in LaTeX
    ('[', r'{[}'),
    (']', r'{]}'),
    # map chars to avoid TeX ligatures
    # 1. ' - and , not here for some legacy reason
    # 2. no effect with lualatex (done otherwise: #5790)
    ('`', r'{}`'),
    ('<', r'\textless{}'),
    ('>', r'\textgreater{}'),
    # map char for some unknown reason.  TODO: remove this?
    ('|', r'\textbar{}'),
    # map special Unicode characters to TeX commands
    ('✓', r'\(\checkmark\)'),
    ('✔', r'\(\pmb{\checkmark}\)'),
    # used to separate -- in options
    ('﻿', r'{}'),
    # map some special Unicode characters to similar ASCII ones
    # (even for Unicode LaTeX as may not be supported by OpenType font)
    ('⎽', r'\_'),
    ('ℯ', r'e'),
    ('ⅈ', r'i'),
    # Greek alphabet not escaped: pdflatex handles it via textalpha and inputenc
    # OHM SIGN U+2126 is handled by LaTeX textcomp package
]

# A map Unicode characters to LaTeX representation
# (for LaTeX engines which don't support unicode)
unicode_tex_replacements = [
    # map some more common Unicode characters to TeX commands
    ('¶', r'\P{}'),
    ('§', r'\S{}'),
    ('€', r'\texteuro{}'),
    ('∞', r'\(\infty\)'),
    ('±', r'\(\pm\)'),
    ('→', r'\(\rightarrow\)'),
    ('‣', r'\(\rightarrow\)'),
    ('–', r'\textendash{}'),
    # superscript
    ('⁰', r'\(\sp{\text{0}}\)'),
    ('¹', r'\(\sp{\text{1}}\)'),
    ('²', r'\(\sp{\text{2}}\)'),
    ('³', r'\(\sp{\text{3}}\)'),
    ('⁴', r'\(\sp{\text{4}}\)'),
    ('⁵', r'\(\sp{\text{5}}\)'),
    ('⁶', r'\(\sp{\text{6}}\)'),
    ('⁷', r'\(\sp{\text{7}}\)'),
    ('⁸', r'\(\sp{\text{8}}\)'),
    ('⁹', r'\(\sp{\text{9}}\)'),
    # subscript
    ('₀', r'\(\sb{\text{0}}\)'),
    ('₁', r'\(\sb{\text{1}}\)'),
    ('₂', r'\(\sb{\text{2}}\)'),
    ('₃', r'\(\sb{\text{3}}\)'),
    ('₄', r'\(\sb{\text{4}}\)'),
    ('₅', r'\(\sb{\text{5}}\)'),
    ('₆', r'\(\sb{\text{6}}\)'),
    ('₇', r'\(\sb{\text{7}}\)'),
    ('₈', r'\(\sb{\text{8}}\)'),
    ('₉', r'\(\sb{\text{9}}\)'),
]

tex_escape_map = {}  # type: Dict[int, str]
tex_escape_map_without_unicode = {}  # type: Dict[int, str]
tex_replace_map = {}
tex_hl_escape_map_new = {}  # type: Dict[int, str]
tex_hl_escape_map_new_without_unicode = {}  # type: Dict[int, str]


def get_escape_func(latex_engine: str) -> Callable[[str], str]:
    """Get escape() function for given latex_engine."""
    if latex_engine in ('lualatex', 'xelatex'):
        return escape_for_unicode_latex_engine
    else:
        return escape


def escape(s: str) -> str:
    """Escape text for LaTeX output."""
    return s.translate(tex_escape_map)


def escape_for_unicode_latex_engine(s: str) -> str:
    """Escape text for unicode supporting LaTeX engine."""
    return s.translate(tex_escape_map_without_unicode)


def get_hlescape_func(latex_engine: str) -> Callable[[str], str]:
    """Get hlescape() function for given latex_engine."""
    if latex_engine in ('lualatex', 'xelatex'):
        return hlescape_for_unicode_latex_engine
    else:
        return hlescape


def hlescape(s: str) -> str:
    """Escape text for LaTeX highlighter."""
    return s.translate(tex_hl_escape_map_new)


def hlescape_for_unicode_latex_engine(s: str) -> str:
    """Escape text for unicode supporting LaTeX engine."""
    return s.translate(tex_hl_escape_map_new_without_unicode)


def escape_abbr(text: str) -> str:
    """Adjust spacing after abbreviations. Works with @ letter or other."""
    return re.sub(r'\.(?=\s|$)', r'.\@{}', text)


def init() -> None:
    for a, b in tex_replacements:
        tex_escape_map[ord(a)] = b
        tex_escape_map_without_unicode[ord(a)] = b
        tex_replace_map[ord(a)] = '_'

    for a, b in unicode_tex_replacements:
        tex_escape_map[ord(a)] = b
        tex_replace_map[ord(a)] = '_'

    for a, b in tex_replacements:
        if a in '[]{}\\':
            continue
        tex_hl_escape_map_new[ord(a)] = b
        tex_hl_escape_map_new_without_unicode[ord(a)] = b

    for a, b in unicode_tex_replacements:
        tex_hl_escape_map_new[ord(a)] = b

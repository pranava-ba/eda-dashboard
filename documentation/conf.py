"""Sphinx configuration for the EDA Dashboard documentation."""

project = "EDA Dashboard"
copyright = "2025–2026, BI Analytics"
author = "BI Analytics"
release = "3.0"

# -- General ----------------------------------------------------------------
extensions = [
    "myst_parser",          # write docs in Markdown
    "sphinx_design",        # cards, grids, badges
]

myst_enable_extensions = [
    "colon_fence",          # ::: fenced admonitions/directives
    "deflist",              # definition lists
    "linkify",              # bare URLs → links
    "attrs_inline",
]
myst_heading_anchors = 3    # auto-anchor headings for cross-links

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- HTML output ------------------------------------------------------------
# Default Furo theme (high-contrast, black-on-white) with lavender used only as
# a subtle brand/link accent — nothing that affects text readability.
html_theme = "furo"
html_title = "EDA Dashboard"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#4c3a8f",   # brand / sidebar highlight
        "color-brand-content": "#5a3fb3",   # links (~6.4:1 on white)
    },
    "dark_css_variables": {
        "color-brand-primary": "#cabcf6",
        "color-brand-content": "#cabcf6",
    },
    "sidebar_hide_name": False,
}

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

# -- HTML output (Furo + pastel-lavender theme) -----------------------------
html_theme = "furo"
html_title = "EDA Dashboard"
html_static_path = ["_static"]
html_css_files = ["lavender.css"]

# Pastel-lavender palette, expressed through Furo's CSS variables.
_LAVENDER = {
    "light_css_variables": {
        "color-brand-primary": "#6b4fb0",     # headings / brand
        "color-brand-content": "#7a5cc9",     # links
        "color-background-primary": "#fdfcff",
        "color-background-secondary": "#f3effc",  # sidebar / code blocks
        "color-background-hover": "#ece4fa",
        "color-background-border": "#e6ddf7",
        "color-foreground-primary": "#2c2543",    # body text
        "color-foreground-secondary": "#6a6284",
        "color-foreground-muted": "#8a83a3",
        "color-highlight-on-target": "#efe8fc",
        "color-api-background": "#f3effc",
        "color-inline-code-background": "#efe8fc",
        "color-admonition-title-background--note": "#ede6fb",
        "color-admonition-title--note": "#6b4fb0",
    },
    "dark_css_variables": {
        "color-brand-primary": "#c7b6f2",
        "color-brand-content": "#cbbaf6",
        "color-background-primary": "#161320",
        "color-background-secondary": "#1e1930",
        "color-background-hover": "#2a2340",
        "color-background-border": "#2c2542",
        "color-foreground-primary": "#e9e4f7",
        "color-foreground-secondary": "#b3aacb",
        "color-inline-code-background": "#241d38",
        "color-api-background": "#1e1930",
    },
    "sidebar_hide_name": False,
}
html_theme_options = _LAVENDER

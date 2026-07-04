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
        "color-brand-primary": "#463089",     # headings / brand (deep, high-contrast)
        "color-brand-content": "#553bad",     # links
        "color-background-primary": "#ffffff",     # white content = max readability
        "color-background-secondary": "#f6f3fc",   # sidebar / code blocks (subtle)
        "color-background-hover": "#ece5fa",
        "color-background-border": "#e3daf5",
        "color-foreground-primary": "#1c1830",     # body text (near-black)
        "color-foreground-secondary": "#4c4665",
        "color-foreground-muted": "#645d7c",
        "color-highlight-on-target": "#f0eafc",
        "color-api-background": "#f6f3fc",
        "color-inline-code-background": "#f0ecfa",
        "color-inline-code-foreground": "#5b3fae",
    },
    "dark_css_variables": {
        "color-brand-primary": "#cdc0f6",     # headings / brand
        "color-brand-content": "#d3c6f9",     # links
        "color-background-primary": "#15121f",
        "color-background-secondary": "#1e1930",
        "color-background-hover": "#2a2340",
        "color-background-border": "#2f2748",
        "color-foreground-primary": "#ece8f8",     # body text (bright)
        "color-foreground-secondary": "#bcb4d6",
        "color-foreground-muted": "#a49cc0",
        "color-inline-code-background": "#251e3a",
        "color-inline-code-foreground": "#cdbdf8",
        "color-api-background": "#1e1930",
    },
    "sidebar_hide_name": False,
}
html_theme_options = _LAVENDER

"""Sphinx configuration for the EDA Dashboard documentation."""

project = "EDA Dashboard"
copyright = "2025–2026, BI Analytics"
author = "BI Analytics"
release = "3.0"

# -- General ----------------------------------------------------------------
extensions = [
    "myst_parser",          # write docs in Markdown
]

myst_enable_extensions = [
    "colon_fence",          # ::: fenced directives
    "deflist",
    "linkify",              # bare URLs → links
]

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- HTML output ------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_title = "EDA Dashboard"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
    "style_external_links": True,
}

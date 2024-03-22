Sample repository structure to reference any amount of GitBook spaces in a MkDocs website.

MkDocs plugins to make it work:

- monorepo: https://github.com/backstage/mkdocs-monorepo-plugin
- custom hook directly based on https://github.com/pledra/gitbook2mkdocs

For this setup to work:

- each GitBook space must be synced to their own diretory <gitbook_space>/docs/
- as per the monorepo documentation, there must be a mkdocs.yaml in <gitbook_space> directory with at minimum `site_name` configuration and the main mkdocs.yaml needs to reference a GitBook space with `!include`

Caveat: this solution implies that you need to write the `nav` section that matches the content of GitBook's SUMMARY.md. MkDocs will generate a nav section for you if you don't but it will not be ordered as it is on GitBook. There may be a way to write a hook or plugin to alleviate this situation.

Note: I only tested this with Python 3.11 and the package versions mentionned in requirements.txt.

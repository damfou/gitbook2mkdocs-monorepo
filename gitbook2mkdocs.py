# noinspection SpellCheckingInspection
"""
A hook to convert GitBook markdown to MkDocs markdown.
Directly adapted from https://github.com/pledra/gitbook2mkdocs, without the conversion of .gitbook/assets/ to gbassets/
See also: https://www.mkdocs.org/user-guide/configuration/#hooks on how to write hooks
"""
import re


def remove_escaping_chars(content):
    # Function to remove escaping characters between colons
    def process_match(match):
        return match.group(1) + match.group(2).replace("\\", "") + match.group(3)

    content = re.sub(r"(:)(.*?)(:)", process_match, content)
    return content


# noinspection SpellCheckingInspection
def replace_figures_with_images(markdown):
    # Find all occurrences of <figure><img src="..."><figcaption>...</figcaption></figure>
    # and replace them with ![...](...)
    markdown = re.sub(
        r'<figure><img src="(.*?)" alt="(.*?)"><figcaption>.*?</figcaption></figure>',
        r"![\2](\1)",
        markdown,
    )

    return markdown


# noinspection SpellCheckingInspection
def convert_tabs(content):
    # Function to change gitbook tab format into mkdocs tab format
    # Replace {% tabs %} with an empty string (not needed in the target format)
    content = re.sub(r"{% tabs %}", "", content)

    # Replace {% endtabs %} with an empty string (not needed in the target format)
    content = re.sub(r"{% endtabs %}", "", content)

    # Replace {% tab title="Title" %} with the respective tab title
    content = re.sub(r'{% tab title="([^"]+)" %}', r'=== "\1"', content)

    # Replace {% endtab %} with an empty string (not needed in the target format)
    content = re.sub(r"{% endtab %}", "", content)

    # Indent content within tabs
    tab_content_pattern = r'(=== ".*?")((?:\r?\n)(?:(?!\r?\n===).)*)(\r?\n)'

    def indent_content(match):
        title = match.group(1)
        content_ = "    " + match.group(2).strip().replace("\n", "\n    ")
        return "{}\n{}\n".format(title, content_)

    content = re.sub(tab_content_pattern, indent_content, content)

    return content


# noinspection SpellCheckingInspection
def convert_hints(content):
    # Replace gitbook hint blocks with admonition
    def indent_text(match):
        hint_style = match.group(1)
        inner_text = match.group(2).rstrip()
        indented_text = inner_text.replace("\n", "\n    ")
        return f"!!! {hint_style}\n    {indented_text}\n"

    pattern = r'{% hint style="([a-zA-Z]+)" %}\s*(.*?)\s*{% endhint %}'
    return re.sub(pattern, indent_text, content, flags=re.DOTALL)


def replace_gitbook_syntax(content):
    # Function to replace GitBook syntax with MkDocs Admonition syntax
    # Remove all gitbook specific [^1] values
    # noinspection RegExpRedundantEscape
    content = re.sub(r"\[\^1\]:?", "", content)

    # Remove content-ref tags and keep only the text between the tags
    content = re.sub(r"{% content-ref %}(.*?){% endcontent-ref %}", r"\1", content)

    # Remove content-ref tags
    content = re.sub(
        r"{%[\w\s]+?content-ref\s*.*?%}(.*?)\{%[\w\s]+?endcontent-ref\s*.*?%}",
        r"\1",
        content,
        flags=re.DOTALL,
    )

    content = convert_hints(content)
    content = convert_tabs(content)
    return content


# noinspection SpellCheckingInspection,PyUnusedLocal
def on_page_markdown(markdown, **kwargs):
    # Replace GitBook syntax with MkDocs syntax
    markdown = replace_gitbook_syntax(markdown)

    # Replace HTML figures with Markdown images
    markdown = replace_figures_with_images(markdown)

    return markdown

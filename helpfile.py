# helpfile.py
import markdown2

help_md_content = """

LinkMaster is a Python-based GUI application that allows users to create different types of links between directories and files. It provides an easy-to-use interface for creating directory junctions, symbolic links, and directory links.

## <u>Types of Links</u>
- <b>Directory Junction</b>: A directory junction is a type of link that redirects to another directory in the file system. It's similar to a shortcut, but appears to applications as if it's a real directory.
- <b>Symbolic Link</b>: A symbolic link is a file that points to another file or directory. It's similar to a directory junction, but can also point to files.
- <b>Directory Link</b>: A directory link is a special type of link that behaves like a shortcut to a directory, but appears to the operating system and applications as a normal directory.

## <u>Usage</u>
1. Click the type of link you want to create: Directory Junction, Symbolic Link, or Directory Link.
2. When prompted, select the source and target directories or files using the provided fields.
3. Click the 'Generate Links' button to create the link.
"""

def get_html_content():
    return markdown2.markdown(help_md_content)


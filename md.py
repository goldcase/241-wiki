import markdown, gfm, os, urllib, mcq_hammertime, sys, re
from io import open
from bs4 import BeautifulSoup

# Set default encoding.
reload(sys)
sys.setdefaultencoding('Cp1252')

HEAD_FILE = "head.html"
TAIL_FILE = "tail.html"

cur_dir = os.path.dirname(__file__)
md_dir = os.path.join(cur_dir, "md-files")
#output_dir = os.path.join(cur_dir, "gh-pages")
output_dir = os.path.join(cur_dir, "sys-gh-pages")

# Get all markdown files in md-dir.
files = [f for f in os.listdir(md_dir) if os.path.isfile(os.path.join(md_dir, f)) if f.endswith(".md")]
# Initialize extension
mcq = mcq_hammertime.MCExtension()
md = markdown.Markdown(extensions = ['gfm', mcq])

with open(os.path.join(cur_dir, HEAD_FILE), "r") as head:
    head_text = head.read()

with open(os.path.join(cur_dir, TAIL_FILE), "r") as tail:
    tail_text = tail.read()

def sanitize(filename):
    return re.sub(r'\W+', '', filename.lower())

for l in files:
    with open(os.path.join(md_dir, l), mode="r", encoding="utf8") as f:
        string = f.read()
        # Run the parser.
        html = md.reset().convert(string)
        stripped = sanitize(l).rstrip(".md")
        with open(os.path.join(output_dir, stripped + ".html"), mode="w") as f_target:
            f_target.write(head_text.format(l.rstrip(".md").replace("-", " ")) + html + tail_text)

def convert_wiki_link(soup, link_text):
    wiki_name = link_text.lstrip("[[").rstrip("]]").strip()
    link = sanitize(wiki_name) + ".html"
    new_tag = soup.new_tag("a")
    new_tag["href"] = link
    new_tag.string = wiki_name
    return new_tag

def create_index(filenames):
    with open(os.path.join(output_dir, "home.html"), mode="r", encoding="utf8") as f:
        soup = BeautifulSoup(f, "html.parser")
        all_wiki_links = soup.find_all("li")
        for link in all_wiki_links:
            if link.string is not None and link.string.startswith("[["):
                link.string.replace_with(convert_wiki_link(soup, link.string))
        with open(os.path.join(output_dir, "index.html"), mode="w", encoding="utf8") as idx_file:
            idx_file.write(soup.prettify())
#            idx_file.write(unicode("<li><a href='{0}'>{1}</a></li><br />".format(unicode(stripped), html_filename)))
#        idx_file.write("</ol><br />" + tail_text)

if __name__ == "__main__":
    create_index(files)

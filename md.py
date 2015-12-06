import markdown, gfm, os, urllib, mcq_hammertime, sys, re
from io import open

reload(sys)
sys.setdefaultencoding('Cp1252')

HEAD_FILE = "head.html"
TAIL_FILE = "tail.html"

cur_dir = os.path.dirname(__file__)
md_dir = os.path.join(cur_dir, "md-files")
output_dir = os.path.join(cur_dir, "gh-pages")

# Get all markdown files in md-dir.
files = [f for f in os.listdir(md_dir) if os.path.isfile(os.path.join(md_dir, f)) if f.endswith(".md")]
# Initialize extension
mcq = mcq_hammertime.MCExtension()
md = markdown.Markdown(extensions = ['gfm', mcq])

with open(os.path.join(cur_dir, HEAD_FILE), "r") as head:
    head_text = head.read()

with open(os.path.join(cur_dir, TAIL_FILE), "r") as tail:
    tail_text = tail.read()

def escape_url(url):
    return url

def sanitize(filename):
    return re.sub(r'\W+', '', filename.lower())

for l in files:
    with open(os.path.join(md_dir, l), mode="r", encoding="utf8") as f:
        string = f.read()
        html = md.reset().convert(string)
        sanitized = sanitize(l)
        stripped = escape_url(sanitized.rstrip(".md"))
        with open(os.path.join(output_dir, stripped + ".html"), mode="w") as f_target:
            f_target.write(head_text.format(l.rstrip(".md").replace("-", " ")) + html + tail_text)

def create_index(filenames):
    with open(os.path.join(output_dir, "index.html"), mode="w", encoding="utf8") as idx_file:
        idx_file.write(head_text.format("Table of Contents") + "<br /><ol>")
        for filename in filenames:
            html_filename = filename.rstrip(".md") + ".html"
            sanitized = sanitize(filename)
            stripped = escape_url(sanitized.rstrip(".md")) + ".html"
            idx_file.write(unicode("<li><a href='{0}'>{1}</a></li><br />".format(unicode(stripped), html_filename)))
        idx_file.write("</ol><br />" + tail_text)

if __name__ == "__main__":
    create_index(files)

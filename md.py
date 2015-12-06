import markdown, gfm, os
import mcq_hammertime
import sys

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

def sanitize(filename):
    return filename.replace(":", "").lower()

for l in files:
    with open(os.path.join(md_dir, l), "r") as f:
        string = f.read()
        html = md.reset().convert(string)
        sanitized = sanitize(l)
        stripped = sanitized.rstrip(".md")
        with open(os.path.join(output_dir, stripped + ".html"), "w") as f_target:
            f_target.write(head_text.format(l.rstrip(".md").replace("-", " ")) + html + tail_text)

def create_index(filenames):
    with open(os.path.join(output_dir, "index.html"), "w") as idx_file:
        idx_file.write(head_text.format("Table of Contents") + "<br /><ol>")
        for filename in filenames:
            html_filename = filename.rstrip(".md") + ".html"
            sanitized = sanitize(filename)
            stripped = sanitized.rstrip(".md") + ".html"
            idx_file.write("<li><a href='{0}'>{1}</a></li><br />".format(stripped, html_filename))
        idx_file.write("</ol><br />" + tail_text)

if __name__ == "__main__":
    create_index(files)

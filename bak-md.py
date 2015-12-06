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

for l in files:
    with open(os.path.join(md_dir, l), "r") as f:
        string = f.read()
        html = md.reset().convert(string)
        with open(os.path.join(output_dir, l.rstrip(".md") + ".html"), "w") as f_target:
            with open(os.path.join(cur_dir, HEAD_FILE), "r") as head:
                f_target.write(head.read().format(l.rstrip(".md")))
            f_target.write(html)
            with open(os.path.join(cur_dir, TAIL_FILE), "r") as tail:
                f_target.write(tail.read())

def create_index(filenames):
    with open(os.path.join(output_dir, "index.html"), "w") as idx_file:
        with open(os.path.join(cur_dir, HEAD_FILE), "r") as head:
            idx_file.write(head.read().format("Table of Contents"))
        for filename in filenames:
            html_filename = filename.rstrip(".md") + ".html"
            idx_file.write("<a href='" + html_filename + "'>" + html_filename + "</a><br />")
        with open(os.path.join(cur_dir, TAIL_FILE), "r") as tail:
            idx_file.write(tail.read())

if __name__ == "__main__":
    create_index(files)

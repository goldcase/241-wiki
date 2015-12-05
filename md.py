import markdown, gfm, os
import mcq_hammertime
import sys

reload(sys)
sys.setdefaultencoding('Cp1252')

cur_dir = os.path.dirname(__file__)
md_dir = os.path.join(cur_dir, "md-files")
output_dir = os.path.join(cur_dir, "output")

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
            with open(os.path.join(cur_dir, "head.html"), "r") as head:
                f_target.write(head.read())
            f_target.write(html)
            with open(os.path.join(cur_dir,"tail.html"), "r") as tail:
                f_target.write(tail.read())

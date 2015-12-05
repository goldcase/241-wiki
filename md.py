import markdown, gfm, os
import mcq_hammertime

cur_dir = os.path.dirname(__file__)
md_dir = os.path.join(cur_dir, "md-files")
output_dir = os.path.join(cur_dir, "output")

# Get all markdown files in md-dir.
files = [f for f in os.listdir(md_dir) if os.path.isfile(os.path.join(md_dir, f)) if f.endswith(".md")]

for f in files:
    with open(f, "r") as f:
        string = f.read()
        mcq = mcq_hammertime.MCExtension()
        html = markdown.markdown(string, extensions=['gfm', mcq])
        with open(os.path.join(output_dir, "synchronization-converted.html"), "w") as f_target:
            with open(os.path.join(cur_dir, "head.html"), "r") as head:
                f_target.write(head.read())
            f_target.write(html)
            with open(os.path.join(cur_dir,"tail.html"), "r") as tail:
                f_target.write(tail.read())

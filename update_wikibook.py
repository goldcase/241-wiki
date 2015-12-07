import os, datetime
from time import sleep

while True:
    print "Performing a check."
    os.chdir("md-files")
    os.system("git pull")
    sleep(5)
    os.chdir(os.pardir)
    os.system("python md.py")
    sleep(5)
    os.chdir("sys-gh-pages")
    os.system("git add --all .")
    sleep(5)
    os.system("git commit -m 'Detected change at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".'")
    sleep(5)
    os.system("git push origin gh-pages")
    sleep(5)
    os.chdir(os.pardir)
    sleep(30)

import os, datetime
from time import sleep

while True:
    os.chdir("md-files")
    os.system("git pull")
    sleep(2)
    os.chdir(os.pardir)
    os.system("python md.py")
    sleep(3)
    os.chdir("gh-pages")
    os.system("git add .")
    os.system("git commit -m 'Detected change at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".'")
    sleep(1)
    os.system("git push origin gh-pages")
    sleep(2)
    os.chdir(os.pardir)
    sleep(30)

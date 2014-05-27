# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# How to get started?
# 
# [Home - Evernote Developers](http://dev.evernote.com/)
# 
# [evernote/evernote-sdk-python](https://github.com/evernote/evernote-sdk-python)
# 
#     git clone https://github.com/evernote/evernote-sdk-python.git
# 
# get a dev token (that will give you access to your own account) at [Developer Tokens](https://www.evernote.com/api/DeveloperToken.action) and work through [Evernote Cloud API — Python Quick-start Guide - Evernote Developers](http://dev.evernote.com/doc/start/python.php)
# 
# see more [rdhyee/evernote-web-utility](https://github.com/rdhyee/evernote-web-utility)

# <codecell>

from settings import EVERNOTE_DEV_TOKEN
from evernote.api.client import EvernoteClient

# <codecell>

# https://gist.githubusercontent.com/evernotegists/5313860/raw/example.py
# note the sandbox=False

client = EvernoteClient(token=EVERNOTE_DEV_TOKEN, sandbox=False)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

# <codecell>



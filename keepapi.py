import gkeepapi
import keyring
import os
import json
from secret_values import *


keep = gkeepapi.Keep()


print("Loading state")
state = None
if os.path.exists("state"):
    # Load cache
    fh = open('state', 'r')
    state = json.load(fh)
    keep.restore(state)


print("Logging in")
token = keyring.get_password('google-keep-token', email)
if token is None:
    success = keep.login(email, app_password, state=state if state is not None else None)

    if success:
        token = keep.getMasterToken()
        keyring.set_password('google-keep-token', email, token)
else:
    keep.resume(email, token, state=state if state is not None else None)
    

print("Syncing")
keep.sync()

print("Dumping Sync")
# Store cache
state = keep.dump()
fh = open('state', 'w')
json.dump(state, fh)






print("Work")
# https://gkeepapi.readthedocs.io/en/latest/#caching-notes

# Find by labels
gnotes = keep.find(labels=[keep.findLabel('daily')], archived=False, trashed=False)

count = 0
for gnote in gnotes:
    count += 1
    for line in gnote.items:
        print(line)
    break
print(count)

#note = keep.createNote('Todo', 'Eat breakfast')
#note.pinned = True
#note.color = gkeepapi.node.ColorValue.Red
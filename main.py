
import sys
import re
import subprocess
from time import time, sleep
import json
import names

TIMESPAN = 30 #seconds

store = {}

def process( rfid ):
    global store
    now = time()
    if rfid not in store:
        name = names.buildname()
        # TODO: Check whether or not the name already exists.
        store[rfid] = {'latest': -1, 'score': 0, 'checkins': [], 'rfid': rfid, 'name': name, 'multiplier': 1}
    store[rfid]['checkins'].append(now)
    if now-store[rfid]['latest'] < TIMESPAN:
        return
    store[rfid]['latest'] = now
    store[rfid]['score'] += store[rfid]['multiplier'];

    refresh()
    commit()

def refresh():
    print chr(27) + "[2J"
    result = sorted( store.values(), key=lambda i: i['score'], reverse=True )
    i = 1
    for e in result[:10]:
        print str(i) + ". ", e['rfid'], e['name'], e['score']
        i += 1

def init():
    global store
    try:
        with open("spaceworkers.json") as fp:
            store = json.load(fp)
    except:
        pass

def commit():
    global store
    with open("spaceworkers.json", "w") as fp:
        json.dump(store, fp, indent=4)

def main():

    init()



    rx = re.compile("UID.*: ([0-9a-f ]+)$")

    while True:
        refresh()
        try:
            raw = subprocess.check_output(["nfc-poll"], shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            continue
        for line in raw.splitlines():
            if "UID" in line:
                match = rx.search(line)
                if match:
                    rfid = match.group(1).replace(" ", "")
                    process(rfid)


if __name__ == "__main__":
    main()

# vim: expandtab tabstop=4 softtabstop=4 shiftwidth=4 textwidth=79:

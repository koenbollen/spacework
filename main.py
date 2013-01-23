
import sys
from time import time, sleep    
import json

TIMESPAN = 30 #seconds

store = {}

def process( rfid ):
    global store
    now = time()
    if rfid not in store:
        store[rfid] = {'latest': -1, 'score': 0, 'checkins': [], 'rfid': rfid, 'name': "John Doe", 'multiplier': 1}
        
    store[rfid]['checkins'].append(now)
    if now-store[rfid]['latest'] < TIMESPAN:
        return
    
    store[rfid]['latest'] = now
    store[rfid]['score'] += store[rfid]['multiplier'];
    
    refresh()
    commit()
    
def refresh():
    print chr(27) + "[2J"
    result = sorted( store.values(), key=lambda i: i['score'] )
    for e in result[:10]:
        print e['rfid'], e['name'], e['score']
    
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
    
    while True:
        raw_input("press enter for face rfid")
        rfid = "a191c715"
        process( rfid )
        sleep(1) # emulate delay of rfid reader?


if __name__ == "__main__":
    main()
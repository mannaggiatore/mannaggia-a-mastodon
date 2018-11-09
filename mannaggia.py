#!/usr/bin/env python3

import re
import os
import sys
import random
import time
import argparse

IMPRECAZIONE = "Mannaggia"
DB_FILE = "santi_e_beati.txt"

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dec"]
MONTH31 = ["jan","mar","may","jul","ago","oct","dec"]
MONTH30 = ["apr","jun","sep","nov"]


parser = argparse.ArgumentParser(prog="mannaggia-nocloud")
parser = argparse.ArgumentParser(description='Mannaggiatore senza audio')
parser.add_argument('-f','--file', help='db file to read',
                    required=False, default=DB_FILE)
parser.add_argument('-w','--wait', help='wait time in seconds between one amnnaggia and the other',
                    type=int, required=False, default=3)
parser.add_argument('-d','--date', help='do the mannaggia for a specific date like "1 jan" or "23 dec"',
                    required=False)
parser.add_argument('-r','--random', help='random day for santi e beati', action="store_true",
                    default=False, required=False)
parser.add_argument('-c', '--count', help='numero di mannagge', type=int, default=1, required=False)
args = parser.parse_args()

def random_saints():
    db = args.file
    if args.random:
        rm = random.choice(MONTHS)
        if rm == "feb":
            today = str(random.choice(range(1, 28))) + " " + rm
        if rm in MONTH30 :
            today = str(random.choice(range(1, 30))) + " " + rm
        if rm in MONTH31 :
            today = str(random.choice(range(1, 31))) + " " + rm
    else:
        if args.date is not None:
            today = args.date
        else:
            today = time.strftime("%d" + " " + "%b").lower().lstrip("0")
    santig = ''
    for line in open(db, 'r'):
        if today in line:
            santig = line
            break
    santi = re.split('\:|\;|\.', santig)
    del santi[0]
    return santi

def run():
    global_counter = 0
    count = 0
    hard_limit = args.count + 1000
    while True:
        global_counter += 1
        if global_counter > hard_limit:
            print('Sorry, niente mannaggia per oggi')
            break
        try:
            santi = random_saints()
        except:
            raise
            continue
        if not santi:
            continue
        rand_mannaggia = random.choice(santi).strip()
        if not rand_mannaggia:
            continue
        lower_mannaggia = rand_mannaggia.lower()
        if lower_mannaggia.startswith(('madonna ', 'nostra madonna ',
                                    'maria ', 'dedicazione ')):
            articolo = " alla"
        elif lower_mannaggia.startswith(('sante ', 'beate ')):
            articolo = " alle"
        elif lower_mannaggia.startswith(('santi ', 'beati ', 'papi ')):
            articolo = " ai"
        elif lower_mannaggia.startswith(('papa ', 'natale ')):
            articolo = " al"
        else:
            articolo = " a"
        mannaggia =  IMPRECAZIONE + articolo + " " + rand_mannaggia
        if not mannaggia:
            continue
        print(mannaggia)
        sys.stdout.flush()
        count += 1
        if args.count > 0 and count >= args.count:
            break
        time.sleep(args.wait)

if __name__ == '__main__':
    run()

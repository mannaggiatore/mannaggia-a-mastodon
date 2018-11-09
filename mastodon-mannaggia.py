#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from mastodon import Mastodon

API_URL = 'https://botsin.space/'

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


def getMannaggia():
    cmd = ['/mannaggia.py']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    try:
        stdout = stdout.strip()
        stdout = stdout.decode('utf8')
    except:
        return 'uh-oh: something was wrong with the encoding of the mannaggia; try again'
    if process.returncode != 0:
        return 'something terrible is happening: exit code: %s, stderr: %s' % (
                process.returncode, stderr.decode('utf8'))
    if not stdout:
        return 'sadness: the mannaggia was empty; try again'
    return stdout


def serve(token):
    mannaggia = getMannaggia()
    print('serving:\n%s' % mannaggia)
    mastodon = Mastodon(access_token=token, api_base_url=API_URL)
    mastodon.status_post(mannaggia)


if __name__ == '__main__':
    if 'MANNAGGIABOT_TOKEN' not in os.environ:
        print("Please specify the Mastodon token in the MANNAGGIABOT_TOKEN environment variable")
        sys.exit(1)
    serve(token=os.environ['MANNAGGIABOT_TOKEN'])

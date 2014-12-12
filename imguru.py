#!/usr/bin/env python
from __future__ import print_function
from imgurpython import ImgurClient as imgur
import webbrowser
import os.path
import sys
import requests
import json
from imgurpython.helpers.error import ImgurClientError
client_id = '0ee25e395ec9569'
client_secret = '400182ea3b3818efcaae28d8614fef3df2713400'
log = 'imguru.log'
SUPPORTED = ['.png', '.jpg', '.jpeg', '.gif']


def connect(client_id, client_secret):
    try:
        client = imgur(client_id, client_secret)
        return True, client
    except ImgurClientError as e:
        return False, e.error_message
    except:
        return False, sys.exc_info()[0]


def file_upload(client, filename):
    try:
        response = client.upload_from_path(filename)
        link = response.get('link', False)
        return True, response, filename
    except ImgurClientError as e:
        return False, e.error_message, filename
    except:
        return False, sys.exc_info()[0], filename


def dir_upload(client, path):
    for root, dirs, files in os.walk(path):
        for fname in files:
            if os.path.splitext(fname)[-1].lower() in SUPPORTED:
                yield file_upload(client, os.path.join(root, fname))


def make_album(**kwargs):
    payload = {'data': kwargs}
    url = 'http://thekindlyone.co.in/imguru/create'
    try:
        r = requests.post(url, data=json.dumps(payload))
        if r.status_code == 200:
            return True, r.content
        else:
            return False, r.status_code
    except:
        return False, sys.exc_info()[0]


def main():
    path = os.path.expanduser(sys.argv[1])
    if not os.path.exists(path):
        print(" ERROR: {} not found.".format(path))
        sys.exit(1)

    ok, response = connect(client_id, client_secret)
    if ok:
        client = response
    else:
        print("cannot connect")
        sys.exit(1)

    if os.path.isdir(path):  # entire directory
        print ('directory detected ')
        title = os.path.split(
            path)[-1] if path != '.' else os.path.split(os.getcwd())[-1]
        ids = []
        links = []
        for ok, result, filename in dir_upload(client, path):
            if ok:
                ids.append(result.get('id'))
                links.append(result.get('link'))
                print('Uploaded {} to {}'.format(
                    os.path.basename(filename),
                    result.get('link')))
            else:
                print('Error uploading {}. Info: {}'.format(
                    filename, result))

        ok, content = make_album(title=title, links=links)
        if ok:
            print ("Album Created! title: {} url: {}".format(
                title,
                content))
            webbrowser.open(content)
        else:
            print("Cannot create album. Info: {}".format(content))
    else:  # single file
        ok, response, _ = file_upload(client, path)
        if ok:
            print("Uploaded {} to {}".format(
                os.path.basename(path),
                response.get('link')))
            webbrowser.open(response.get('link'))
        else:
            print("Error uploading {}  Info: {}".format(
                path,
                response))


if __name__ == '__main__':
    main()

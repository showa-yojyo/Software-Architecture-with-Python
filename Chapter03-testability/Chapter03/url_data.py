# Code Listing #1
# 末尾の get_url_data() だけ押さえれば十分。
# open() したファイルを close() していないのが気になる。
import os
import hashlib # これが急所
import requests


def get_url_data(url):
    """ Return data for a URL """

    # Return data while saving the data in a file
    # which is a hash of the URL
    data = requests.get(url).content
    # Save it in a filename
    # URL 文字列だけでファイル名を一貫性を保って決定する。
    filename = hashlib.md5(url).hexdigest()
    with open(filename, 'wb') as f:
        f.write(data)
    return data


def get_url_data_stub(url):
    """ Stub function replacing get_url_data """

    # No actual web request is made, instead
    # the file is opened and data returned
    filename = hashlib.md5(url).hexdigest()
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except OSError:
        return None


def get_url_data(url):
    """ Return data for a URL """

    # First check for cached file - if so return its
    # contents. Note that we are not checking for
    # age of the file - so content may be stale.
    filename = hashlib.md5(url).hexdigest()
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except OSError:
        pass

    # First time - so fetch the URL and write to the
    # file. In subsequent calls, the file contents will
    # be returned.
    data = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(data)

    return data

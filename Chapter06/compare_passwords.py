#!/usr/bin/env python
# Code Listing #14

"""

Comparing passwords in memory - using simple hashes

"""

import hashlib
import sqlite3
import getpass # 標準モジュール


def read_password(user):
    """ Read password from a password DB """
    # Using an sqlite db for demo purpose

    # ('jack', 'reacher123')
    # ('frodo', 'ring123')
    db = sqlite3.connect('passwd.db')
    cursor = db.cursor()
    try:
        # SQL 文を組み立てるのに %s を使ってはならない
        #passwd = cursor.execute(
        #    "select password from passwds where user='%(user)s'" % locals()).fetchone()[0]
        passwd = cursor.execute(
            "select password from passwds where user=?", (user,)).fetchone()[0]
        # 急所
        return hashlib.sha1(passwd.encode('utf-8')).hexdigest()
    except TypeError:
        pass


def verify_password(user):
    """ Verify password for user """

    hash_pass = hashlib.sha1(getpass.getpass(
        "Password: ").encode('utf-8')).hexdigest() # 急所
    print(hash_pass)
    if hash_pass == read_password(user):
        print('Password accepted')
    else:
        print('Wrong password, Try again')


if __name__ == "__main__":
    import sys
    verify_password(sys.argv[1])

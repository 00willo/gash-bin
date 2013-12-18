#!/usr/bin/python

# Simple script to set a user's SHA-1 password in a mysql database for freeradius.  It will create the user entry in the radcheck tables if it doesn't exist.

import MySQLdb
import hashlib
import getpass
import sys

user_exists = False

try:
        radiusconn = MySQLdb.connect (host = "localhost", user = "root",passwd = "", db = "radius")
except:
        print "I am unable to connect to the radius database"
        sys.exit(1)

radcur = radiusconn.cursor (MySQLdb.cursors.DictCursor)

user = raw_input('Set password for which user : ')
radcur.execute("select * from radcheck where username = %s", (user)) 
rows = radcur.fetchall()
if rows:
        print('User already exists')
        print('This will reset your password')
        user_exists = True
while True:
    passwd = getpass.getpass(prompt='Enter a password : ')
    passwd2 = getpass.getpass(prompt='Please re-enter the password : ')
    if passwd == passwd2:
        break
    else:
        print('Password do not match')
    
h = hashlib.sha1(passwd).hexdigest()
print("Hash: %s") % h
if not user_exists:
        sql = "insert into radcheck (username, attribute, op, value) values (\"%s\", \"SHA-Password\", \":=\", \"%s\");" % (user, h)
        print("Inserting password")
else:
        sql = "update radcheck set attribute = \"SHA-Password\", op = \":=\", value = \"%s\" where username = \"%s\"" % (h, user) 
        print("Updating password")
print sql
try:
  # Execute the SQL command
  radcur.execute(sql)
except:
        print("Error on doing the sql bit")
        sys.exit(1)

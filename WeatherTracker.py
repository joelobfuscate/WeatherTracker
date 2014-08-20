#!/usr/bin/env python

import json
import urllib2
import sqlite3
import time

# Get temperature
while True:

	f=urllib2.urlopen('http://api.wunderground.com/api/e260c734250b742d/conditions/q/CA/Mountain_View.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = 'Mountain View'
	try:
		temp_f = parsed_json['current_observation']['temp_f']

	except:
		print parsed_json['response']
		continue
	print 'Current temperature in {} is {}'.format(location,temp_f)
	f.close()
	
	conn = sqlite3.connect('test.db')
	c=conn.cursor()
	try:
		c.execute('CREATE TABLE Temp(time REAL,temp_f REAL)')
	except:
		pass
	data=(time.time(),temp_f)
	c.execute('INSERT INTO Temp VALUES(?,?)',data)
	
	conn.commit()
	conn.close()

	time.sleep(180)
	

#!/usr/bin/env python

import json
import urllib2
import sqlite3
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import dropbox as dbox
import webbrowser

# SQL Database
dbname = 'test.db'

# Dropbox app keys/secret
app_key = 'o4ewwn9y97bnjk4'
app_secret = 'xt3f58jsdpdvlv4'
access_type = 'app_folder'

# Try to get access_token from SQL
conn = sqlite3.connect(dbname)
c = conn.cursor()
try:
	c.execute('SELECT * FROM Dropbox')
	data=c.fetchall()
	access_token = data
# Get access token from Dropbox
except:
	sess = dbox.session.DropboxSession(app_key,app_secret,access_type)
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	webbrowser.

code = raw_input('Enter auth code here: ').strip()
access_token, user_id = flow.finish(code)
print access_token
print user_id
client = dbox.client.DropboxClient(access_token)
print 'linked account: {}'.format(client.account_info())

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
sec_per_day = 60.*60.*24.

while True:
	try:
		conn = sqlite3.connect(dbname)
		c=conn.cursor()
		c.execute('SELECT * FROM Temp')
		data=c.fetchall()
		conn.close()
		
		data=np.array(data)
		
		# for row in data:
		#         print 'Time: {},\tTemp: {}'.format(row[0],row[1])
		
		ax.clear()
		dates = data[:,0]/sec_per_day
		ax.plot_date(dates,data[:,1],'o-',dates,data[:,2],'o-')
		ax.legend(['Mountain View','Sensor'])
		fig.savefig('out.png')

		f = open('out.png','rb')
		response = client.put_file('/out.png',f,overwrite=True)
		print 'uploaded: {}'.format(response)
		
		plt.pause(180)
		# plt.show()
	except KeyboardInterrupt:
		raise
	except:
		pass

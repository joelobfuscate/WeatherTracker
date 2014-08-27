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
import time

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
	need_creds = True
	while need_creds:
		try:
			fakesession = dict()
			flow=dbox.client.DropboxOAuth2Flow(app_key,app_secret,redirect_uri='http://localhost:8080/',session=fakesession,csrf_token_session_key='dropbox-auth-csrf-token')
			url=flow.start()
			webbrowser.get('/usr/bin/chromium %s').open(url,new=1)
			code=raw_input('Enter code: ').strip()
			access_token,user_id=flow.finish(code)
			print 'access_token is {}'.format(access_token)
			need_creds=False
		except dbox.rest.ErrorResponse:
			time.sleep(1)

# access_token, user_id = flow.finish(code)
client = dbox.client.DropboxClient(access_token)
print 'linked account: {}'.format(client.account_info())

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
sec_per_day = 60.*60.*24.

# def upload_to_dropbox(client,filename):
#         f=open(filename,'rb')
#         response=client.put_file(

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
		f.close()
		print 'uploaded: {}'.format(response)
		
		plt.pause(180)
		# plt.show()
	except KeyboardInterrupt:
		raise
	except:
		pass

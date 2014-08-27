#!/usr/bin/env python

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import dropbox as dbox
import webbrowser
import time
import myhttpd
from pytz import timezone

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
	access_token = data[0][0]
	print data
# Get access token from Dropbox
except IndexError:
	need_creds = True
	while need_creds:
		try:
			fakesession = dict()
			flow=dbox.client.DropboxOAuth2Flow(app_key,app_secret,redirect_uri='http://localhost:8080/',session=fakesession,csrf_token_session_key='dropbox-auth-csrf-token')
			url=flow.start()
			webbrowser.get('/usr/bin/chromium %s').open(url,new=1)

			httpd = myhttpd.ClientRedirectServer(('localhost',8080),myhttpd.ClientRedirectHandler)
			httpd.handle_request()
			httpd.server_close()

			access_token,user_id,url_state=flow.finish(httpd.query_params)
			print 'access_token is {}'.format(access_token)


			try:
				c.execute('CREATE TABLE Dropbox(access_token TEXT)')
			except:
				pass
			c.execute('INSERT INTO Dropbox VALUES(?)',(access_token,))
			conn.commit()


			need_creds=False
		except dbox.rest.ErrorResponse:
			time.sleep(1)
		except KeyboardInterrupt:
			raise

client = dbox.client.DropboxClient(access_token)
print 'linked account: {}'.format(client.account_info())

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
sec_per_day = 60.*60.*24.

loopy=True
while loopy:
	try:
		conn = sqlite3.connect(dbname)
		c=conn.cursor()
		c.execute('SELECT * FROM Temp')
		data=c.fetchall()
		conn.close()
		
		data=np.array(data)
		
		ax.clear()
		dates = data[:,0]
		plotdates = mdates.epoch2num(dates)
		pactime = timezone('US/Pacific')
		axisfmt = mdates.DateFormatter('%-m/%-d %-H:%M',tz=pactime)
		p1=ax.plot_date(plotdates,data[:,1],'-')
		p2=ax.plot_date(plotdates,data[:,2],'-')
		ax.set_ylabel('Deg. Fahrenheit')
		ax.legend(['Mountain View','Sensor'],loc=4,ncol=2,bbox_to_anchor=(1,1.02),borderaxespad=0)
		ax.xaxis.set_major_formatter(axisfmt)
		# ax.set_title('WeatherTracker')
		fig.autofmt_xdate()
		# fig.tight_layout()
		fig.savefig('out.png')

		f = open('out.png','rb')
		response = client.put_file('/out.png',f,overwrite=True)
		f.close()
		print 'uploaded: {}'.format(response)
		
		time.sleep(180)
		# loopy=False
		# plt.show()
	except KeyboardInterrupt:
		raise

#!/usr/bin/env python

import json
import urllib2
import sqlite3
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

while True:
	conn = sqlite3.connect('test.db')
	c=conn.cursor()
	c.execute('SELECT * FROM Temp')
	data=c.fetchall()
	conn.close()
	
	data=np.array(data)
	
	# for row in data:
	#         print 'Time: {},\tTemp: {}'.format(row[0],row[1])
	
	ax.clear()
	ax.plot(data[:,0],data[:,1],'o-')
	
	plt.pause(180)
	# plt.show()

#!/usr/bin/env python

# import pdb
import argparse
import sqlite3
import matplotlib.figure as mplfig
import matplotlib.dates as mdates
import numpy as np
import dropbox as dbox
import webbrowser
import time
import myhttpd
from pytz import timezone
import matplotlib.gridspec as gridspec

# SQL Database
dbname = 'test.db'

# Dropbox app keys/secret
app_key = 'o4ewwn9y97bnjk4'
app_secret = 'xt3f58jsdpdvlv4'
access_type = 'app_folder'

def main(days):
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
    
    fig = mplfig.Figure(figsize=(8,12))
    gs = gridspec.GridSpec(2,1)
    ax = fig.add_subplot(gs[0,0])
    ax1 = fig.add_subplot(gs[1,0])
    # sec_per_day = 60.*60.*24.
    
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
            ax1.clear()
            dates = data[:,0]
            datadates = mdates.epoch2num(dates)

            mtvtemp = data[:,1]
            sensortemp = data[:,2]
            pactime = timezone('US/Pacific')
            axisfmt = mdates.DateFormatter('%-m/%-d %-H:%M',tz=pactime)

	    lastweek_bool = (datadates> (mdates.epoch2num(time.time())-7))
	    plotdates = datadates[lastweek_bool]
	    mtvtempplot = mtvtemp[lastweek_bool]
	    sensortempplot = sensortemp[lastweek_bool]
	    p1=ax.plot_date(plotdates,mtvtempplot,'-')
	    p2=ax.plot_date(plotdates,sensortempplot,'-')
	    ax.set_ylabel('Deg. Fahrenheit')
	    ax.xaxis.set_major_formatter(axisfmt)

            recent_bool = (datadates> (mdates.epoch2num(time.time())-days))
            plotdates = datadates[recent_bool]
            mtvtempplot = mtvtemp[recent_bool]
            sensortempplot = sensortemp[recent_bool]
            p1=ax1.plot_date(plotdates,mtvtempplot,'-')
            p2=ax1.plot_date(plotdates,sensortempplot,'-')
            ax1.set_ylabel('Deg. Fahrenheit')
            ax1.legend(['Mountain View: {:0.1f}'.format(mtvtemp[-1]),'Sensor: {:0.1f}'.format(sensortemp[-1])],loc=0)
            ax1.xaxis.set_major_formatter(axisfmt)
            # ax.set_title('WeatherTracker')

	    # ax.autofmt_xdate()
	    # ax1.autofmt_xdate()
            # fig.tight_layout()
            gs.tight_layout(fig)
            fig.savefig('out.png')
    
            f = open('out.png','rb')
            response = client.put_file('/out.png',f,overwrite=True)
            f.close()
            print 'uploaded: {}'.format(response)
            
            time.sleep(300)
            # loopy=False
            # plt.show()
        except KeyboardInterrupt:
            raise
        except:
            pass

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Loads and runs a gui to analyze saved spectrometer data.')
    parser.add_argument('-v','--verbose',action='store_true',
        help='enable verbose mode')
    parser.add_argument('-d','--days',type=float,
        help='image number')
    
    arg=parser.parse_args()
    
    main(arg.days)

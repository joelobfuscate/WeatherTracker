#!/usr/bin/env python

import json
import urllib2
import sqlite3
import time
import w1thermsensor as therm

sensor = therm.W1ThermSensor()

while True:
    try:
        # Get Mountain View temperature from Wunderground
        f=urllib2.urlopen('http://api.wunderground.com/api/e260c734250b742d/conditions/q/CA/Mountain_View.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        location = 'Mountain View'
        try:
            temp_f_WeatherChannel = parsed_json['current_observation']['temp_f']

        except:
            print parsed_json['response']
            continue
        print 'Current temperature in {} is {}'.format(location,temp_f_WeatherChannel)
        f.close()

        # Get temperature from sensor
        temp_f_Sensor = sensor.get_temperature(therm.W1ThermSensor.DEGREES_F)
        print 'Sensor temperature is {}'.format(temp_f_Sensor)
        
        conn = sqlite3.connect('test.db')
        c=conn.cursor()
        try:
            c.execute('CREATE TABLE Temp(time REAL,temp_f_WeatherChannel REAL,temp_f_Sensor REAL)')
        except:
            pass
        data=(time.time(),temp_f_WeatherChannel,temp_f_Sensor)
        c.execute('INSERT INTO Temp VALUES(?,?,?)',data)
        
        conn.commit()
        conn.close()

    except KeyboardInterrupt:
        raise
    except:
        pass

    time.sleep(300)

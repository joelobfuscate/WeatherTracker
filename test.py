#!/usr/bin/env python

import myhttpd

httpd = myhttpd.ClientRedirectServer(('localhost',8080),myhttpd.ClientRedirectHandler)
httpd.handle_request()
httpd.server_close()
print 'Done'

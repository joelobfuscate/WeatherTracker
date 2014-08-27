import BaseHTTPServer
try:
	from urlparse import parse_qsl
except ImportError:
	from cgi import parse_qsl

class ClientRedirectServer(BaseHTTPServer.HTTPServer):
	query_params={}

class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type",'text/html')
		s.end_headers()
		query = s.path.split('?', 1)[-1]
		query = dict(parse_qsl(query))
		s.server.query_params=query
		s.wfile.write("<html><head><title>Auth Status</title>")
		s.wfile.write('<script language="JavaScript" type="text/javascript">')
		s.wfile.write('function delayClose() {')
		s.wfile.write('	alert(\'a\');')
		s.wfile.write('	window.setTimeout(CloseMe,500);')
		s.wfile.write('}')
		s.wfile.write('function CloseMe() {')
		s.wfile.write('	alert(\'b\');')
		s.wfile.write('	window.close();')
		s.wfile.write('	alert(\'c\');')
		s.wfile.write('}')
		s.wfile.write('</script>')
		s.wfile.write('</head>')
		# s.wfile.write('<body onload="alert(\'hello\')"><p>Auth flow has completed</p>')
		s.wfile.write('<body onload="delayClose()"><p>Auth flow has completed</p>')
		s.wfile.write('</body></html>')

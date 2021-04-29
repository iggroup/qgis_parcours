from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import psycopg2  

##----------------------------------------------------------##
## JSON Web server
##----------------------------------------------------------##

hostName = "localhost"
hostPort = 8000
hostPort1 = 8001
hostPort2 = 8002

class MyServer(BaseHTTPRequestHandler):
# Connexion à la base de données
	try:
		conn = psycopg2.connect("dbname='parcours_locaux' user='postgres' host='localhost' password='postgres'")
		cursor = conn.cursor()
	except:
		print("unable to connect to database")

# Contient les headers standards pour répondre du JSON
	def _set_headers(self):
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Content-Type', 'application/json')
		self.send_header('Access-Control-Allow-Methods', 'GET')
		self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
		self.send_header('Access-Control-Allow-Headers', 'Content-Type')
		self.end_headers()

# Fonction qui envoie directement les chemins, infrastructures et images à l'initialisation
	def do_GET(self):

# Exécution des commandes SQL
			self.cursor.execute("SELECT json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON((the_geom))::json)) FROM chemins_pedestres AS the_geom")
			self.SEND = self.cursor.fetchall()
# Envoi du GeoJson vers le webserver
			self.send_response(200)
			self._set_headers()
# Le  [2:-2] permet d'enlever les crochets de début et fin qui sont inutiles pour la lecture du GeoJson vers JavaScript
			self.wfile.write(bytes(json.dumps(self.SEND)[2:-2], "utf-8"))

# Lancement du webserver et exécution de la classe sur le webserver
myServer = HTTPServer((hostName, hostPort), MyServer)
 
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

# Cloture du webserver par le raccourci ctrl + C
myServer.server_close()

print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

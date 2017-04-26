from database import server as databaseserver

Server = databaseserver.Server()

server = "Arctursus"


dataserver = Server.find_one({"alias":server})
print dataserver

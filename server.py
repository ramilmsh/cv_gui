from src.gui.Server import Server

server = Server()
server.run(host="0.0.0.0", threaded=True)

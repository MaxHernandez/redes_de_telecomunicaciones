#!/usr/bin/python
import socket, sys, gtk, struct, threading, time, random

"""
Referencias:
http://www.binarytides.com/python-socket-programming-tutorial/
http://acaciaecho.wordpress.com/2011/06/20/python-socket-server-example/
"""

class TTT(threading.Thread):

    def __init__(self, remote_host, port):
        threading.Thread.__init__(self)
        
        self.window = gtk.Window()
        self.channel = None
        self.input = None #
        self.output = None #
        self.remote_host = remote_host
        self.port = port
        self.role = None
        self.assignation = {"server" : 0, "client" : 1}
        self.inverse_assignation = {0 : "server", 1 : "client"}
        self.char_assignation = {"server" : "O", "client" : "X" }
        # Vairables del protocolo
        self.turno = 0
        self.fin_partida = 0
        self.siguiente_movimiento = None
        self.matriz_estado = None
        self.nombre = ["", ""]

    def __del__(self):
        if self.channel != None:
            self.channel.close()

    def run (self):
        self.esperar_oponente()

    def esperar_oponente(self):

        self.fin_partida = struct.unpack("H", self.recive()[:1] )[0]
        self.siguiente_movimiento = struct.unpack("H", self.recive()[:1] )[0]

        if self.fin_partida != 0:
            print "Fin del juego"
            return

        if self.turno == 0:
            self.turno = 1
        else:
            self.turno = 0
        if self.role == "client":
            self.bottons_matrix[x][y].set_label(self.char_assignation["server"])
            self.matriz_estado[x][y] = self.assingation["server"]+1
        else:
            self.bottons_matrix[x][y].set_label(self.char_assignation["client"])
            self.matriz_estado[x][y] = self.assingation["client"]+1
        

    def verificar_partida(self):
        temp = 0
        for i in range(3):
            if self.matriz_estado[0][i] == self.matriz_estado[1][i] and self.matriz_estado[1][i] == self.matriz_estado[2][i]:
                temp = self.matriz_estado[0][i]
        for i in range(3):
            if self.matriz_estado[i][0] == self.matriz_estado[i][1] and self.matriz_estado[i][1] == self.matriz_estado[i][2]:
                temp = self.matriz_estado[i][0]
                       
        if self.matriz_estado[0][0] == self.matriz_estado[1][1] and self.matriz_estado[1][1] == self.matriz_estado[2][2]:
            temp = self.matriz_estado[0][0]

        if self.matriz_estado[0][2] == self.matriz_estado[1][1] and self.matriz_estado[1][1] == self.matriz_estado[2][0]:
            temp = self.matriz_estado[1][1]
        
        for i in range(3):
            for j in range(3):
                if self.matriz_estado[i][j] == 0:
                    return temp
        return 3


    def on_button_clicked(self, w):
        if self.inverse_assignation[self.turno] == self.role:
            print "No es tu turno"
            return 

        temp =  w.name.split(",")
        x, y = (int(temp[0]), int(temp[1]))

        self.fin_partida = self.verificar_partida()
        if self.fin_partida != 0:
            self.send(struct.pack("H", self.fin_partida))
            self.send(struct.pack("H", self.siguiente_movimiento))
            return

        self.siguiente_movimiento = (y*3)+x
        self.matriz_estado[x][y] = self.assignation[self.role]+1

        self.bottons_matrix[x][y].set_label(self.char_assignation[self.role])
        if self.turno == 0:
            self.turno = 1
        else:
            self.turno = 0
        self.send(struct.pack("H", self.fin_partida))
        self.send(struct.pack("H", self.siguiente_movimiento))
        self.start()
        

    def new_game(self, nombre):
        self.matriz_estado = [[0]*3]*3
        self.nombre[self.assignation[sys.argv[1]]] = nombre

        if len(sys.argv) > 1 and sys.argv[1] == "client":
            if self.connect_to():
                self.setup_server() 
                self.role = "client"
                self.setup_giu(nombre)

        elif len(sys.argv) > 1 and sys.argv[1] == "server":
            if self.setup_server():
                time.sleep(1.0/10)
                self.connect_to() 
                self.role = "server"
                self.start()
                self.setup_giu(nombre)
        else:
            print "Selecciona un rol \"python ticTactToe.py server|client\""

    def setup_giu(self, nombre):
        grid = gtk.Table(3, 3, True)
        self.window.add(grid)
        self.bottons_matrix = []

        for i in range(3):
            temp = []
            for j in range(3):
                button = gtk.Button(label=" ")
                button.set_name(str(i)+","+str(j))
                button.set_size_request(100,100)
                button.connect("clicked", self.on_button_clicked)
                grid.attach(button, i, i+1, j, j+1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=0, ypadding=0)
                temp.append(button)
            self.bottons_matrix.append(temp)

            #Eliminarl de aqui
        self.bottons_matrix[0][0].set_label("X")
        self.bottons_matrix[1][1].set_label("O")
        self.bottons_matrix[2][0].set_label("X")
        self.bottons_matrix[1][0].set_label("O")
        self.bottons_matrix[2][2].set_label("X")

        # a aqui
        self.window.connect("delete-event", gtk.main_quit)
        self.window.set_title(nombre)
        self.window.show_all()

        gtk.main()

    def connect_to(self):
        try:
            self.output = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            return False

        try:
            self.remote_ip = socket.gethostbyname(self.remote_host )
        except socket.gaierror:
            print 'Hostname could not be resolved.'
            return False

        try:
            if sys.argv[1] == "server":
                self.output.connect((self.remote_ip , self.port)) # Eliminar si no funciona
            else:
                self.output.connect((self.remote_ip , self.port+1)) # Eliminar si no funciona
            print 'Connection reached'
        except:
            print 'Conections refused'
            return False

        return True

    def setup_server(self):
        try:
            self.input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sys.argv[1] == "client":
                self.input.bind(('', self.port))
            else:
                self.input.bind(('', self.port+1))
 
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            return False


        print 'server started successfully, waiting...'
        self.input.listen(1)
        self.input, addr = self.input.accept()
 
        print 'contact', addr, 'on'
        return True

    def send(self, data):
        try :
            print "Send:", data
            self.output.sendall(data)
        except socket.error:
            print 'Send failed'
            return False

        return True

    def recive(self):
        data = None
        try:
            while True is not False:
                print "Esperando datos"
                data = self.input.recv(4096)
                print ("["+data+"]")
                if data is not None:
                    break
        except socket.error:
            print "conexion perdida"

        return data    

def main():

    remote_host = 'localhost'
    port = 4040
    ttt = TTT(remote_host, port)
    ttt.new_game(sys.argv[2])

main()

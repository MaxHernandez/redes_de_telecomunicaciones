#! /usr/bin/python
from math import log
from random import randint
from subprocess import call
from sys import argv

def generar_hipercubo(dimensiones): 
    numero_nodos = 2**dimensiones
    grafo = dict()
    for i in range(numero_nodos):
        for j in range(numero_nodos):
            distancia = i^j
            if distancia == 0:
                grafo[i, j] = 0
                continue

            distancia = log(distancia, 2)
            if distancia%1 == 0.0 : # Terminar, si distancia binaria entre ambos es 1 
                grafo[i, j] = 1
            else:
                grafo[i, j] = 0
    return grafo, numero_nodos

def generar_simulacion(name='simulacion.tcl', dimensiones = 2, time_simulation=30):
    grafo, numero_nodos = generar_hipercubo(dimensiones)

    nodos = ''
    for n in range(numero_nodos):
        nodos += 'set node'+str(n)+' [$simulation node]\n'

    conexiones = ''
    for i in range(numero_nodos):
        for j in range(numero_nodos):
            if grafo[i, j] == 1:
                conexiones += '$simulation duplex-link $node'+str(i)+' $node'+str(j)+' 1Mb 10ms DropTail\n'


    conexiones_tcp = ''
    numero_conexiones_tcp = randint(0, numero_nodos)
    for i in range(numero_conexiones_tcp):
        nodos_tcp = [None, None]
        nodos_tcp[0] = randint(0, numero_nodos-1)
        nodos_tcp[1] = randint(0, numero_nodos-1)
        while nodos_tcp[0] == nodos_tcp[1]:
            nodos_tcp[1] = randint(0, numero_nodos)
            
        conexiones_tcp += """
        set tcp%d [new Agent/TCP]
        $tcp%d set class_ 2

        $simulation attach-agent $node%d $tcp%d

        set sink%d [new Agent/TCPSink]
        $simulation attach-agent $node%d $sink%d
        $simulation connect $tcp%d $sink%d
        $tcp%d set fid_ %d
        """%(i, i, nodos_tcp[0], i, i, nodos_tcp[1], i, i, i, i, i)

    conexiones_ftp = ''
    for i in range(numero_conexiones_tcp):
        conexiones_ftp += """
        set ftp%d [new Application/FTP]
        $ftp%d attach-agent $tcp%d
        $ftp%d set type_ FTP
        """%(i, i, i, i)

    tiempos_simulaciones = ''
    for i in range(numero_conexiones_tcp):
        tiempos_simulaciones += '$simulation at %0.2f "$ftp%d start"\n' % (float(randint(0, time_simulation/2)), i)
        tiempos_simulaciones += '$simulation at %0.2f "$ftp%d stop"\n' % (float(randint( (time_simulation/2)+1, time_simulation)), i)

    final_simulacion = '$simulation at '+str(float(time_simulation))+' "finish"'

    colors_simulation = ''
    for i in range(numero_conexiones_tcp):
        colors_simulation += '$simulation color %d #%02X%02X%02X \n'%(i, randint(0,255), randint(0,255), randint(0,255))

    # aqui se organiza la simulacion 
    simulacion = ("set simulation [new Simulator]",
                  """
set simulation_file [open output.nam w]
$simulation namtrace-all $simulation_file
proc finish {} {
        global simulation simulation_file
        $simulation flush-trace
        close $simulation_file
        exec nam output.nam &
        exit 0
    }
    """,
                  colors_simulation,
                  nodos,
                  conexiones,
                  conexiones_tcp,
                  conexiones_ftp,
                  tiempos_simulaciones,
                  final_simulacion,
                  "$simulation run"
)

    fl = open(name, 'w')
    for i in simulacion:
        fl.write(i+'\n')
    fl.close()

    call(['ns', name])

def main():
    if len(argv) > 1:
        generar_simulacion(dimensiones = int(argv[1]))
    else:
        generar_simulacion()

main()

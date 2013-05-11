# ns redes.tcl
set simulation [new Simulator]

set simulation_file [open output.nam w]
$simulation namtrace-all $simulation_file
proc finish {} {
        global simulation simulation_file
        $simulation flush-trace
        close $simulation_file
        exec nam output.nam &
        exit 0
    }

set node1 [$simulation node]
set node2 [$simulation node]
set node3 [$simulation node]
set node4 [$simulation node]
set node5 [$simulation node]
set node6 [$simulation node]

$simulation color 1 #ff0000
$simulation color 2 Green
$simulation color 3 Blue

#Crear una conexion entre los nodos
$simulation duplex-link $node2 $node3 1Mb 10ms DropTail
$simulation duplex-link $node4 $node5 2Mb 10ms DropTail
$simulation duplex-link $node1 $node6 2Mb 10ms DropTail
$simulation duplex-link $node2 $node6 1Mb 10ms DropTail
$simulation duplex-link $node3 $node6 1Mb 10ms DropTail
$simulation duplex-link $node4 $node6 2Mb 10ms DropTail
$simulation duplex-link $node5 $node6 10Mb 20ms DropTail

$simulation queue-limit $node1 $node6 10
$simulation queue-limit $node2 $node6 10
$simulation queue-limit $node3 $node6 10
$simulation queue-limit $node4 $node6 10
$simulation queue-limit $node5 $node6 10

$simulation duplex-link-op $node1 $node6 queuePos 0.5
$simulation duplex-link-op $node2 $node6 queuePos 0.5
$simulation duplex-link-op $node3 $node6 queuePos 0.5
$simulation duplex-link-op $node4 $node6 queuePos 0.5
$simulation duplex-link-op $node5 $node6 queuePos 0.5

#Configurando conexion tcp
set tcp [new Agent/TCP]
$tcp set class_ 2
$simulation attach-agent $node1 $tcp
set sink [new Agent/TCPSink]
$simulation attach-agent $node5 $sink
$simulation connect $tcp $sink
$tcp set fid_ 1

set tcp2 [new Agent/TCP]
$tcp2 set class_ 2
$simulation attach-agent $node2 $tcp2
set sink2 [new Agent/TCPSink]
$simulation attach-agent $node4 $sink2
$simulation connect $tcp2 $sink2
$tcp2 set fid_ 1

#Conexion FTP sobre la conexion tcp
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP

$simulation at 0.1 "$ftp2 start"
$simulation at 10.0 "$ftp2 stop"
$simulation at 0.1 "$ftp start"
$simulation at 10.0 "$ftp stop"
$simulation at 10.0 "finish"

$simulation run

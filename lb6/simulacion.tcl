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
    
$simulation color 0 #A318DF 
$simulation color 1 #7C58FB 
$simulation color 2 #B03136 
$simulation color 3 #954EB5 

set node0 [$simulation node]
set node1 [$simulation node]
set node2 [$simulation node]
set node3 [$simulation node]
set node4 [$simulation node]
set node5 [$simulation node]
set node6 [$simulation node]
set node7 [$simulation node]

$simulation duplex-link $node0 $node1 1Mb 10ms DropTail
$simulation duplex-link $node0 $node2 1Mb 10ms DropTail
$simulation duplex-link $node0 $node4 1Mb 10ms DropTail
$simulation duplex-link $node1 $node0 1Mb 10ms DropTail
$simulation duplex-link $node1 $node3 1Mb 10ms DropTail
$simulation duplex-link $node1 $node5 1Mb 10ms DropTail
$simulation duplex-link $node2 $node0 1Mb 10ms DropTail
$simulation duplex-link $node2 $node3 1Mb 10ms DropTail
$simulation duplex-link $node2 $node6 1Mb 10ms DropTail
$simulation duplex-link $node3 $node1 1Mb 10ms DropTail
$simulation duplex-link $node3 $node2 1Mb 10ms DropTail
$simulation duplex-link $node3 $node7 1Mb 10ms DropTail
$simulation duplex-link $node4 $node0 1Mb 10ms DropTail
$simulation duplex-link $node4 $node5 1Mb 10ms DropTail
$simulation duplex-link $node4 $node6 1Mb 10ms DropTail
$simulation duplex-link $node5 $node1 1Mb 10ms DropTail
$simulation duplex-link $node5 $node4 1Mb 10ms DropTail
$simulation duplex-link $node5 $node7 1Mb 10ms DropTail
$simulation duplex-link $node6 $node2 1Mb 10ms DropTail
$simulation duplex-link $node6 $node4 1Mb 10ms DropTail
$simulation duplex-link $node6 $node7 1Mb 10ms DropTail
$simulation duplex-link $node7 $node3 1Mb 10ms DropTail
$simulation duplex-link $node7 $node5 1Mb 10ms DropTail
$simulation duplex-link $node7 $node6 1Mb 10ms DropTail


        set tcp0 [new Agent/TCP]
        $tcp0 set class_ 2

        $simulation attach-agent $node6 $tcp0

        set sink0 [new Agent/TCPSink]
        $simulation attach-agent $node4 $sink0
        $simulation connect $tcp0 $sink0
        $tcp0 set fid_ 0
        
        set tcp1 [new Agent/TCP]
        $tcp1 set class_ 2

        $simulation attach-agent $node0 $tcp1

        set sink1 [new Agent/TCPSink]
        $simulation attach-agent $node2 $sink1
        $simulation connect $tcp1 $sink1
        $tcp1 set fid_ 1
        
        set tcp2 [new Agent/TCP]
        $tcp2 set class_ 2

        $simulation attach-agent $node6 $tcp2

        set sink2 [new Agent/TCPSink]
        $simulation attach-agent $node5 $sink2
        $simulation connect $tcp2 $sink2
        $tcp2 set fid_ 2
        
        set tcp3 [new Agent/TCP]
        $tcp3 set class_ 2

        $simulation attach-agent $node1 $tcp3

        set sink3 [new Agent/TCPSink]
        $simulation attach-agent $node0 $sink3
        $simulation connect $tcp3 $sink3
        $tcp3 set fid_ 3
        

        set ftp0 [new Application/FTP]
        $ftp0 attach-agent $tcp0
        $ftp0 set type_ FTP
        
        set ftp1 [new Application/FTP]
        $ftp1 attach-agent $tcp1
        $ftp1 set type_ FTP
        
        set ftp2 [new Application/FTP]
        $ftp2 attach-agent $tcp2
        $ftp2 set type_ FTP
        
        set ftp3 [new Application/FTP]
        $ftp3 attach-agent $tcp3
        $ftp3 set type_ FTP
        
$simulation at 6.00 "$ftp0 start"
$simulation at 27.00 "$ftp0 stop"
$simulation at 14.00 "$ftp1 start"
$simulation at 27.00 "$ftp1 stop"
$simulation at 6.00 "$ftp2 start"
$simulation at 17.00 "$ftp2 stop"
$simulation at 13.00 "$ftp3 start"
$simulation at 19.00 "$ftp3 stop"

$simulation at 30.0 "finish"
$simulation run

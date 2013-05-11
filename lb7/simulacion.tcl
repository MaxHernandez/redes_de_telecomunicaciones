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
    
$simulation color 0 #08ADFC 
$simulation color 1 #4ED1FD 
$simulation color 2 #F58B8D 

set node0 [$simulation node]
set node1 [$simulation node]
set node2 [$simulation node]
set node3 [$simulation node]
set node4 [$simulation node]
set node5 [$simulation node]
set node6 [$simulation node]
set node7 [$simulation node]

$simulation duplex-link $node0 $node1 1Mb 10ms DropTail
$simulation duplex-link $node1 $node2 1Mb 10ms DropTail
$simulation duplex-link $node2 $node3 1Mb 10ms DropTail
$simulation duplex-link $node3 $node4 1Mb 10ms DropTail
$simulation duplex-link $node4 $node5 1Mb 10ms DropTail
$simulation duplex-link $node5 $node6 1Mb 10ms DropTail
$simulation duplex-link $node6 $node7 1Mb 10ms DropTail
$simulation duplex-link $node7 $node0 1Mb 10ms DropTail


        set udp0 [new Agent/UDP]
        $simulation attach-agent $node2 $udp0

        set null0 [new Agent/Null]
        $simulation attach-agent $node7 $null0
        $simulation connect $udp0 $null0
        $udp0 set fid_ 0
        
        set udp1 [new Agent/UDP]
        $simulation attach-agent $node7 $udp1

        set null1 [new Agent/Null]
        $simulation attach-agent $node5 $null1
        $simulation connect $udp1 $null1
        $udp1 set fid_ 1
        
        set udp2 [new Agent/UDP]
        $simulation attach-agent $node3 $udp2

        set null2 [new Agent/Null]
        $simulation attach-agent $node6 $null2
        $simulation connect $udp2 $null2
        $udp2 set fid_ 2
        

    set exp [new Application/Traffic/Exponential]
    $exp attach-agent $udp0
    $exp set type_ Exponential
    $exp set packet_size_ 1000
    $exp set rate_ 1mb
    
                                                                                                                           
    set par [new Application/Traffic/Pareto]
    $par attach-agent $udp1
    $par set type_ Pareto
    $par set packet_size_ 1000
    $par set rate_ 1mb
    
                                                                                                                           
    set cbr [new Application/Traffic/CBR]
    $cbr attach-agent $udp2
    $cbr set type_ CBR
    $cbr set packet_size_ 1000
    $cbr set rate_ 1mb
    

    $simulation at 0.00 "$exp start"
    $simulation at 30.00 "$exp stop"
    $simulation at 0.00 "$par start"
    $simulation at 30.00 "$par stop"
    $simulation at 0.00 "$cbr start"
    $simulation at 30.00 "$cbr stop"
    
$simulation at 30.0 "finish"
$simulation run

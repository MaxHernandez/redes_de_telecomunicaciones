
BEGIN {
    tiempo_simulacion = 0
    paquetes_enviados = 0
    paquetes_entregados = 0
    datos_entregados = 0
    nodo_origen = 3
    nodo_destino = 6
}

{
    if ("r" == $1 && "cbr" == $9 && nodo_destino == $7){
paquetes_entregados += 1
datos_entregados += $11-20
tiempo_simulacion = $3
    }

    if ("r" == $1 && "cbr" == $9 && nodo_origen == $5){
paquetes_enviados += 1
    }
}

END {
    printf("%g\n", paquetes_enviados)
    printf("%g\n", paquetes_entregados)
    printf("%g\n", (datos_entregados/tiempo_simulacion)*(8/1000))
}

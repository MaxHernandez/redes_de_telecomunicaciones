BEGIN {
    tiempo_simulacion = 0
    paquetes_enviados = 0
    paquetes_entregados = 0
    datos_entregados = 0
    nodo_origen = 0
    nodo_destino = 4
}

{
    if ("r" == $1 && "tcp" == $9 && nodo_destino == $7){
	paquetes_entregados += 1
	datos_entregados += $11-20
	tiempo_simulacion = $3
    }

    if ("r" == $1 && "tcp" == $9 && nodo_origen == $5){
	paquetes_enviados += 1
    }
}

END {
    printf("Se mandaron %g y de esos %g fueron entregados con exito \n", paquetes_enviados, paquetes_entregados)
    printf("El rendimiento es: %g Kbps \n", (datos_entregados/tiempo_simulacion)*(8/1000))
}
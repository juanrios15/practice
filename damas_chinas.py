class Tablero:
    
    def __init__(self):
        self.matriz = [["" for x in range(8)] for x in range(8)]

    def dibujar_tablero(self):
        print("   ", end="")
        for x in range(8):
            print(f"  {x}  ", end="")
        print()
        for i, fila in enumerate(self.matriz):
            print("   ", end="")
            print(" ----"*8)
            print(f" {i} ", end="")
            for campo in fila:
                print("|", end=" ")
                if isinstance(campo, Dama):
                    print(campo.nombre, end=" ")
                else:
                    print("  ", end=" ")
            print("|")


class Dama:
    
    def __init__(self, nombre, jugador, x, y):
        self.nombre = nombre
        self.jugador = jugador
        self.pos_x = x
        self.pos_y = y
    
    def __str__(self):
        return self.nombre


def encontrar_posicion(mov1, mov2, pos_x, pos_y):
    if mov1 == "-":
        pos_x = pos_x - 1
    else:
        pos_x = pos_x + 1
    if mov2 == "-":
        pos_y = pos_y - 1
    else:
        pos_y = pos_y + 1    
    return pos_x, pos_y

def seleccionar_ficha(fichas):
    ficha = input("Seleccione ficha: ")
    if ficha not in fichas:
        ficha = seleccionar_ficha(fichas)
    return ficha

def seleccionar_movimiento(movs):
    movimiento = int(input("Seleccione un movimiento: "))
    if movimiento not in movs:
        movimiento = seleccionar_movimiento(movs)
    return movimiento

def validar_disponibles(tablero, fichas, damas_vivas, turno):
    ficha = seleccionar_ficha(fichas)
    for dama in damas_vivas:
        if dama.nombre == ficha:
            ficha_seleccionada = dama
            break
    # Movimientos disponibles:
    movimientos = [["-","-"], ["-","+"], ["+","-"], ["+","+"]]
    movimientos_disponibles = []
    indice_mov = 1
    for mov in movimientos:
        pos_x, pos_y = encontrar_posicion(mov[0], mov[1], ficha_seleccionada.pos_x, ficha_seleccionada.pos_y)   
        if pos_x < 0 or pos_y < 0 or pos_x > 7 or pos_y > 7:
            pass
        else:
            if tablero.matriz[pos_x][pos_y] == "":
                movimientos_disponibles.append({"item": indice_mov, "pos_x":pos_x, "pos_y":pos_y, "come": False})
                indice_mov +=1
            elif isinstance(tablero.matriz[pos_x][pos_y], Dama):
                dama_observada = tablero.matriz[pos_x][pos_y]
                if dama_observada.jugador == turno:
                    pass
                else:
                    # revisar el siguiente espacio:
                    npos_x, npos_y = encontrar_posicion(mov[0], mov[1], pos_x, pos_y)
                    if npos_x < 0 or npos_y < 0 or npos_x > 7 or npos_y > 7:
                        pass
                    else:
                        if tablero.matriz[npos_x][npos_y] == "":
                            movimientos_disponibles.append({
                                                            "item": indice_mov,
                                                            "pos_x":npos_x, 
                                                            "pos_y":npos_y, 
                                                            "come": True, 
                                                            "come_x": pos_x, 
                                                            "come_y": pos_y})
                            indice_mov +=1
                        else:
                            pass
            else:
                print("ERROR GRAVE, VUELVA A INTENTARLO")
                pass
    if len(movimientos_disponibles) == 0:
        print("Esta ficha no tiene movimientos disponibles.")
        movimientos_disponibles, ficha_seleccionada = validar_disponibles(tablero, fichas, damas_vivas, turno)
    return movimientos_disponibles, ficha_seleccionada    

def validar_disponibles_recomer(tablero, ficha_sel, turno):
    movimientos = [["-","-"], ["-","+"], ["+","-"], ["+","+"]]
    movimientos_disponibles = []
    indice_mov = 1
    for mov in movimientos:
        pos_x, pos_y = encontrar_posicion(mov[0], mov[1], ficha_sel.pos_x, ficha_sel.pos_y)   
        if pos_x < 0 or pos_y < 0 or pos_x > 7 or pos_y > 7:
            pass
        else:
            if isinstance(tablero.matriz[pos_x][pos_y], Dama):
                dama_observada = tablero.matriz[pos_x][pos_y]
                if dama_observada.jugador != turno:
                    npos_x, npos_y = encontrar_posicion(mov[0], mov[1], pos_x, pos_y)
                    if npos_x < 0 or npos_y < 0 or npos_x > 7 or npos_y > 7:
                        pass
                    else:
                        if tablero.matriz[npos_x][npos_y] == "":
                            movimientos_disponibles.append({
                                                            "item": indice_mov,
                                                            "pos_x":npos_x, 
                                                            "pos_y":npos_y, 
                                                            "come": True, 
                                                            "come_x": pos_x, 
                                                            "come_y": pos_y})
                            indice_mov +=1
                        else:
                            pass
    return movimientos_disponibles

def ejecutar_movimiento(damas_rival, movimientos_disponibles, ficha_sel):
    print(f"Tiene {len(movimientos_disponibles)} movimientos:")
    for mov in movimientos_disponibles:
        print(f"{mov['item']}. x={mov['pos_x']}, y={mov['pos_y']}")
    
    index_movs = [mov["item"] for mov in movimientos_disponibles]

    movimiento = seleccionar_movimiento(index_movs)
    for disponible in movimientos_disponibles:
        if movimiento == disponible["item"]:
            movimiento_elegido = disponible
            break
    if movimiento_elegido["come"] == True:
        tablero.matriz[movimiento_elegido["come_x"]][movimiento_elegido["come_y"]] = ""
        for dama_rival in damas_rival:
            if dama_rival.pos_x == movimiento_elegido["come_x"] and dama_rival.pos_y == movimiento_elegido["come_y"]:
                damas_rival.remove(dama_rival)
    tablero.matriz[ficha_sel.pos_x][ficha_sel.pos_y] = ""
    ficha_sel.pos_x = movimiento_elegido["pos_x"]
    ficha_sel.pos_y = movimiento_elegido["pos_y"]
    tablero.matriz[ficha_sel.pos_x][ficha_sel.pos_y] = ficha_sel
    
    if movimiento_elegido["come"] == True:
        movimientos_disponibles = validar_disponibles_recomer(tablero, ficha_sel, turno)
        if len(movimientos_disponibles) > 0:
            tablero.dibujar_tablero()
            ejecutar_movimiento(damas_rival, movimientos_disponibles, ficha_sel)
    
    
tablero = Tablero()
damas_jugador1 = []
running = True
turno = True
# Fichas del jugador 1
for x in range(4):
    dama1 = Dama(f"A{x+1}", True, 0, x*2)
    dama2 = Dama(f"A{x+5}", True, 1, x*2+1)
    tablero.matriz[0][x*2] = dama1
    tablero.matriz[1][x*2+1] = dama2
    damas_jugador1.append(dama1)
    damas_jugador1.append(dama2)

# Fichas del jugador 2
damas_jugador2 = []
for x in range(4):
    dama1 = Dama(f"B{x+1}", False, 6, x*2)
    dama2 = Dama(f"B{x+5}", False, 7, x*2+1)
    tablero.matriz[6][x*2] = dama1
    tablero.matriz[7][x*2+1] = dama2
    damas_jugador2.append(dama1)
    damas_jugador2.append(dama2)


#INICIO DEL JUEGO
while running:
    tablero.dibujar_tablero()
    jugador = 1 if turno else 2
    fichas = []
    if turno == True:
        damas_vivas = damas_jugador1
        damas_rival = damas_jugador2
    else:
        damas_vivas = damas_jugador2
        damas_rival = damas_jugador1
    for ficha in damas_vivas:
        fichas.append(ficha.nombre) 
    print(f"Turno del jugador #{jugador}")
    
    movimientos_disponibles, ficha_seleccionada = validar_disponibles(tablero, fichas, damas_vivas, turno)
    ejecutar_movimiento(damas_rival, movimientos_disponibles, ficha_seleccionada)      
        
    if len(damas_rival) == 0:
        tablero.dibujar_tablero()
        print("*********")
        print("GANADOR")
        print(f"Jugador {jugador} ha ganado la partida")
        running = False
    turno = not turno
    
        
        
        
        
    
        
   
    
        
    
    
            
    
    


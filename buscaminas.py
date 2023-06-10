from copy import deepcopy
import random
import os
import time
import msvcrt
import animacion


def mostrarTablero(tablero):
    print()
    marco = '                         ╠════╬════╬════╬════╬════╬════╬════╬════╣'
    for i in range(8):
        if i == 0:
            print('                         ╔════╦════╦════╦════╦════╦════╦════╦════╗')
        else:
            print(marco)

        print('                         ║', tablero[i][0], '║', tablero[i][1], '║', tablero[i][2], '║',
              tablero[i][3], '║', tablero[i][4], '║', tablero[i][5], '║', tablero[i][6], '║', tablero[i][7], '║')

    print('                         ╚════╩════╩════╩════╩════╩════╩════╩════╝')
    print()


def asignarMinas(tablero):
    cont = 0
    while cont != 10:
        num1 = random.randrange(0, 8)
        num2 = random.randrange(0, 8)
        if tablero[num1][num2] == '💣':
            continue
        else:
            tablero[num1][num2] = '💣'
            cont += 1


def contMinas(tablero, fila, columna):
    contMinas = 0
    for i in range(-1, 2):
        for x in range(-1, 2):
            if fila+i > 7 or columna+x > 7 or fila+i < 0 or columna+x < 0:
                continue
            elif tablero[fila+i][columna+x] == '💣':
                contMinas += 1
    if fila > 7 or columna > 7 or fila < 0 or columna < 0:
        pass
    else:
        if tablero[fila][columna] != '💣' and tablero[fila][columna] != '  ':
            pass
        else:
            return contMinas


def autoPoner(tablero, tableroSinMinas, columna, fila):
    ceros = [(fila, columna)]
    while len(ceros) > 0:
        fila, columna = ceros.pop()
        for i in range(-1, 2):
            for x in range(-1, 2):
                if fila+i > 7 or columna+x > 7 or fila+i < 0 or columna+x < 0:
                    continue
                elif tablero[fila+i][columna+x] == '  ':
                    if contMinas(tablero, fila+i, columna+x) == 0:
                        tablero[fila+i][columna+x] = ' 0'
                        tableroSinMinas[fila+i][columna+x] = ' 0'
                        if (fila+i, columna+x)not in ceros:
                            ceros.append((fila+i, columna+x))
                    else:
                        tableroSinMinas[fila+i][columna+x] = ' ' + \
                            str(contMinas(tablero, fila+i, columna+x))
                        tablero[fila+i][columna+x] = ' ' + \
                            str(contMinas(tablero, fila+i, columna+x))
                else:
                    continue


def juegoPrincipal(tableroMoverse, emojisList, tableroSinMinas, tablero, opccionJugar):
    fila = 0
    columna = 0
    posAnterior = tableroMoverse[fila][columna]
    movTeclado = 0
    emojiRandom = emojisList[random.randrange(0, len(emojisList))]
    tableroMoverse[fila][columna] = emojiRandom
    animacion.mensajeBuscaminas()
    mostrarTablero(tableroMoverse)
    while movTeclado != ' ':
        emojiRandom = emojisList[random.randrange(0, len(emojisList))]
        tableroMoverse[fila][columna] = posAnterior
        print('Donde quieres moverte usando W/A/S/D/espacio: ')
        movTeclado = msvcrt.getwch()
        if movTeclado == 'w' and fila != 0:
            fila -= 1
        elif movTeclado == 's' and fila != 7:
            fila += 1
        elif movTeclado == 'a' and columna != 0:
            columna -= 1
        elif movTeclado == 'd' and columna != 7:
            columna += 1
        else:
            os.system('cls')
        posAnterior = tableroMoverse[fila][columna]
        tableroMoverse[fila][columna] = emojiRandom
        os.system('cls')
        animacion.mensajeBuscaminas()
        mostrarTablero(tableroMoverse)
        tableroMoverse[fila][columna] = '  '
    if opccionJugar == True:
        cont = 0
        if tablero[fila][columna] == '💣':
            os.system('cls')
            animacion.perdiste()
            mostrarTablero(tablero)
            return 0
        elif contMinas(tablero, fila, columna) == 0 and tablero[fila][columna] == '  ':
            tablero[fila][columna] = ' 0'
            tableroSinMinas[fila][columna] = ' 0'
            autoPoner(tablero, tableroSinMinas, columna, fila)
        elif contMinas(tablero, fila, columna) != '🚩' and tablero[fila][columna] == '  ':
            tableroSinMinas[fila][columna] = ' ' + \
                str(contMinas(tablero, fila, columna))
            tablero[fila][columna] = ' '+str(contMinas(tablero, fila, columna))

        for i in range(8):
            for x in range(8):
                if tableroSinMinas[i][x] != '  ' and tableroSinMinas[i][x] != '💣' and tableroSinMinas[i][x] != '🚩':
                    cont += 1
        time.sleep(0.001)
        if cont == 54:
            os.system('cls')
            animacion.ganaste()
            mostrarTablero(tablero)
            return 0
        mostrarTablero(tableroSinMinas)
    elif tableroSinMinas[fila][columna] == '🚩' and opccionJugar == '🚩':
        if tableroMoverse[fila][columna] == '  ':
            print('NO HAY BANDERA')
        else:
            tableroSinMinas[fila][columna] = '  '
            tablero[fila][columna] = '  '
    elif tableroSinMinas[fila][columna] == '  ' and opccionJugar == False:
        tableroSinMinas[fila][columna] = '🚩'
        tablero[fila][columna] = '🚩'
    else:
        pass
    os.system('cls')


def menuPartida():
    tablero = [['  ' for i in range(8)] for i in range(8)]
    tableroSinMinas = deepcopy(tablero)
    asignarMinas(tablero)
    os.system('cls')
    animacion.bomba()
    print('El objetivo del juego Buscaminas es liberar todas las casillas que no tienen una mina.\nEl tablero es de 8x8 y en el habran 10 minas que deberas de evitar.\nLas casillas con número indican la cantidad de minas en las casillas que la rodean.\nLas banderas te serviran de referencia a ti mismo para saber donde puede haber una mina, estas las podras desplegar por todo el tablero.\nPara poder moverte por el tablero necesitaras de las teclas W/A/S/D.\nPara confirmar la posicion que quieres elejir deberas pular espacio\nMucha suerte!!!')
    print()
    input('Dale a enter para empezar: ')
    os.system('cls')
    while True:
        tableroMoverse = deepcopy(tableroSinMinas)
        os.system('cls')
        animacion.mensajeBuscaminas()
        mostrarTablero(tableroSinMinas)
        print('Quieres poner una bandera?:\ns = Poner Bandera\nn = Quitar Bandera\nj = Juagar\no = Sales del buscaminas\nElige: ')
        bandera = msvcrt.getwch()
        os.system('cls')
        emojisList = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '😣', '😖', '😫', '😩', '🥺', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱',
                      '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
        if bandera == 's':
            juegoPrincipal(tableroMoverse, emojisList,
                tableroSinMinas, tablero, False)
        elif bandera == 'n':
            juegoPrincipal(tableroMoverse, emojisList,
                tableroSinMinas, tablero, '🚩')
        elif bandera == 'j':
            if juegoPrincipal(tableroMoverse, emojisList, tableroSinMinas, tablero, True) == 0:
                break
        elif bandera == 'o':
            os.system('cls')
            print()
            animacion.graciasXjuagar()
            break
        else:
            continue


menuPartida()

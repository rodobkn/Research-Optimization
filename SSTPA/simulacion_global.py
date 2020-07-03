# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:39:20 2020

@author: pvcor
"""

import codigo_matematico
import data_simulacion
from data_simulacion import Equipos, Equipos_torneo_estatico, Equipos, Equipos_torneo_estatico_2
import pandas as pd
from pandas import ExcelWriter
import subprocess
import numpy as np


df = pd.read_excel('Datos_originales.xlsx', "Resultados")
pagina_equipos = pd.read_excel('Datos_originales.xlsx', "Equipos")
writer = pd.ExcelWriter('Datos.xlsx')
pagina_equipos.to_excel(writer,'Equipos', index=False)
df.to_excel(writer,'Resultados', index=False)
writer.save()

N = int(input("Ingrese el numero de simulaciones de torneo a realizar: "))

booleano = True

print("Escriba el numero de las fechas desde las cuales desea optimizar inclusive.")
print("Para ingresar cada fecha presione enter.")
print("Al finalizar escriba -1 y luego enter.")

lista_fechas = []

while booleano == True:
    n = int(input("Ingrese numero: "))
    if n == -1:
        booleano = False
    else: 
        lista_fechas.append(n)

def ordenamiento_formato():
    global lista_fechas
    lista = []
    lista.append(int(lista_fechas[0]))
    lista_fechas.pop(0)
    for i in range(len(lista_fechas)):
        lista.append(3)
        lista.append(int(lista_fechas[0])-1)
        lista.append(1)
        lista.append(2)
        lista.append(int(lista_fechas[0]))
        lista_fechas.pop(0)
    lista.append(3)
    lista.append(30)
    lista.append(4)
    lista.append(0)
    return lista

lista_fechas_final = ordenamiento_formato()
lista_fechas_auxiliar = tuple(lista_fechas_final)
parametro_avanzar_el_calendario = 30
lista_atractivo_real = []

def calcular_goles_hechos(data):

    goles_hechos = 0

    for fecha in data:

        goles_hechos = goles_hechos + fecha[1]

    return goles_hechos

def calcular_goles_recibidos(data):

    goles_recibidos = 0

    for fecha in data:

        goles_recibidos = goles_recibidos + fecha[2]

    return goles_recibidos

def calcular_puntos(data):

    puntos = 0

    for fecha in data:

        if fecha[1] > fecha[2]:

            puntos += 3

        elif fecha[1] == fecha[2]:

            puntos += 1

        else:
            pass

    return puntos 

def calcular_goles_hechos_de_local(data):

    goles_local = 0

    for fecha in data:

        if fecha[0] == 1:

            goles_local = goles_local + fecha[1]
        else:
            pass

    return goles_local

def calcular_goles_hechos_visita(data):

    goles_visita = 0

    for fecha in data:

        if fecha[0] == 0:

            goles_visita = goles_visita + fecha[1]
        else:
            pass

    return goles_visita

def calcular_goles_recibidos_local(data):

    goles_recibidos = 0

    for fecha in data:

        if fecha[0] == 1:

            goles_recibidos = goles_recibidos + fecha[2]
        else:
            pass

    return goles_recibidos

def calcular_goles_recibidos_visita(data):

    goles_recibidos = 0

    for fecha in data:

        if fecha[0] == 0:

            goles_recibidos = goles_recibidos + fecha[2]
        else:
            pass

    return goles_recibidos

def calcular_partidos_jugados_local(data):

    partidos_jugados = 0

    for fecha in data:

        if fecha[0] == 1:

            partidos_jugados += 1

        else:
            pass

    return partidos_jugados

def calcular_partidos_jugados_visita(data):

    partidos_jugados = 0

    for fecha in data:

        if fecha[0] == 0:

            partidos_jugados += 1

        else:
            pass

    return partidos_jugados

def calcular_puntos_reales(data):
    #Deberia entregar una lista de la siguiente manera:
    #partiendo con fecha=16
    #[fecha, puntos en esa fecha]

    lista = []


    for numero_fecha in range(16,31):

        puntos = 0

        for fecha in range(numero_fecha):

            if data[fecha][1] > data[fecha][2]:

                puntos += 3

            elif data[fecha][1] == data[fecha][2]:

                puntos += 1

            else:
                pass

        lista.append([numero_fecha, puntos])



    return lista

def aplicar_colores(palabra):


    if str(palabra)=="amarillo":
        color_celda = "yellow"

    elif str(palabra)=="rojo":
        color_celda = "red"

    elif str(palabra)=="azul":
        color_celda = "blue"

    elif str(palabra)=="verde":
        color_celda = "green"

    else:
        color_celda = 'white'

    return f'background-color: {color_celda}'


for i in range(N):
    
    
    fecha_inicial = lista_fechas_final[0]
    lista_fechas_final.pop(0)
    file = open("fecha_actual.txt", "w") #actualizar para que este en la otra carpeta
    file.write(str(fecha_inicial))
    file.close()
    data_simulacion.info_equipos(fecha_inicial - 1)
    fixture = data_simulacion.fixture_inicial(fecha_inicial)
    
    class Equipo:
    
        def __init__(self, nombre_equipo):
    
            self.nombre_equipo = nombre_equipo
    
            self.data_equipo = Equipos[self.nombre_equipo]   #Esto es la lista(visita/local, goles hechos, goles recibidos) del equipo que está 
                                                             #en data_15_partidos_torneo_2019.py
    
            self.data_equipo_resultados_reales = Equipos_torneo_estatico[self.nombre_equipo]  #Aqui le pasamos la info de la siguiente manera
                                                                                              #[local-visita, goles hechos, goles recibidos, fecha]
            self.data_equipo_resultados_reales.sort(key = lambda x: x[3])
    
            self.puntos_reales = calcular_puntos_reales(self.data_equipo_resultados_reales)
    
    
    
            self.goles_hechos = calcular_goles_hechos(self.data_equipo)
    
            self.goles_recibidos = calcular_goles_recibidos(self.data_equipo)
    
            self.diferencia_de_goles = self.goles_hechos - self.goles_recibidos
    
            self.puntos = calcular_puntos(self.data_equipo)
    
            self.goles_hechos_local = calcular_goles_hechos_de_local(self.data_equipo)
    
            self.goles_hechos_visita = calcular_goles_hechos_visita(self.data_equipo)
    
            self.goles_recibidos_local = calcular_goles_recibidos_local(self.data_equipo)
    
            self.goles_recibidos_visita = calcular_goles_recibidos_visita(self.data_equipo)
    
            self.partidos_local = calcular_partidos_jugados_local(self.data_equipo)
    
            self.partidos_visita = calcular_partidos_jugados_visita(self.data_equipo)
    
        def actualizar_datos(self):
    
            self.goles_hechos = calcular_goles_hechos(self.data_equipo)
    
            self.goles_recibidos = calcular_goles_recibidos(self.data_equipo)
    
            self.diferencia_de_goles = self.goles_hechos - self.goles_recibidos
    
            self.puntos = calcular_puntos(self.data_equipo)
    
            self.goles_hechos_local = calcular_goles_hechos_de_local(self.data_equipo)
    
            self.goles_hechos_visita = calcular_goles_hechos_visita(self.data_equipo)
    
            self.goles_recibidos_local = calcular_goles_recibidos_local(self.data_equipo)
    
            self.goles_recibidos_visita = calcular_goles_recibidos_visita(self.data_equipo)
    
            self.partidos_local = calcular_partidos_jugados_local(self.data_equipo)
    
            self.partidos_visita = calcular_partidos_jugados_visita(self.data_equipo)
    
    class Torneo:
        def __init__(self):
            self.nombre_equipos = Equipos.keys()     #Contiene una lista con los nombres de los equipos del torneo
            self.fixture = fixture                   #Contiene el fixture
            self.equipos_objetos = []                #Esta será la lista que contiene los equipos como objetos
            self.marcadores_fechas_reales = []
            self.marcadores_fechas = []              #Contendra esto para la primera fecha(indice 0):
                                                     #[[('EV', 'OH'), (3, 2)], [('U', 'HH'), (2, 1)], ... , [('UdC', 'PA'), (3, 3)]]
                                                     #Obviamente la segunda, es lo mismo, y estará en el indice 1
    
        def setear_equipos_objetos(self):
            for nombre in self.nombre_equipos:
                self.equipos_objetos.append(Equipo(nombre))
        
        def avanzar_el_calendario(self):
            global parametro_avanzar_el_calendario
            n = parametro_avanzar_el_calendario
            print("")
            fechas_reales = data_simulacion.asignacion_resultados(self.fixture)
            self.marcadores_fechas_reales = fechas_reales 
            fecha_fin = n - (30 - len(fechas_reales))
            
            for fecha in fechas_reales[0:fecha_fin]:
                
                for partido in fecha:
                
                    nombre_equipo_1 = partido[0][0]
                
                    for equipo_objeto in self.equipos_objetos:
                        
                        if nombre_equipo_1 == equipo_objeto.nombre_equipo:
                        
                            equipo_objeto.data_equipo.append([1, partido[1][0], partido[1][1]])
                            equipo_objeto.actualizar_datos()
    
                        else:
                            pass
    
                    nombre_equipo_2 = partido[0][1]
    
                    for equipo_objeto in self.equipos_objetos:
    
                        if nombre_equipo_2 == equipo_objeto.nombre_equipo:
    
                            equipo_objeto.data_equipo.append([0, partido[1][1], partido[1][0]])
                            equipo_objeto.actualizar_datos()
    
                        else:
                            pass
    
            self.fixture = self.fixture[fecha_fin:]
    
            fecha_inicio = 31 - len(fechas_reales)
            df = pd.read_excel('Datos.xlsx', "Resultados")
            pagina_equipos = pd.read_excel('Datos.xlsx', "Equipos")
    
            index_inicio = 126  #Porque (128-2)=126 , que es el indice real con el cual trabajamos en el dataframe de pandas.
                                #Empezamos con la fecha 16
    
            index_inicio_real = index_inicio - ((fecha_inicio - 16) * (9))
    
    
            for fecha in self.marcadores_fechas_reales[0:fecha_fin]:
    
                contador = 8
    
                for resultado in fecha:
    
                    df.iloc[index_inicio_real + contador, 2] = resultado[0][0]
                    df.iloc[index_inicio_real + contador, 3] = resultado[0][1]
                    df.iloc[index_inicio_real + contador, 4] = str(resultado[1][0]) + " " + ":" + " " + str(resultado[1][1])
    
                    contador = contador - 1
    
                index_inicio_real = index_inicio_real - 9
                
            #EL FOR DE ABAJO ES DE PRUEBA------------------------------------------------
                
            for fecha in self.marcadores_fechas_reales[fecha_fin:]:
    
                contador = 8
    
                for resultado in fecha:
    
                    df.iloc[index_inicio_real + contador, 2] = resultado[0][0]
                    df.iloc[index_inicio_real + contador, 3] = resultado[0][1]
                    df.iloc[index_inicio_real + contador, 4] = "sin resultado"
    
                    contador = contador - 1
    
                index_inicio_real = index_inicio_real - 9
            
            #EL FOR DE ABAJO ES DE PRUEBA------------------------------------------------
    
    
            writer = pd.ExcelWriter('Datos.xlsx')
            pagina_equipos.to_excel(writer,'Equipos', index=False)
            df.to_excel(writer,'Resultados', index=False)
            writer.save()
                
    
        def simular(self):
    
            print("A continuación simularemos el resto del calendario")
            print("Esto puede tardar unos segundos")
            print("")
            fechas = codigo_matematico.simulacion_calendario(self.fixture)
            self.marcadores_fechas = fechas
    
            for fecha in fechas:
    
                for partido in fecha:
    
                    nombre_equipo_1 = partido[0][0]
    
                    for equipo_objeto in self.equipos_objetos:
    
                        if nombre_equipo_1 == equipo_objeto.nombre_equipo:
    
                            equipo_objeto.data_equipo.append([1, partido[1][0], partido[1][1]])
                            equipo_objeto.actualizar_datos()
    
                        else:
                            pass
    
                    nombre_equipo_2 = partido[0][1]
    
                    for equipo_objeto in self.equipos_objetos:
    
                        if nombre_equipo_2 == equipo_objeto.nombre_equipo:
    
                            equipo_objeto.data_equipo.append([0, partido[1][1], partido[1][0]])
                            equipo_objeto.actualizar_datos()
    
                        else:
                            pass
    
            fecha_inicio = 31 - len(fechas)
            df = pd.read_excel('Datos.xlsx', "Resultados")
            pagina_equipos = pd.read_excel('Datos.xlsx', "Equipos")
    
            index_inicio = 126  #Porque (128-2)=126 , que es el indice real con el cual trabajamos en el dataframe de pandas.
                                #Empezamos con la fecha 16
    
            index_inicio_real = index_inicio - ((fecha_inicio - 16) * (9))
    
    
            for fecha in self.marcadores_fechas:
    
                contador = 8
    
                for resultado in fecha:
    
                    df.iloc[index_inicio_real + contador, 2] = resultado[0][0]
                    df.iloc[index_inicio_real + contador, 3] = resultado[0][1]
                    df.iloc[index_inicio_real + contador, 4] = str(resultado[1][0]) + " " + ":" + " " + str(resultado[1][1])
    
                    contador = contador - 1
    
                index_inicio_real = index_inicio_real - 9
    
            writer = pd.ExcelWriter('Datos.xlsx')
            pagina_equipos.to_excel(writer,'Equipos', index=False)
            df.to_excel(writer,'Resultados', index=False)
            writer.save()
    
    
    #aqui borramos la info de partidos simulados para actualizarla luego con partidos reales
    
            for fecha in fechas:
    
                for partido in fecha:
    
                    nombre_equipo_1 = partido[0][0]
    
                    for equipo_objeto in self.equipos_objetos:
    
                        if nombre_equipo_1 == equipo_objeto.nombre_equipo:
    
                            equipo_objeto.data_equipo.pop()
                            equipo_objeto.actualizar_datos()
    
                        else:
                            pass
    
                    nombre_equipo_2 = partido[0][1]
    
                    for equipo_objeto in self.equipos_objetos:
    
                        if nombre_equipo_2 == equipo_objeto.nombre_equipo:
    
                            equipo_objeto.data_equipo.pop()
                            equipo_objeto.actualizar_datos()
    
                        else:
                            pass
    
    
        def generar_datos_visualizacion(self,indicador_maximo_atractivo):
    
    
            diccionario_equipos = {
            'CC' : [],
            'UdC' : [],
            'CR' : [],
            'U' : [],
            'TM' : [],
            'UC' : [],
            'PA' : [],
            'HH' : [],
            'IQ' : [],
            'AN' : [],
            'OH' : [],
            'AI' : [],
            'UE' : [],
            'LC' : [],
            'SL' : [],
            'EV' : []
                }
    
    
            #Al final tiene que tener 15 listas así, cada equipos, empezando con fecha=16:
            #[fecha, parametro A (1 si puede ser campeon, 0 si no puede ser campeon), parametro D (1 si puede descender, 0 si no puede descender), puntos,color]
            #los colores pueden ser "rojo", "amarillo", "azul", "verde"
            #rojo -----> A=0 y D=0
            #amarillo -> A=0 y D=1
            #azul -----> A=1 y D=0
            #verde ----> A=1 y D=1
    
            lista = []
            data_simulacion.info_equipos_torneo_estatico_2(30)
    
            for equipo_objeto in self.equipos_objetos:
    
                equipo_objeto.data_equipo_resultados_reales = data_simulacion.Equipos_torneo_estatico_2[equipo_objeto.nombre_equipo]
    
                equipo_objeto.data_equipo_resultados_reales.sort(key = lambda x: x[3])
    
                equipo_objeto.puntos_reales = calcular_puntos_reales(equipo_objeto.data_equipo_resultados_reales)
    
                lista.append([equipo_objeto.nombre_equipo, equipo_objeto.puntos_reales])
    
    
            factor = 14
            for numero_fecha in range(16,31):
    
                puntos_puntero = 0
                puntos_ultimo = 20000
    
                
                for lista_equipo in lista:
    
                    if lista_equipo[1][numero_fecha - 16][1] > puntos_puntero:
                        puntos_puntero = lista_equipo[1][numero_fecha - 16][1]
    
                    else:
                        pass
    
                    if lista_equipo[1][numero_fecha - 16][1] < puntos_ultimo:
                        puntos_ultimo = lista_equipo[1][numero_fecha - 16][1]
    
                    else:
                        pass
    
                for lista_equipo in lista:
    
                    parametro_A = 0
                    parametro_D = 0
                    color = None
    
                    if (lista_equipo[1][numero_fecha - 16][1] + (factor*3)) >= puntos_puntero:
                        parametro_A = 1
                    else:
                        pass
    
                    if (puntos_ultimo + (factor*3)) >= lista_equipo[1][numero_fecha - 16][1]:
                        parametro_D = 1
                    else:
                        pass
    
                    if parametro_A==0 and parametro_D==0:
                        color = "rojo"
                    elif parametro_A==0 and parametro_D==1:
                        color = "amarillo"
                    elif parametro_A==1 and parametro_D==0:
                        color = "azul"
                    else:
                        color = "verde"
                    
                    diccionario_equipos[lista_equipo[0]].append([numero_fecha, parametro_A, parametro_D, lista_equipo[1][numero_fecha - 16][1],color])
    
                factor = factor - 1
    
    
            #print(diccionario_equipos)
    
            diccionario_final = {"NOMBRE EQUIPO": [], "FECHA 16": [], "FECHA 17": [], "FECHA 18": [], "FECHA 19": [],
                        "FECHA 20": [], "FECHA 21": [], "FECHA 22": [], "FECHA 23": [], "FECHA 24": [], "FECHA 25": [],
                        "FECHA 26": [], "FECHA 27": [], "FECHA 28": [], "FECHA 29": [], "FECHA 30": []}
    
            for clave in diccionario_equipos:
    
                diccionario_final["NOMBRE EQUIPO"].append(clave)
                diccionario_final["FECHA 16"].append(diccionario_equipos[clave][0][4])
                diccionario_final["FECHA 17"].append(diccionario_equipos[clave][1][4])
                diccionario_final["FECHA 18"].append(diccionario_equipos[clave][2][4])
                diccionario_final["FECHA 19"].append(diccionario_equipos[clave][3][4])
                diccionario_final["FECHA 20"].append(diccionario_equipos[clave][4][4])
                diccionario_final["FECHA 21"].append(diccionario_equipos[clave][5][4])
                diccionario_final["FECHA 22"].append(diccionario_equipos[clave][6][4])
                diccionario_final["FECHA 23"].append(diccionario_equipos[clave][7][4])
                diccionario_final["FECHA 24"].append(diccionario_equipos[clave][8][4])
                diccionario_final["FECHA 25"].append(diccionario_equipos[clave][9][4])
                diccionario_final["FECHA 26"].append(diccionario_equipos[clave][10][4])
                diccionario_final["FECHA 27"].append(diccionario_equipos[clave][11][4])
                diccionario_final["FECHA 28"].append(diccionario_equipos[clave][12][4])
                diccionario_final["FECHA 29"].append(diccionario_equipos[clave][13][4])
                diccionario_final["FECHA 30"].append(diccionario_equipos[clave][14][4])
            
            
            atractivo = 0
            for key in diccionario_final:
                
                if key == 'NOMBRE EQUIPO':
                    pass
                else:
                    
                    for color in diccionario_final[key]:
                        
                        if color == 'verde':
                            
                            atractivo += 2
                        
                        elif color == 'amarillo':
                            
                            atractivo += 1
                        
                        elif color == 'azul':
                            
                            atractivo += 1.5
                            
                        elif color == 'rojo':
                            
                            atractivo += 0
        
            if indicador_maximo_atractivo == True:
                
                df = pd.DataFrame(diccionario_final)
                df = df[["NOMBRE EQUIPO", "FECHA 16", "FECHA 17", "FECHA 18", "FECHA 19", "FECHA 20",
                    "FECHA 21", "FECHA 22", "FECHA 23", "FECHA 24", "FECHA 25", "FECHA 26", "FECHA 27", "FECHA 28", "FECHA 29", "FECHA 30"]]
            
            
            
                styled = (df.style.applymap(aplicar_colores))
                writer = ExcelWriter('tabla_con_colores.xlsx')
                #El argumento index=False, evita que se agregue una columna adicional con la enumeración de cada fila
                styled.to_excel(writer, 'Hoja de datos', engine='openpyxl', index=False)
    
                writer.save()
            
            return atractivo
    
    
    torneo_2019 = Torneo()
    torneo_2019.setear_equipos_objetos()
    
    
    ###PRIMERA ITERACION AUTOMATICA###
    
    ##TENGO EL FIXTURE NORMAL DESDE fecha_inicial HASTA LA FECHA 30
    
    ##SIMULAMOS
    torneo_2019.simular()
    
    ##OPTIMIZAMOS
    #AQUI importar fecha_inicial a params.py y correr model.py ===>
    p1 = subprocess.Popen(['python.exe' ,'model.py'], shell=True) 
    p1.wait()
    torneo_2019.fixture = data_simulacion.fixture_dinamico() #ACTUALIZAMOS EL FIXTURE AL OPTIMIZADO
    if torneo_2019.fixture == True:
        print("El programa termina puesto que el modelo es infactible")
        boleano = True
    else:
        
        boleano = False
    ##################################

    while boleano == False:
    
        # print(" ")
        # print("Si quiere salir escriba ------------------------------------> 0")
        # print("Si quiere simular escriba ----> 1")
        # print("Si quiere optimizar escriba ----> 2")
        # print("Si quiere actualizar/jugar una fecha del campeonato 2018 escriba ----> 3")
        # print("Si quiere el excel de colores----------------------> 4")
        # print("")
        
        print(lista_fechas_auxiliar)
        print(lista_fechas_final)
        imput = lista_fechas_final[0]
        lista_fechas_final.pop(0)
    
        if imput == 1:
    
            torneo_2019.simular()
    
        elif imput == 2:
    
            fecha_inicial = lista_fechas_final[0]
            lista_fechas_final.pop(0)
            file = open("fecha_actual.txt", "w") #actualizar para que este en la otra carpeta
            file.write(str(fecha_inicial))
            file.close()
            #AQUI importar fecha_inicial a params.py y correr model.py ===>
            p1 = subprocess.Popen(['python.exe' ,'model.py'], shell=True) 
            p1.wait()
            torneo_2019.fixture = data_simulacion.fixture_dinamico()
            if torneo_2019.fixture == True:
                print("El programa termina puesto que el modelo es infactible")
                boleano = True
            else:
                print("SE HA OPTIMIZADO EL FIXTURE")
                boleano = False
    
        elif imput == 3:
    
            parametro_avanzar_el_calendario = lista_fechas_final[0]
            lista_fechas_final.pop(0)
            torneo_2019.avanzar_el_calendario()
    
        elif imput == 4:
            
            if len(lista_atractivo_real) == 0:
                Max = 0
            else:
                Max = max(lista_atractivo_real)
            
            current_atractivo = torneo_2019.generar_datos_visualizacion(False)
            
            lista_atractivo_real.append(current_atractivo)
            
            if current_atractivo > Max:
                torneo_2019.generar_datos_visualizacion(True)
                df = pd.read_excel('Datos.xlsx', "Resultados")
                pagina_equipos = pd.read_excel('Datos.xlsx', "Equipos")
                writer = pd.ExcelWriter('Datos_maximo_atractivo.xlsx')
                pagina_equipos.to_excel(writer,'Equipos', index=False)
                df.to_excel(writer,'Resultados', index=False)
                writer.save()
    
        else:
    
            boleano = True
    
    df = pd.read_excel('Datos_originales.xlsx', "Resultados")
    pagina_equipos = pd.read_excel('Datos_originales.xlsx', "Equipos")
    writer = pd.ExcelWriter('Datos.xlsx')
    pagina_equipos.to_excel(writer,'Equipos', index=False)
    df.to_excel(writer,'Resultados', index=False)
    writer.save()

    lista_fechas_final = list(lista_fechas_auxiliar)

    boleano = False

    data_simulacion.Equipos = {
    'CC' : [],
    'UdC' : [],
    'CR' : [],
    'U' : [],
    'TM' : [],
    'UC' : [],
    'PA' : [],
    'HH' : [],
    'IQ' : [],
    'AN' : [],
    'OH' : [],
    'AI' : [],
    'UE' : [],
    'LC' : [],
    'SL' : [],
    'EV' : []
        }
    
    #este sirve para las visualizaciones del torneo estatico no mas
    data_simulacion.Equipos_torneo_estatico = {
    'CC' : [],
    'UdC' : [],
    'CR' : [],
    'U' : [],
    'TM' : [],
    'UC' : [],
    'PA' : [],
    'HH' : [],
    'IQ' : [],
    'AN' : [],
    'OH' : [],
    'AI' : [],
    'UE' : [],
    'LC' : [],
    'SL' : [],
    'EV' : []
        }
    
    
    #Este lo hacemos para la visualizacion luego de todas las iteraciones
    data_simulacion.Equipos_torneo_estatico_2 = {
    'CC' : [],
    'UdC' : [],
    'CR' : [],
    'U' : [],
    'TM' : [],
    'UC' : [],
    'PA' : [],
    'HH' : [],
    'IQ' : [],
    'AN' : [],
    'OH' : [],
    'AI' : [],
    'UE' : [],
    'LC' : [],
    'SL' : [],
    'EV' : []
        }

print(lista_atractivo_real)
atractivo_promedio = np.sum(np.array(lista_atractivo_real))/N
print("el promedio de atractivo fue: "+str(atractivo_promedio))
print("el numero maximo de atractivo alcanzado fue: "+str(max(lista_atractivo_real)))




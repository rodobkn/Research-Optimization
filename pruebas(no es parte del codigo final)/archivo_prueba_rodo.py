import codigo_matematico
import data_simulacion
from data_simulacion import Equipos, Equipos_torneo_estatico, Equipos, Equipos_torneo_estatico_2
import pandas as pd
from pandas import ExcelWriter
import subprocess
import numpy as np


primera_fecha = int(input("Ingrese la primera fecha desde la que optimiza: "))



def setear_headers(primera_fecha):   #excel de colores luego de las iteraciones
    terminar = False
    df = pd.read_excel('Datos_originales.xlsx', sheet_name='Resultados')
    lista_partidos = []

    for i in df.index:

        if terminar == True:

            break

        if (i % 9 == 0):

            if int(df['Jornada'][i]) < primera_fecha:

                terminar = True

        else:
            local_team = str(df['Local'][i]).replace(u'\xa0', u'')
            visit_team = str(df['Visita'][i]).replace(u'\xa0', u'')
            final_string = local_team + "-" + visit_team
            lista_partidos.append(final_string)


    lista_headers_estaticos = ["Puntaje Total", "Cantidad partidos ascenso-descenso", "Puntaje ascenso-descenso", "Cantidad partidos sólo ascenso",
                                "Puntaje ascenso", "Cantidad partidos sólo descenso", "Puntaje descenso"]

    headers = lista_headers_estaticos + lista_partidos

    diccionario = {}

    for header in headers:

        diccionario[header] = []


    return diccionario


diccionario = setear_headers(primera_fecha)



def encontrar_fecha_del_partido(string_partido):

    df = pd.read_excel('Datos.xlsx', sheet_name='Resultados')
    fecha = None

    for i in df.index:

        if (i % 9 == 0):

            fecha = int(df['Jornada'][i])

        else:

            local_team = str(df['Local'][i]).replace(u'\xa0', u'')
            visit_team = str(df['Visita'][i]).replace(u'\xa0', u'')
            final_string = local_team + "-" + visit_team

            if final_string == string_partido:

                return fecha


for key in diccionario:

    if len(key) > 7:

        pass

    else:

        fecha_partido = encontrar_fecha_del_partido(key)
        diccionario[key].append(fecha_partido)

print(diccionario)





    




            


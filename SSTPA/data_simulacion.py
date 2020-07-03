import pandas as pd
import csv

df = pd.read_excel('Datos.xlsx', sheet_name='Resultados')
df_original = pd.read_excel('Datos_originales.xlsx', sheet_name='Resultados')

resultados_reales = []

Equipos = {
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
Equipos_torneo_estatico = {
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
Equipos_torneo_estatico_2 = {
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


######### excel de colores ########
#[local-visita, goles hechos, goles en contra, fecha]
def info_equipos_torneo_estatico(info_fechas):   #excel de colores
    w = 0
    fecha = 30 
    for i in df.index:

        if (str(df['Jornada'][i]) != 'nan') and (df['Jornada'][i] < fecha):
            fecha = df['Jornada'][i]

        if str(df['Resultado'][i]) != 'nan' and w <= info_fechas*8 - 1:
            Equipos_torneo_estatico[str(df['Local'][i]).replace(u'\xa0', u'')].append([1,int(str(df['Resultado'][i])[0]),int(str(df['Resultado'][i])[4]),int(fecha)])
            w += 1

    w = 0
    fecha = 30
    for i in df.index:

        if (str(df['Jornada'][i]) != 'nan') and (df['Jornada'][i] < fecha):
            fecha = df['Jornada'][i]

        if str(df['Resultado'][i]) != 'nan' and w <= info_fechas*8 -1:
            Equipos_torneo_estatico[str(df['Visita'][i]).replace(u'\xa0', u'')].append([0,int(str(df['Resultado'][i])[4]),int(str(df['Resultado'][i])[0]),int(fecha)])
            w += 1

def info_equipos_torneo_estatico_2(info_fechas):   #excel de colores luego de las iteraciones
    df = pd.read_excel('Datos.xlsx', sheet_name='Resultados')
    w = 0
    fecha = 30 
    for i in df.index:

        if (str(df['Jornada'][i]) != 'nan') and (df['Jornada'][i] < fecha):
            fecha = df['Jornada'][i]

        if str(df['Resultado'][i]) != 'nan' and w <= info_fechas*8 - 1:
            Equipos_torneo_estatico_2[str(df['Local'][i]).replace(u'\xa0', u'')].append([1,int(str(df['Resultado'][i])[0]),int(str(df['Resultado'][i])[4]),int(fecha)])
            w += 1

    w = 0
    fecha = 30
    for i in df.index:

        if (str(df['Jornada'][i]) != 'nan') and (df['Jornada'][i] < fecha):
            fecha = df['Jornada'][i]

        if str(df['Resultado'][i]) != 'nan' and w <= info_fechas*8 -1:
            Equipos_torneo_estatico_2[str(df['Visita'][i]).replace(u'\xa0', u'')].append([0,int(str(df['Resultado'][i])[4]),int(str(df['Resultado'][i])[0]),int(fecha)])
            w += 1


def partidos_jugados_torneo_estatico():  #agrega a la lista resultados_reales los resultados reales de los equipos de la feha 1 a la 30
    global resultados_reales
    resultados_reales = []
    w = 0
    fecha = 30 
    for i in df.index:
        if str(df_original['Resultado'][i]) != 'nan' and w <= fecha*8 - 1:
            resultados_reales.append([(str(df_original['Local'][i]).replace(u'\xa0', u''),df_original['Visita'][i].replace(u'\xa0', u'')),(int(str(df_original['Resultado'][i])[0]),int(str(df_original['Resultado'][i])[4]))])
            w += 1
###################################

def info_equipos(info_fechas):  
    w = 0
    fecha = 30 
    for i in df.index:

        if (str(df['Jornada'][i]) != 'nan') and (df['Jornada'][i] < fecha):
            fecha = df['Jornada'][i]

        if str(df['Resultado'][i]) != 'nan' and w <= 30*8 - 1:
            Equipos[str(df['Local'][i]).replace(u'\xa0', u'')].append([1,int(str(df['Resultado'][i])[0]),int(str(df['Resultado'][i])[4]),int(fecha)])
            w += 1

    w = 0
    fecha = 30
    for i in df.index:

        if (str(df['Jornada'][i]) != 'nan') and (df['Jornada'][i] < fecha):
            fecha = df['Jornada'][i]

        if str(df['Resultado'][i]) != 'nan' and w <= 30*8 -1:
            Equipos[str(df['Visita'][i]).replace(u'\xa0', u'')].append([0,int(str(df['Resultado'][i])[4]),int(str(df['Resultado'][i])[0]),int(fecha)])
            w += 1
            
    for equipo in Equipos:
        Equipos[equipo].sort(key = lambda x: x[3])
    
    for equipo in Equipos:
        c = 0
        while c < 30-info_fechas:
            Equipos[equipo].pop()
            c += 1
        for fecha in Equipos[equipo]:
            fecha.pop()

def fixture_inicial(fecha_inicial): #recupera el fixture inicial no optimizado incluyendo la fecha_inicial
    lista_aux = []
    fixture = []
    jornada = 0
    for i in df.index:
        if str(df['Jornada'][i]) != 'nan':
            jornada = int(df['Jornada'][i])
        if str(df['Resultado'][i]) != 'nan' and jornada >= fecha_inicial:
            lista_aux.append([str(df['Local'][i]).replace(u'\xa0', u''),str(df['Visita'][i]).replace(u'\xa0', u'')])
            if len(lista_aux) == 8:
                fixture.append(lista_aux)
                lista_aux = []
    fixture.reverse()
    return fixture

def fixture_dinamico(): #lee la programacion optimizada y la traduce para simularla
    lista_aux = []
    fixture = []
    with open('programacion.csv', newline='') as File:  
        reader = csv.reader(File)
        for row in reader:
            
            #SE PRUEBA SI EL MODELO ES INFACTIBLE PRIMERO
            if row[0] == 'Modelo Infactible':
                print("EL MODELO ES INFACTIBLE, Y POR TANTO NO SE DEBE SEGUIR")
                boleano_a_retornar = True
                return boleano_a_retornar
            
            if row[0] == '':
                lista_aux.append([row[1],row[2]])
                if len(lista_aux) == 8:
                    fixture.append(lista_aux)
                    lista_aux = []  
    return fixture

def asignacion_resultados(fixture): #asigna los resultados reales a un fixture dado
    global resultados_reales
    resultados_reales = []
    partidos_jugados_torneo_estatico()
    resultados_fixture_nuevo = []
    fecha_actual = 0
    for fecha in fixture:
        resultados_fixture_nuevo.append([])
        for partido in fecha:
            for tupla in resultados_reales:
                if (partido[0],partido[1]) == tupla[0]:
                    resultados_fixture_nuevo[fecha_actual].append([(partido[0],partido[1]),tupla[1]])
        fecha_actual += 1
    return resultados_fixture_nuevo


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



######### excel de colores ########
info_equipos_torneo_estatico(30)  #Te crea el diccionario de equipos, con la info verdadera del torneo, hasta la fecha 30
###################################


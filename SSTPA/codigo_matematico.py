import numpy as np
import math

from data_simulacion import Equipos

#visitante = 0
#local = 1
#partido i-esimo: [0,3,1] => gano 3 a 1 siendo visita


def promedio_goles_hechos_visita(equipo):
  goles_hechos = 0
  fechas = 0
  for i in range(len(equipo)):
    if equipo[i][0] == 0:
      goles_hechos += equipo[i][1]
      fechas += 1
  return goles_hechos/fechas
    
def promedio_goles_hechos_local(equipo):
  goles_hechos = 0
  fechas = 0
  for i in range(len(equipo)):
    if equipo[i][0] == 1:
      goles_hechos += equipo[i][1]
      fechas += 1
  return goles_hechos/fechas

def promedio_goles_hechos_total(equipo):
  goles_hechos = 0
  fechas = 0
  for i in range(len(equipo)):
    goles_hechos += equipo[i][1]
    fechas += 1
  return goles_hechos/fechas

def promedio_goles_recibidos_visita(equipo):
  goles_recibidos = 0
  fechas = 0
  for i in range(len(equipo)):
    if equipo[i][0] == 0:
      goles_recibidos += equipo[i][2]
      fechas += 1
  return goles_recibidos/fechas
    
def promedio_goles_recibidos_local(equipo):
  goles_recibidos = 0
  fechas = 0
  for i in range(len(equipo)):
    if equipo[i][0] == 1:
      goles_recibidos += equipo[i][2]
      fechas += 1
  return goles_recibidos/fechas

def promedio_goles_recibidos_total(equipo):
  goles_recibidos = 0
  fechas = 0
  for i in range(len(equipo)):
    goles_recibidos += equipo[i][2]
    fechas += 1
  return goles_recibidos/fechas

def poisson_bivariada_invertida(lambda1,lambda2,lambda3,U):
  lista_probabilidades_acumuladas = []
  p = 0
  for x in range(8):
    for y in range(8):
      z = 0
      v = np.exp(-(lambda1+lambda2+lambda3))*((lambda1**x)*(lambda2**y)/(math.factorial(x)*math.factorial(y)))
      for k in range(min(x,y)+1):
        z += (math.factorial(x)/(math.factorial(k)*math.factorial(x-k)))*(math.factorial(y)/(math.factorial(k)*math.factorial(y-k)))*math.factorial(k)*((lambda3/(lambda2*lambda1))**k)
      p += z*v
      lista_probabilidades_acumuladas.append([(x,y),p])
  for i in range(len(lista_probabilidades_acumuladas)):
    if U <= lista_probabilidades_acumuladas[i][1]:
      return lista_probabilidades_acumuladas[i][0]

def instancia_poisson_bivariada(equipo_local,equipo_visita):
  lambda1 = (promedio_goles_hechos_local(equipo_local) + promedio_goles_hechos_total(equipo_local) + promedio_goles_recibidos_visita(equipo_visita) + promedio_goles_recibidos_total(equipo_visita))/4
  lambda2 = (promedio_goles_hechos_visita(equipo_visita) + promedio_goles_hechos_total(equipo_visita) + promedio_goles_recibidos_local(equipo_local) + promedio_goles_recibidos_total(equipo_local))/4
  lambda3 = 0
  promedio_goles_total_equipo_local = (promedio_goles_hechos_total(equipo_local) + promedio_goles_recibidos_total(equipo_visita))/2
  promedio_goles_total_equipo_visita = (promedio_goles_hechos_total(equipo_visita) + promedio_goles_recibidos_total(equipo_local))/2
  for i in range(len(equipo_local)):
    lambda3 += (equipo_local[i][1] + equipo_visita[i][2] - promedio_goles_total_equipo_local)*(equipo_visita[i][1] + equipo_local[i][2] - promedio_goles_total_equipo_visita)
  lambda3 = lambda3/len(equipo_local)
  if lambda3 < 0:
    lambda3 = 0
  U = np.random.uniform(0,1)
  return poisson_bivariada_invertida(lambda1,lambda2,lambda3,U)

def simulacion_partido(equipo_local,equipo_visita):
  lista_resultados = []
  for x in range(8):
    for y in range(8):
      lista_resultados.append([(x,y),0])
  for i in range(100):
    r = instancia_poisson_bivariada(equipo_local,equipo_visita)
    for k in range(len(lista_resultados)):
      if lista_resultados[k][0] == r:
        lista_resultados[k][1] += 1
  ocurrencias = 0
  resultado_simulado = lista_resultados[0][0]
  for j in range(len(lista_resultados)):
    if lista_resultados[j][1] > ocurrencias:
      resultado_simulado = lista_resultados[j][0]
      ocurrencias = lista_resultados[j][1]
  return resultado_simulado

def simulacion_calendario(fixture):

  calendario_simulado = []
  indice_fecha = 0
  for fecha in fixture:
    calendario_simulado.append([])
    for llave in range(len(fecha)):
        simulacion_resultado = simulacion_partido(Equipos[fixture[indice_fecha][llave][0]],Equipos[fixture[indice_fecha][llave][1]])
        calendario_simulado[indice_fecha].append([(fixture[indice_fecha][llave][0],fixture[indice_fecha][llave][1]),simulacion_resultado])
    indice_fecha +=1
  return calendario_simulado

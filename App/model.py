"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf



# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'routes_avg_duration': None,
            'connections': None,
            'components': None,
            'paths': None,
        }

        analyzer['routes_avg_duration'] = mp.newMap(numelements=688,
                                     maptype='PROBING', loadfactor=0.5)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=688)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addTrip(analyzer, trip):

    if trip['Trip  Duration'] == "0":
        pass
    else:
        origin_id = int(trip['Start Station Id'])
        if not gr.containsVertex(analyzer['connections'], origin_id):
            gr.insertVertex(analyzer['connections'], origin_id)
        destination_id = int(trip['End Station Id'][0:len(trip['End Station Id'])-2])
        if not gr.containsVertex(analyzer['connections'], destination_id):
            gr.insertVertex(analyzer['connections'], destination_id)
        duration = float(trip['Trip  Duration'])
        #agregar estaciones de origen a tabla de hash
        if mp.contains(analyzer['routes_avg_duration'], origin_id):
            entry = mp.get(analyzer['routes_avg_duration'], origin_id)
            destinations_map = me.getValue(entry)
            #verificar estaciones de destino
            if mp.contains(destinations_map, destination_id):
                entry2 = mp.get(destinations_map, destination_id)
                trip_duration = me.getValue(entry2)
                trip_duration['duration'] += duration
                trip_duration['counter'] += 1
            else:
                mp.put(destinations_map, destination_id, {'duration':duration, 'counter':1})
        else:
            mp.put(analyzer['routes_avg_duration'], origin_id, mp.newMap(numelements=688, maptype='PROBING', loadfactor=0.5))





def createTripsGraph(analyzer):

    #crear vertices con el id de las estaciones
    
    origin_list = mp.keySet(analyzer['routes_avg_duration'])
    for key in lt.iterator(origin_list):
        destinations_map = mp.get(analyzer['routes_avg_duration'], key)['value']
        destinations_list = mp.keySet(destinations_map)
        for key2 in lt.iterator(destinations_list):
            entry = mp.get(destinations_map, key2)
            trip_info = me.getValue(entry)
            avg_duration = trip_info['duration']/float(trip_info['counter'])
            #addConnection(analyzer['connections'], key, key2, avg_duration)
            gr.addEdge(analyzer['connections'], key, key2, avg_duration)

    #print(gr.vertices(analyzer['connections']))
        
    return analyzer




def addConnection(analyzer, origin, destination, avg_duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, avg_duration)
    return analyzer

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

"""
geoprocess.py
Funções geográficas (Haversine) e filtragem por raio.
"""

from math import radians, sin, cos, asin, sqrt
from typing import List, Dict

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula distância aproximada em quilômetros entre dois pontos
    usando fórmula Haversine.
    Entradas em graus decimais.
    """
    R = 6371.0  # raio médio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def locais_proximos(origem_lat: float, origem_lon: float, locais: List[Dict], raio_km: float) -> List[Dict]:
    """
    Recebe coordenada de origem e lista de locais (cada um com
    'coordenadas': {'latitude', 'longitude'}) e retorna apenas os que
    estão dentro de `raio_km`, ordenados pela distância.
    """
    resultado = []
    for loc in locais:
        lat = None
        lon = None
        coords = loc.get("coordenadas") or {}
        lat = coords.get("latitude")
        lon = coords.get("longitude")
        if lat is None or lon is None:
            continue
        dist = haversine(origem_lat, origem_lon, lat, lon)
        if dist <= raio_km:
            item = loc.copy()
            item["distancia_km"] = round(dist, 3)
            resultado.append(item)
    resultado.sort(key=lambda x: x["distancia_km"])
    return resultado

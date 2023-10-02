import pandas as pd
import urllib.request
import json

servers = {                # Listado de servers en un diccionario para que las querys se realicen en cada uno de ellos.
    'br1': 'br1',
    'eun1': 'eun1',
    'euw1': 'euw1',
    'jp1': 'jp1',
    'kr': 'kr',
    'la1': 'la1',
    'la2': 'la2',
    'na1': 'na1',
    'oc1': 'oc1',
    'ru': 'ru',
    'tr1': 'tr1',
}

api_key = 'RGAPI-99b5528d-8b18-45be-a28b-a313046dbf84'  # Reemplaza con tu propia clave de API de RiotGames

def get_summoner_data(userName, server_region):     # Esta función recibe el Nombre del usuario y la región para consultar los datos del usuario ingresado
    url = f'https://{server_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{userName}?api_key={api_key}'
    
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f'No se encontraron datos para {userName} en {server_region}')
        else:
            print(f'Error al obtener datos para {userName} en {server_region}. Código de error: {e.code}')
    except Exception as e:
        print(f'Ocurrió un error: {str(e)}')
    return None

def datosUser(userName):        # Esta es la función la cual itera entre servidores y guarda los datos extraidos en un DataFrame para luego limpiarlos con Pandas
    user_per_server = {}
    for server_name, server_region in servers.items():
        summoner_data = get_summoner_data(userName, server_region)
        if summoner_data:
            user_per_server[server_name] = summoner_data
    df = pd.DataFrame.from_dict(user_per_server, orient='index')
    
    return df

# Ingresa el nombre de usuario del usuario
userName = input("Inserte UserName sin espacios: ")

# Llama a la función para obtener datos del usuario
df = datosUser(userName)

# Imprime el DataFrame
print(df)

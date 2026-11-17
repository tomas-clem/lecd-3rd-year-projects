import boto3
from bs4 import BeautifulSoup, element
import re
import requests
import time
from tqdm import tqdm
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import json
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import googlemaps

boto3.setup_default_session(profile_name='pecd',region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

def get_db_ids():
    response = client.scan(TableName="houses")
    #print(response["ResponseMetadata"]["HTTPStatusCode"])
    #print(response)
    ids = list(map(lambda x: x["id"]["S"],response["Items"]))
    return response["Items"]

#response = get_db_ids()

#print(len(response))

#with open('data.json', 'w') as f:
    #json.dump(response, f)

#print(response)
#print(len(response))

#anocon = {}

#print(response[0]["id"]["S"])

#for i in range(len(response)):
    #try:
        #anocon[response[i]["id"]["S"]] = {"ano_construcao" : response[i]['built_in']['S']}
    #except:
        #anocon[response[i]["id"]["S"]] = {"ano_construcao" : response[i]['built_in']['NULL']}

f = open('data.json', encoding="utf8")
data = json.load(f)
output = []
for i in range(len(data)):
    output.append(data[i]['price']['S'])

#Processamento dos dados

df = pd.read_json(r'data.json')
#print(df.columns)
print(df.columns)

output = df['price']

input = df.drop(columns=['id','price'])
#print(input)

#print(input['amenities'])
amenities = []
for i in range(len(input['amenities'])):
    try:
        aux = ""
        for j in range(len(input['amenities'][i]['L'])):
            aux = aux + " " + str(input['amenities'][i]['L'][j]['S'])
        amenities.append(aux)
    except:
        #str(input['built_in'][i]['NULL'])
        amenities.append(None)

input['amenities'] = amenities

#print(input['amenities'])
#print(df['built_in'])

built = []
for i in range(len(input['built_in'])):
    try:
        built.append(input['built_in'][i]['S'])
    except:
        #
        built.append(-1)

input['built_in'] = built

#print(input['location'])
location = []
for i in range(len(input['location'])):
    location.append(input['location'][i]['S'])

input['location'] = location

tipo = []
for i in range(len(input['tipology'])):
    tipo.append(input['tipology'][i]['S'][1:])

input['tipology'] = tipo

mdois = []
for i in range(len(input['m2'])):
    mdois.append(input['m2'][i]['S'][:-2])

input['m2'] = mdois

mdoisu = []
for i in range(len(input['m2_util'])):
    mdoisu.append(input['m2_util'][i]['S'][:-2])

input['m2_util'] = mdoisu

timestamp = []
for i in range(len(input['timestamp'])):
    try:
        timestamp.append(input['timestamp'][i]['S'])
    except:
        timestamp.append(str(input['timestamp'][i]))
input['timestamp'] = timestamp

for i in np.where(input['timestamp'] == 'nan'):
    input['timestamp'][i] = -1

ene = []
for i in range(len(input['energetic_efficiency'])):
    try:
        ene.append(input['energetic_efficiency'][i]['S'])
    except:
        ene.append(str(input['energetic_efficiency'][i]['NULL']))


input['energetic_efficiency'] = ene

type = []
for i in range(len(input['house_type'])):
    type.append(input['house_type'][i]['S'])

input['house_type'] = type
out = []
for i in range(len(output)):
    out.append(int(output[i]['S'][:-1].replace(",","")))

output = out
maximoout = np.max(output)
output = output/np.max(output)

output = np.append(output,maximoout)

output = pd.DataFrame(output)



#print(output)
colunas = ['built_in', 'tipology', 'amenities', 'm2', 'm2_util','timestamp', 'energetic_efficiency', 'house_type']
#for j in colunas:
    #print(input[j])

encoder = LabelEncoder()
input['amenities'] = encoder.fit_transform(input['amenities'])

input['house_type'] = encoder.fit_transform(input['house_type'])

#print(input['house_type'])

encoder = LabelEncoder()
input['energetic_efficiency'] = encoder.fit_transform(input['energetic_efficiency'])

#print(input['energetic_efficiency'])

#print(input['location'])

gmaps = googlemaps.Client(key='{google_maps_api_key}')

# Geocoding an address
#for i in range(len(input['locations'])):
#lat = []
#lng = []
for i in range(len(input['location'])):
    #geocode_result = gmaps.geocode(input['location'][i])
    #lat.append(geocode_result[0]['geometry']['location']['lat'])
    #lng.append(geocode_result[0]['geometry']['location']['lng'])
    pass

#print(lat[:10])
#print(lng[:10])

#fp= open(r'coordenadas.txt', 'w')
#fp.write(str(lat))
#fp.write("\n" + str(lng))


with open(r'coordenadas.txt', 'r') as fp:
    # Lê todas as linhas do arquivo
    linhas = fp.readlines()

latitudes = linhas[0][1:-2]
longitudes = linhas[1][1:-2]

#print(latitudes)

latitudes = latitudes.split(",")
longitudes = longitudes.split(",")
for i in range(len(latitudes)):
    latitudes[i] = float(latitudes[i])
    longitudes[i] = float(longitudes[i])

input['latitude'] = latitudes
input['longitude'] = longitudes

    #input[i] = np.array(input[i]) / input[i].max()
    #print(input[i])

input = pd.DataFrame(input)
input = input.drop(columns=['location'])

for i in input.columns:
    input[i] = input[i].astype(float)
    input[i] = np.array(input[i]).astype(float) / np.max(input[i])
#input = input.values.tolist()

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((lat,long))

#for j in colunas:
    #print(input[j])

#input.to_csv('input.csv', index=False)
output.to_csv('output.csv',index=False)

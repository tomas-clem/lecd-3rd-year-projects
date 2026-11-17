import pickle
import json
import googlemaps
import numpy as np
import pandas as pd
import uuid
import boto3
from scipy.spatial import KDTree
import os

modelo13 = pickle.load(open("../Scripts/modelos/modelo_dist13.pkl", 'rb'))
modelo14 = pickle.load(open("../Scripts/modelos/modelo_dist14.pkl", 'rb'))
modelo15 = pickle.load(open("../Scripts/modelos/modelo_dist15.pkl", 'rb'))
modelo16 = pickle.load(open("../Scripts/modelos/modelo_dist16.pkl", 'rb'))
modelo23 = pickle.load(open("../Scripts/modelos/modelo_dist23.pkl", 'rb'))
modelo27 = pickle.load(open("../Scripts/modelos/modelo_dist27.pkl", 'rb'))
modelooutro = pickle.load(open("../Scripts/modelos/modelo_dist_outros.pkl", 'rb'))

distrito = pd.read_csv('../Scripts/distritos_centro.csv')

gmaps = googlemaps.Client(key='{google_maps_api_key}')


f = open('../Scripts/desnormalizar.json')
 
dicio = json.load(f)

dicio2 = {"tipo_imovel":7, "latitude":0,"longitude":0,"area":500,"tipologia":14,"Price":10000000000}
distrito = pd.read_csv('../Scripts/distritos_centro.csv')
distrito['ID'] = [i for i in range(len(distrito))]

amenities =  {' air conditioning': 0, ' air conditioning garden': 1, ' air conditioning green areas': 2, ' air conditioning swimming pool': 3, ' air conditioning swimming pool garden': 4, ' air conditioning swimming pool green areas': 5, ' garden': 6, ' green areas': 7, ' swimming pool': 8, ' swimming pool garden': 9, ' swimming pool green areas': 10, None: 11}

boto3.setup_default_session(profile_name='default',region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

response = client.scan(TableName="houses")


def amenitiess(lista):
    if len(lista[1]) == 0:
        lista[1] = 1
    else:
        aux = " ".join(lista[1])
        lista[1] = amenities[aux]
    return lista

def desamenitiess(lista):
    for i in amenities:
        if lista[2] == 1:
            lista[2] = None
            break
        if lista[2] == amenities[i]:
            lista[2] = i
    return lista
    

x = [i for i in range(len(dicio)-1)]
def normalizar(lista):
    temp = []
    for i,j in zip(dicio,x):
        temp.append(float(lista[j]) / float(dicio[i]))
    return temp

def desnormalizar_preco(pred):
    return int(dicio['price']*pred)

def prever(lista,modelo):
    pred = modelo.predict([lista])[0]
    pred = desnormalizar_preco(pred)

    return pred

def desnormalizar(lista):
    temp = []
    for i,j in zip(dicio,x):
        temp.append(int(float(lista[j]) * float(dicio[i])))
    return temp

def intervalo(pred):
    max = int(pred-pred*0.05)
    min = int(pred+pred*0.05)
    return [max,min]

def cor(valor,intervalo):
    min = intervalo[0]
    max = intervalo[1]
    cor = ''
    if valor == "":
        return "white"
    valor= int(valor)
    if (valor < max) & (valor > min):
        cor = "green"
    elif (valor < min):
        cor = "darkgreen"
    elif (valor > min) & (valor > max-max*0.05):
        cor = "yellow"
    elif (valor >   max-max*0.05):
        cor = "red"
    return cor

def obter_lat_long(X_train):
    data_train = []
    for lat, lon in zip(X_train['latitude'], X_train['longitude']):
        coord = [lat, lon]
        data_train.append(coord)
    data_train = np.array(data_train)
    return data_train

def coordenadas(x):
    response = gmaps.geocode(x)
    latitude = response[0]['geometry']['location']['lat']
    longitude = response[0]['geometry']['location']['lng']
    return np.array([[latitude,longitude]])


def kmeans_1(data_train): 

    centroides = obter_lat_long(distrito)
    labels = np.argmin(np.array([np.linalg.norm(data_train - centroide, axis=1) for centroide in centroides]), axis=0)
    return labels[0]


def modelo_distrito(label_knn):
    match(label_knn):
        case 13: 
            modelo = modelo13
        case 14: 
            modelo = modelo14

        case 15:
            modelo = modelo15

        case 16: 
            modelo = modelo16

        case 23: 
            modelo = modelo23

        case 27: 
            modelo = modelo27
        case default:
            modelo = modelooutro
    return modelo

class norm:
    @staticmethod
    def typology(value):
        aux = 0
        val = int(value.split(" a ")[0][1:])
        if val >=0 and val <= 10:
            return val+1
        elif val == 13:
            return 12
        elif val == 17:
            return 13
        else:
            return 14
    
    def reverse_typology(value):
        aux = "T"
        val = str(value)
        return aux + val
    
    def energy_certificate(value):
        aux = 0
        match value:
            case "A+":
                aux = 1
            case "A":
                aux = 2
            case "B":
                aux = 3
            case "B-":
                aux = 4
            case "C":
                aux = 5
            case "D":
                aux = 6
            case "E":
                aux = 7
            case "F":
                aux = 8
            case "G":
                aux = 9
        return aux  
        
    def house_type(value):
        aux = 0
        match value:
            case "Isolado":
                aux = 1
            case "Apartamento":
                aux = 2
            case "Casa / Moradia":
                aux = 3
            case "Quinta / Monte":
                aux = 4
            case "Palácio":
                aux = 5
            case "Moinho":
                aux = 6
        return aux
    def reverse_house_type(value):
        aux = ""
        match value + 1:
            case 1:
                aux = "Isolado"
            case 2:
                aux = "Apartamento"
            case 3:
                aux = "Casa / Moradia"
            case 4:
                aux = "Quinta / Monte"
            case 5:
                aux = "Palácio"
            case 6:
                aux = "Moinho"
        return aux

def form_to_house(form,_id):
        coord = coordenadas(form["morada"])
        house = {
            "house_id":str(uuid.uuid4()),
            "user_id":_id,
            "address":form["morada"],
            "lat":str(coord[0][0]),"lon":str(coord[0][1]),
            "typology":form["q1"],
            "area":form["q3"],
            "area_util":form["q4"],
            "age":int(form["q6"]),
            "extras":form.getlist('extras[]'),
            "energy_certificate":form["q5"],
            "house_type":form["q2"],
            "price": form["q7"]
            }
        return house

def form_to_house2(form,_id):
        coord = coordenadas(form["morada"])
        house = {
            "house_id":str(uuid.uuid4()),
            "user_id":_id,
            "address":form["morada"],
            "lat":str(coord[0][0]),"lon":str(coord[0][1]),
            "typology":form["q1"],
            "area":form["q3"],
            "area_util":form["q4"],
            "age":int(form["q6"]),
            "extras":form.getlist('extras[]'),
            "energy_certificate":form["q5"],
            "house_type":form["q2"]
            }
        return house

def get_price(house):
    coord = coordenadas(house["address"])
    listaprev = [house["age"],house["extras"],norm.typology(house["typology"]),norm.energy_certificate(house["energy_certificate"]),norm.house_type(house["house_type"])]

    kmeans = kmeans_1(coord)
    model = modelo_distrito(kmeans)
    listaprev = amenitiess(listaprev)
    listaprev = normalizar(listaprev)
    return prever(listaprev,model)


def datasetusar(x):
    match x:
        case 0:
            dataset = pd.read_csv('../Scripts/Datasets/df_Viana_0.csv')
        case 1:
            dataset = pd.read_csv('../Scripts/Datasets/df_Braga_1.csv')
        case 2:
            dataset = pd.read_csv('../Scripts/Datasets/df_Vila_Real_2.csv')
        case 3:
            dataset = pd.read_csv('../Scripts/Datasets/df_Branganca_3.csv')
        case 4:
            dataset = pd.read_csv('../Scripts/Datasets/df_Porto_4.csv')
        case 5:
            dataset = pd.read_csv('../Scripts/Datasets/df_Aveiro_5.csv')
        case 6:
            dataset = pd.read_csv('../Scripts/Datasets/df_Viseu_6.csv')
        case 7:
            dataset = pd.read_csv('../Scripts/Datasets/df_Guarda_7.csv')
        case 8:
            dataset = pd.read_csv('../Scripts/Datasets/df_Coimbra_8.csv')
        case 9:
            dataset = pd.read_csv('../Scripts/Datasets/df_Castelo_Branco_9.csv')
        case 10:
            dataset = pd.read_csv('../Scripts/Datasets/df_Leiria_10.csv')
        case 11:
            dataset = pd.read_csv('../Scripts/Datasets/df_Santarem_11.csv')
        case 12:
            dataset = pd.read_csv('../Scripts/Datasets/df_Lisboa_12.csv')
        case 13:
            dataset = pd.read_csv('../Scripts/Datasets/df_Portalegre_13.csv')
        case 14:
            dataset = pd.read_csv('../Scripts/Datasets/df_Setubal_14.csv')
        case 15:
            dataset = pd.read_csv('../Scripts/Datasets/df_Evora_15.csv')
        case 16:
            dataset = pd.read_csv('../Scripts/Datasets/df_Beja_16.csv')
        case 17:
            dataset = pd.read_csv('../Scripts/Datasets/df_Faro_17.csv')
        case 18:
            dataset = pd.read_csv('../Scripts/Datasets/df_Madeira_18.csv')
        case 19:
            dataset = pd.read_csv('../Scripts/Datasets/df_Porto_Santo_19.csv')
        case 20:
            dataset = pd.read_csv('../Scripts/Datasets/df_ilhas_20_1_2_4_5_6_8.csv')
        case 21: 
            dataset = pd.read_csv('../Scripts/Datasets/df_ilhas_20_1_2_4_5_6_8.csv')
        case 22: 
            dataset = pd.read_csv('../Scripts/Datasets/df_ilhas_20_1_2_4_5_6_8.csv')
        case 23: 
            dataset = pd.read_csv('../Scripts/Datasets/df_Terceira_23.csv')
        case 24: 
            dataset = pd.read_csv('../Scripts/Datasets/df_ilhas_20_1_2_4_5_6_8.csv')
        case 25: 
            dataset = pd.read_csv('../Scripts/Datasets/df_ilhas_20_1_2_4_5_6_8.csv')
        case 26: 
            dataset = pd.read_csv('../Scripts/Datasets/df_ilhas_20_1_2_4_5_6_8.csv')
        case 27:
            dataset = pd.read_csv('../Scripts/Datasets/df_Sao_Miguel_27.csv')  
        case default:
            dataset = pd.read_csv('../Scripts/Datasets/df_Lisboa_12.csv')
    return dataset

def desnormalizar2(lista):
    for i in range(len(lista)):
        lista[i].tipo_imovel = norm.reverse_house_type(int(lista[i].tipo_imovel * dicio2["tipo_imovel"]))
        lista[i].area = str(int(lista[i].area * dicio2["area"])) + "m²"
        lista[i].tipologia = norm.reverse_typology(int(lista[i].tipologia * dicio2["tipologia"]))

    return lista

def normalizar2(lista):
    for i in range(len(lista)):
        lista[i] = lista[i] / dicio2[i-3]
    return lista

def prever2(lista,modelo):
    pred = modelo.predict([lista])[0]
    return pred 

def get_price2(house):
    coord = coordenadas(house["address"])
    listaprev = [house["age"],house["extras"],norm.typology(house["typology"]),norm.energy_certificate(house["energy_certificate"]),norm.house_type(house["house_type"])]
    kmeans = kmeans_1(coord)
    model = modelo_distrito(kmeans)
    listaprev = amenitiess(listaprev)
    listaprev = normalizar2(listaprev)
    return prever2(listaprev,model)


def maisprox(querie,dataset):
    ids = dataset["ID"]
    datasetaux = dataset.copy()
    datasetaux = dataset.drop(columns=['ID', 'Price','Price_norm'])
    datasetaux = datasetaux.values.tolist()
    ids = ids.values.tolist()

    kdtree = KDTree(datasetaux)

    distancias, indices = kdtree.query(querie, k=10)
    listaprox = [dataset.loc[i] for i in indices]
    
    return listaprox

def morada(lat,long):
    reverse_geocode_result = gmaps.reverse_geocode((int(lat),int(long)))
    return reverse_geocode_result


def definirdfchoro(opcao):
    df = pd.read_csv("../Scripts/teste.csv")
    if opcao == "Last3monts":
        df = df.groupby(["District"])["Price"].mean()
    elif opcao == "abril":
        df =df[df["Month"] == "abril"]
    elif opcao == "janeiro":
        df =df[df["Month"] == "janeiro"]
    elif opcao == "março":
        df =df[df["Month"] == "março"]
    else:
        df = df.groupby(["District"])["Price"].mean()
    return df

def definirdtend(opcao):
    df = pd.read_csv("../Scripts/teste.csv")
    match opcao:
        case "Azores":
            df = df[df["District"] == "Azores"]
        case "Aveiro":
            df = df[df["District"] == "Aveiro"]
        case "Beja":
            df = df[df["District"] == "Beja"]
        case "Braga":
            df = df[df["District"] == "Braga"]
        case "Bragança":
            df = df[df["District"] == "Bragança"]
        case "CasteloBranco":
            df = df[df["District"] == "CasteloBranco"]
        case "Coimbra":
            df = df[df["District"] == "Coimbra"]
        case "Évora":
            df = df[df["District"] == "Évora"]
        case "Faro":
            df = df[df["District"] == "Faro"]
        case "Guarda":
            df = df[df["District"] == "Guarda"]
        case "Leiria":
            df = df[df["District"] == "Leiria"]
        case "Lisboa":
            df = df[df["District"] == "Lisboa"]
        case "Portalegre":
            df = df[df["District"] == "Portalegre"]
        case "Porto":
            df = df[df["District"] == "Porto"]
        case "Santarém":
            df = df[df["District"] == "Santarém"]
        case "Setúbal":
            df = df[df["District"] == "Setúbal"]
        case "VianadoCastelo":
            df = df[df["District"] == "VianadoCastelo"]
        case "VilaReal":
            df = df[df["District"] == "VilaReal"]
        case "Viseu":
            df = df[df["District"] == "Viseu"]
        case "Madeira":
            df = df[df["District"] == "Madeira"]
    return df
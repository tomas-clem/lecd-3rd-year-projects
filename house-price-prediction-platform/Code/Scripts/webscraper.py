import boto3
from bs4 import BeautifulSoup, element
import re
import requests
import time
from tqdm import tqdm

boto3.setup_default_session(profile_name='pecd',region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table('houses')

BASE_URL = "https://www.idealista.pt"
HEADERS = {"Accept-Language": "en-US,en;q=0.5","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0"}


def get_regions():
    r = requests.get(BASE_URL,headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a", class_= "subregion")
    regions = []
    for result in results:
        r2 = requests.get(BASE_URL+result["href"],headers=HEADERS)
        soup2 = BeautifulSoup(r2.text, "html.parser")
        data = {
            "name": result.text,
            "link": result["href"].replace("concelhos-freguesias",""),
            "house_count": int(re.search(r"[\d.]+",soup2.find("a",id="showAllLink")["title"])[0].replace(".",""))
        }
        if data["house_count"] >= 1800:
            for li in soup2.find(id="location_list"):
                if isinstance(li, element.NavigableString):
                    continue
                for result in li.find('ul'):
                    region  = result.find("a")
                    if region != -1:
                        regions.append({"link":region["href"]})
        else:
            regions.append(data)
    return regions

def get_houses(region,i):
    houses_ids = []
    r = requests.get(BASE_URL+region+"?ordem=atualizado-desc", headers=HEADERS)
    soup = BeautifulSoup(r.text,'html.parser')
    for house in soup.find_all("a", class_ ="item-link"):
        id = re.search(r"\d+",house["href"])[0]
        if id in DB_IDS:
            return houses_ids
        houses_ids.append(id)
    if soup.find("a", class_="icon-arrow-right-after"):
        if i % 5 == 0:
            print(i)
            time.sleep(1)
        houses_ids.extend(get_houses(soup.find("a", class_="icon-arrow-right-after")["href"].replace("?ordem=atualizado-desc",""),i+1))
    return houses_ids

def get_house_details(id):
    r = requests.get(BASE_URL+"/en/imovel/"+id+"/", headers=HEADERS)
    soup = BeautifulSoup(r.text,"html.parser")
    features = soup.find("div", class_="details-property_features").findAll("li") if soup.find("div", class_="details-property_features") else None
    features_2 = soup.find("div",class_="details-property-feature-two")
    area = re.findall(r"(\d+ m²)",list(filter(lambda x: "m²" in x.text, features))[0].text)
    built_in = list(filter(lambda x: "Built in" in x.text, features))
    data = {
        "id":id,
        "price":soup.find("span",class_="info-data-price").text,
        "m2": area[0],
        "tipology": soup.find("div", class_="info-features").findAll("span")[1].text.replace("\n",""),
        "location": re.search(r"((?<=sale in ).+|((?<=, ).+))",soup.find("span", class_="main-info__title-main").text)[0] + " , "+soup.find("span",class_="main-info__title-minor").text,
        "house_type":re.search(r"[^T\d ].+(?= for sale)",soup.find("span", class_="main-info__title-main").text)[0],
        "m2_util":area[1] if len(area) > 1 else area[0],
        "energetic_efficiency":soup.select('span[class*="icon-energy-c"]')[0]["title"] if soup.select('span[class*="icon-energy-c"]') else None,
        "built_in":re.search(r"\d+",built_in[0].text)[0] if built_in else None,
        "amenities": list(map(lambda x: x.text.replace("\n",""),features_2.find("ul").find_all("li"))) if (features_2.find("h2").text =="Amenities") else None,
        "timestamp":str(time.time())
    }
    table.put_item(Item=data)

def get_db_ids():
    response = client.scan(TableName="houses",ProjectionExpression="id")
    print(response["ResponseMetadata"]["HTTPStatusCode"])
    ids = list(map(lambda x: x["id"]["S"],response["Items"]))
    return ids

DB_IDS = get_db_ids()
REGIONS = get_regions()
ids = []
for region in tqdm(REGIONS,"Getting house ids"):
    print(region)
    ids.extend(get_houses(region["link"],1))
i = 0
for id in tqdm(ids,"Getting house details"):
    if i % 5 == 0:
        time.sleep(1)
    get_house_details(id)
    i+=1

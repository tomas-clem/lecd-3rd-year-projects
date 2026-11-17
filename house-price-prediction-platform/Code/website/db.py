import boto3
from boto3.dynamodb.conditions import Key
import bcrypt 
import uuid
import secrets
from datetime import datetime, timedelta
import re
import random



boto3.setup_default_session(region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table('users')
recovery_table = dynamodb.Table("recovery")
favorites_table = dynamodb.Table("favorites")


def query_table(table_name, key=None, value=None,LastEvaluatedKey=None):
    table = dynamodb.Table(table_name)

    if key is not None and value is not None:
        filtering_exp = Key(key).eq(value)
        if LastEvaluatedKey is not None:
            return table.query(IndexName='user_id-index',KeyConditionExpression=filtering_exp,Limit=10,ExclusiveStartKey=LastEvaluatedKey)
        return table.query(IndexName='user_id-index',KeyConditionExpression=filtering_exp,Limit=10)

def check_password(password):
    return re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",password)
    
def get_usertable():
    return table

def get_user(email):
    return table.get_item(Key={"email":email})
def get_user_by_id(id):
    return table.get_item(Key={"id":id})

def get_favorites(user_id,LastEvaluatedKey=None):
    response = query_table("favorites","user_id",user_id,LastEvaluatedKey)
    print(response)
    lk = response["LastEvaluatedKey"] if "LastEvaluatedKey" in response else 0
    return response["Items"],lk

def get_house(house_id,user_id):
    return favorites_table.get_item(Key={"house_id":house_id,"user_id":user_id})["Item"]
def delete_fav(house_id,user_id):
    favorites_table.delete_item(Key={"house_id":house_id,"user_id":user_id})

def login(email,password):
    user = get_user(email)
    if("Item" in user):
        _hash = bytes(user["Item"]["hash"])
        passwordBytes = password.encode('utf-8') 
        return bcrypt.checkpw(passwordBytes,_hash)
    return False

def add_price_history(house_id,user_id,price):
    house = get_house(house_id,user_id)
    house["price_history"] = house.get("price_history",[])
    house["price_history"].append([price,str(datetime.timestamp(datetime.now()))])
    print(house["price_history"],1)
    favorites_table.put_item(Item=house)


def register(email,password,name):
    user = get_user(email)
    if("Item" not in user):
        _bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        _hash = bcrypt.hashpw(_bytes, salt)
        unique_id = str(uuid.uuid4())
        table.put_item(Item={"email":email,"hash":_hash,"id":unique_id,"username":name})
        return True
    return False

def create_recover_link(email):
    dt = datetime.now()
    dt += timedelta(minutes=15)
    ts = datetime.timestamp(dt)
    token = secrets.token_urlsafe()
    recovery_table.put_item(Item={"PasswordResetToken":token,"PasswordResetExpiration":str(ts),"email":email})
    return token

def check_recover_link(token,timestamp):
    response = recovery_table.get_item(Key={"PasswordResetToken":token})
    if("Item" in response):
        print(timestamp)
        if( timestamp < float(response["Item"]["PasswordResetExpiration"])):
            return response["Item"]["email"]
def change_password(email,password):
    response = table.get_item(Key={"email":email})
    item = response["Item"]
    _bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    _hash = bcrypt.hashpw(_bytes, salt)
    item["hash"] = _hash
    table.put_item(Item=item)
    

def get_user_id(email):
    user = get_user(email)
    if(user):
        return user["Item"]["id"]
    return None

def save_fav(house):
    favorites_table.put_item(Item=house)
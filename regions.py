import pymongo
from pymongo import MongoClient

myclient = MongoClient("mongodb://root:N5tfgb9QExIGYXIq@cluster0-shard-00-00.e4swe.mongodb.net:27017,cluster0-shard-00-01.e4swe.mongodb.net:27017,cluster0-shard-00-02.e4swe.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-biz1ll-shard-0&authSource=admin&retryWrites=true&w=majority")
#myclient = MongoClient('localhost:27017')
#myclient = MongoClient("mongodb+srv://Customer:customer@cluster0.usknk.mongodb.net/Customer?retryWrites=true&w=majority")

mydb = myclient["Customer"]
mycol = mydb["regions"]

data = [
    {

        "region": "Africa"
    },
    {

        "region": "Australia"
    },
    {

        "region": "Austria"
    },
    {

        "region": "Asia Pacific"
    },
    {

        "region": "Brazil"
    },
    {

        "region": "Canada"
    },
    {

        "region": "Chile"
    },
    {

        "region": "China"
    },
    {

        "region": "Denmark"
    },
    {

        "region": "North Europe"
    },
    {

        "region": "France"
    },
    {

        "region": "Germany"
    },
    {

        "region": "Greece"
    },
    {

        "region": "Central India"
    },
    {

        "region": "Indonesia"
    },
    {

        "region": "Israel"
    },
    {

        "region": "Italy"
    },
    {

        "region": "Japan"
    },
    {

        "region": "Korea"
    },
    {

        "region": "Malaysia"
    },
    {

        "region": "Mexico"
    },
    {

        "region": "New Zealand"
    },
    {

        "region": "Norway"
    },
    {

        "region": "Poland"
    },
    {

        "region": "Qatar"
    },
    {

        "region": "Spain"
    },
    {

        "region": "Sweden"
    },
    {

        "region": "Switzerland"
    },
    {

        "region": "Taiwan"
    },
    {

        "region": "UAE"
    },
    {

        "region": "UK"
    },
    {

        "region": "US"
    }
]


x = mycol.insert_many(data)

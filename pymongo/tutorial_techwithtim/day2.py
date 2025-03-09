from dotenv import load_dotenv , find_dotenv
import os
import pprint
from pymongo import MongoClient,errors
from bson.objectid import ObjectId
from datetime import datetime
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://blueaves15:{password}@trainingclustor.nl44poy.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)



production = client.production 

def create_book_collection():
    book_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            # "title": "Book Object Validation",
            "required": [ "title", "authors", "publish_date", "type", "copies" ],
            "properties": {
                "title": {
                "bsonType": "string",
                "description": "must be a string and is required"
                },
                "authors": {
                "bsonType": "array",
                "items":{
                    "bsonType": "objectId",
                    "description": "must be a objectId and is required"
                }
                },   
                "publish_date": {
                "bsonType": "date",
                "description": "must be a string and is required"
                },  
                "type": {
                    "enum": ["Fiction", "Non-Fiction"],
                    "description": "must be a enum and is required"
                },   
                "copies": {
                "bsonType": "int",
                "minimum": 0,
                "description": "must be a integer grater than 0 and is required"
                },
            }
        }
    }

    try:
        production.create_collection("book")
    except errors.CollectionInvalid as er:
        print(er)
    except errors.OperationFailure as OP:
        print(OP)

    production.command("collMod", "book", validator = book_validator)
create_book_collection()
def create_author_collection():
    author_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "title": "author Object Validation",
            "required": [ "first_name", "last_name", "date_of_birth" ],
            "properties": {
                "first_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
                },
                "last_name": {
                  "bsonType": "string",
                "description": "must be a string and is required"
                },
                "date_of_birth": {
                "bsonType": "date",
                "description": "must be a date and is required"
                }, 
            }}

    }
    try:
        production.create_collection("author")
    except errors.CollectionInvalid as er:
        print(er)
    except errors.OperationFailure as OP:
        print(OP)

    production.command("collMod", "author", validator = author_validator)

# create_author_collection()

def create_data():
    authors = [
        {
        "first_name":"ashish",
        "last_name": "bindra",
        "date_of_birth": datetime(1998,7,20)
        },  {
        "first_name":"sonu",
        "last_name": "bindra",
        "date_of_birth": datetime(1995,7,10)
        },  {
        "first_name":"sershti",
        "last_name": "bindra",
        "date_of_birth": datetime(1996,7,2)
        }, 
         {
        "first_name":"sapna",
        "last_name": "bindra",
        "date_of_birth": datetime(1850,2,20)
        },  {
        "first_name":"sarvesh",
        "last_name": "bindra",
        "date_of_birth": datetime(1940,3,20)
        },
    ]
    
    author_collection = production.author
    authors_ids = author_collection.insert_many(authors).inserted_ids
    print(authors_ids)
    books = [
        {
            "title": "MongoDB Advance",
            "authors": [authors_ids[0]],
            "publish_date": datetime.today(),
            "type": "Non-Fiction",
            "copies":5
        }, {
            "title": "python Advance",
            "authors": [authors_ids[1]],
            "publish_date": datetime.today(),
            "type": "Non-Fiction",
            "copies":5
        },
        # {
        #     "title": "Java Advance",
        #     "authors": [authors_ids[3]],
        #     "publish_date": datetime.today(),
        #     "type": "Non-Fiction",
        #     "copies":5
        # },
        {
            "title": "Ninteen Advance",
            "authors": [authors_ids[4]],
            "publish_date": datetime(1949,3,5),
            "type": "Fiction",
            "copies":5
        }, {
            "title": "pandas Advance",
            "authors": [authors_ids[1]],
            "publish_date": datetime.today(),
            "type": "Fiction",
            "copies":5
        }, {
            "title": "Marry",
            "authors": [authors_ids[3]],
            "publish_date": datetime(2012,2,14),
            "type": "Fiction",
            "copies":5
        }, 
        {
            "title": "Moby Dick",
            "authors": [authors_ids[2]],
            "publish_date": datetime(1800,9,23),
            "type": "Fiction",
            "copies":5
        },
    ]
    
    book_collection = production.book
    book_collection.insert_many(books)

# create_data()
printer = pprint.PrettyPrinter()

# book_containing_a = production.book.find({"title": {"$regex": "a{1}"}}) #atleast one a matched

# printer.pprint(list(book_containing_a))

# authors_and_books = production.author.aggregate([{
#     "$lookup": {
#         "from": "book",
#         "localField":"_id",
#         "foreignField": "authors",
#         "as":"boos"
#     }
# }])

# printer.pprint(list(authors_and_books))

authors_and_books_count = production.author.aggregate([
    {
        "$lookup": {
            "from": "book",
            "localField":"_id",
            "foreignField": "authors",
            "as":"books"
        },
    },
    {
        "$addFields": {
            "total_books": {"$size": "$books"}
        }
    },
    {
        "$project": {"first_name":1, "last_name": 1,"total_books":1, "_id":0} # should be in last
    }
])

# printer.pprint(list(authors_and_books_count))

# find age of the author with in 50 to 150 years
authors_and_books = production.book.aggregate([{
    "$lookup": {
        "from": "author",
        "localField":"authors",
        "foreignField": "_id",
        "as":"authors"
    }
} ,
{
    "$set":{
        "authors": {
            "$map":{
                "input":"$authors",
                "in":{
                    "age": {
                        "$dateDiff":{
                            "startDate": "$$this.date_of_birth",
                            "endDate": "$$NOW",
                            "unit": "year"
                        }
                        },
                        "first_name": "$$this.first_name",
                        "last_name": "$$this.last_name",
                }
            }
        }
    }
}
,{
    "$match":{
        "$and":[
            {"authors.age": {"$gte":50}},
            {"authors.age": {"$lte":150}},
        ]
    }
},{
    "$sort":{
        "age": 1
    }
}
])
printer.pprint(list(authors_and_books))
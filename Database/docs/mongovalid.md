# validation
```py
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

```

```py
from dotenv import load_dotenv , find_dotenv
import os
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://blueaves15:{password}@trainingclustor.nl44poy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

dbs = client.list_database_names()
print("list od dbs",dbs)

test_db = client.test 
collections = test_db.list_collection_names()
print("list of collections",collections)

def insert_test_doc():
    """
    get test collection from test database
    """

    collection = test_db.test_db
    test_document = {
        "name": "ashish",
        "type": "Test",
    }
    inserted_id = collection.insert_one(test_document).inserted_id

    print(inserted_id) # Bson Object ID

# insert_test_doc()

production = client.production
person_collection = production.person_collection

def create_document():
    first_names = ["sunny","bunny","cunny","vunny","munny"]
    last_names = ["imaggnry","imaggnry","imaggnry","imaggnry","imaggnry"]
    ages = [11,22,33,44,55]

    docs = []

    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first_name": first_name,
               "last_name": last_name,
               "age":age}
        docs.append(doc)
        # persion_collection.insert_one(doc)

    person_collection.insert_many(docs) 
    
# create_document()
printer = pprint.PrettyPrinter()

def find_all_people():
    people = person_collection.find()

    for person in people:
        # print(person)
        printer.pprint(person)

# find_all_people()

def find_name(name):
    name_is = person_collection.find_one({"first_name":name})
    printer.pprint(name_is)

# find_name("cunny")
    
def count_people():
    count = person_collection.count_documents(filter={})
    # or
    # count = person_collection.find().count() # number of element return by the find , we hav not to all the element , 
    # count() is debrecated
    print("Number of people",count)

# count_people()
    
def get_person_by_id(persion_id):

    _id = ObjectId(persion_id)
    persion = person_collection.find_one({"_id": _id})

    printer.pprint(persion)

# get_person_by_id("65c88c0529d602cdfab899cf")

def get_age_range(min_age, max_age):
    query = {
        "$and": [
            {"age": {"$gte": min_age}},
            {"age": {"$lte": max_age}}

        ]
    }
    people = person_collection.find(query).sort("age")

    for person in people:
        printer.pprint(person)

# get_age_range(20,35)

def project_columns():
    columns = {"_id":0, "first_name": 1, "last_name": 1}
    people = person_collection.find({}, columns)
    
    for person in people:
        printer.pprint(person)

# project_columns()

def update_person_by_id(persion_id):
    _id = ObjectId(persion_id)

    all_updates = {
        "$set": {"new_field": True}, # if field currently exisited we would orride that field
        "$inc": {"age": 1},
        "$rename": {"first_name": "first", "last_name": "last"}
    }

    # person_collection.update_one({"_id": _id}, all_updates)
    person_collection.update_one({"_id": _id}, {"$unset": {"new_field": ""}})


# update_person_by_id("65c88c0529d602cdfab899d2")
# print("update")

def replace_one(persion_id):
    _id = ObjectId(persion_id)

    new_doc = {
        "first_name": "ashish",
        "last_name": "bindra",
        "age":100
    }

    person_collection.replace_one({"_id": _id}, new_doc)

# replace_one("65c88c0529d602cdfab899cf")
    
def delete_doc_by_id(persion_id):
    _id = ObjectId(persion_id)
    person_collection.delete_one({"_id": _id})

# delete_doc_by_id("65c88c0529d602cdfab899cf")

def add_address_embed(persion_id, address):
    _id = ObjectId(persion_id)

    person_collection.update_one(
        {"_id": _id},{"$addToSet": {'addresses': address}}

    )
address={
    # "_id":"1",
    "street":"13",
    "number": 2456,
    "city":"patiala",
    "country": "india",
}
# add_address_embed("65c88c0529d602cdfab899d0",address=address)

def add_address_relationship(person_id, address):
    _id = ObjectId(person_id)
    
    address = address.copy()
    address["owner_id"] = person_id

    address_collection = production.address
    address_collection.insert_one(address)

add_address_relationship("65c88c0529d602cdfab899d2",address)

```


- first install pymongo `pip install pymongo[srv]`
- `pip install python-dotenv` 

No sql database like mongodb actually stores unstructured data and typically in json format
- Abiltiy to perform frequent changes to struce of the data
- Highly Flexible ()
- Faster quiery 
- saclable

## document model
-------------
database -> collections -> documents

Bson type satore

### find({})
-----
allow to insert a query object which is different properties that we are tyring to match when we are looking for elemnt or document.
-if we live empty it just find all document in collection
----
a curser is sothing that we can iterate over

## oprator
------
$set change the value of specific field create a new field to be a value, can use as overrite
 maily for new field
- $inc => we can increament value
- $rename =>  we can rename the field
- $unset =>  to remove a field
- $addToSet =>  add as an array
- $addFields => to add a new field
- $regex => regular expression
- $lookup => left outter join
- $projection => field to display
- $this => referance of cuurent elemants
- $dateDiff => to find the date differences
- $map => to itrate the elements

* replace_one()-> to replace a document without replacing and id

## schema validation
---------------
way to create a strucure in mongodb
allow to insert what king of what type document we want

error
----
- 12632064:error:10000438:SSL routines:OPENSSL_internal:TLSV1_ALERT_INTERNAL_ERROR:..\..\third_party\boringssl\src\ssl\tls_record.cc:592:SSL alert number 80
 --> solve using add ip address
 - bson.errors.InvalidDocument: cannot encode object: datetime.date(2000, 7, 20), of type: <class 'datetime.date'>

data modeling( relationships and embeded) 
- When we have one - to - one relationships is totaly fine to store as embedeed inside store
- with multiple relationships we can store seprate coollection, if we chnge so we havent change in wvery documents

### subset
----
it can be time consuming if we are grabing  every single document for a specific document

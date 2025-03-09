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

# import pymongo
# client = pymongo.MongoClient()

# db = client['pythondb'] # pythondb is db name

# empCollection = db.employees # Collection name

# document = {
#     'Eno': 100,
#     'Ename': 'ASHISH',
#     'ESAL': 10000000,
#     'eaddr': "Punjab"
# }

# empCollection.insert_one(document)

# print('Document Inserted Successfully!!!')
# client.close()

import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

document = empCollection.find_one() 
print(type(document)) # dict
print(document)

print(document.get('Eno'))

client.close()
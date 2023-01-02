import pymongo

client = pymongo.MongoClient()
db_list = client.list_database_names()
db = client['pytest']

# collection name
empCollection = db.employees
document = {'ENO':101,'ENAME':'Bindra','ESAL':10000}
print(document)	
empCollection.insert_one(document)
print("successfully inserted")
client.close()

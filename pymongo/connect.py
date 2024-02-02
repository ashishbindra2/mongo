import pymongo

client = pymongo.MongoClient()
print(client)

# print(client.__dict__)
db_list = client.list_database_names()
#print(db_list)

#for db in db_list:
#	print(db)

# create dbname
db = client['pytest']
print(db)

# collection name
empCollection = db.employees
print(empCollection)

client.close()




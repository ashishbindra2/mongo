import pymongo

client = pymongo.MongoClient()
db_list = client.list_database_names()
db = client['pytest']

# collection name
empCollection = db.employees
emplist = [

{'ENO':103,'ENAME':'SUNNY','ESAL':12000},
{'ENO':104,'ENAME':'BUNNY','ESAL':13000},
{'ENO':105,'ENAME':'Pinny','ESAL':14000},
{'ENO':106,'ENAME':'Binny','ESAL':15000},
{'ENO':107,'ENAME':'MAAJID','ESAL':160000},
]
print(emplist)	
empCollection.insert_many(emplist)
print("all results successfully inserted")
client.close()
print(f'{len(emplist)}')

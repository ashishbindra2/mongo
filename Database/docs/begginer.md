# random

## connection
```py
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
```

## display
```py
import pymongo

client = pymongo.MongoClient()
db = client['pytest']
empColl = db.employees

document = empColl.find_one()
print(document.get('ENO'))
print(document.get('ENAME'))

empcourser = empColl.find()

for doca in empcourser:
	print(doca)

empcourser = empColl.find()

print('*'*100)
print()
print('ID\tNAME\tSALARY')
for doc in empcourser:
#	print(type(doc))
	print(f"{doc.get('ENO')}\t{doc.get('ENAME')}\t{doc.get('ESAL')}")
print()
print('*'*100)
client.close()
```

## dynamic input
```py
import pymongo

client = pymongo.MongoClient()
db_list = client.list_database_names()
db = client['pytest']

# collection name
empCollection = db.employees

while True:
	eno = int(input('Emp number!!! '))
	ename = input('Emp name.. ')
	esal = float(input('Enter Emp salary.. '))
	document = {'ENO':eno,'ENAME':ename,'ESAL':esal}
	empCollection.insert_one(document)
	print(document)	
	option = input(' yes |	no ').lower()
	while option not in ('yes','y','n','no'):
		option = input(' Invalid option [y|n]')
		print()
	if option in ('no','n'):
		break
	
	
print("Successfully inserted!!! ")
client.close()
```

## insert
```py
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
```

## insert many
```py
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
```
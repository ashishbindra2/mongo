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
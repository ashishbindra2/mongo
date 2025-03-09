# pymongo

* MongoDB shell acts as a client to perform our required database operations.
* MongoDB shell is JavaScript based- special applications to communicates with MongoDb server
* From Python Program to communicate with mongoDB database some special software must be required, which is nothing but Driver software i.e by using Driver Software Python program can communicated with MongoDB Database
* Python Driver Software is: Python Library


- To implement mongo this website is good  https://mongoplayground.net/
- To delete all the records db.collectionname.deleteMany()

pip => Package manager in Python

By default pymango is not available, we have to install separatly by using commands

## How to install pymongo
`pip install pymongo`


## Important steps in python to MongoDB communication
------------------------------------------------------
1. Import pymango module in our python program

    `import pymongo`
    or
    `from pymongo import *`

2. Create client to communicate with mongoDB Server
    1. `client = pymongo.MongoClient()`  
    2. `client = pymongo.MongoClient('localhost',27017)` IP => localhost, PORT => 27017
    3. `client = pymongo.MongoClient()`  

3. Create/Connect with databse

    `empDB = Client['employeeDB]`

4. Create/Connect with collection
    `empCollection = empDB.employees`

5. By using collection object we can perform required databse operations.

    * To insert Documents : <br>
        `empCollection.insert_one({})` => Highly Recommended
        `empCollection.insert_many()`<br>
        `empCollection.insert()` => debrecated
    
    - To find Documents :<br>
        `empCollection.find_one()`<br>
        `empCollection.find()`

    - To Update Documents :<br>
        `empCollection.update_one()`<br> ->recommended
        `empCollection.update_many()`<br>
        `empCollection.update()`<br>

    - To delete Document:<br>
        `empCollection.delete_one()`<br>
        `empCollection.delete_many()`<br>
        `empCollection.delete()`<br>
    
    - Close Client => Highly Recommended<br>
        `client_close()`

        

* If we getting this error while retriving `_id` use `str()` function to type cast

### To perform schema validation first we need to 
- edit set admin to builtin role in mongo db atlas in database access clink
- then we have to set `&authSource=admin"` at the end of connections string

`db.dropdatabase()`

```py title="eg-1"
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

document = {
    'Eno': 100,
    'Ename': 'ASHISH',
    'ESAL': 10000000,
    'eaddr': "Punjab"
}

empCollection.insert_one(document)

print('Document Inserted Successfully!!!')
client.close()
```

```py tittle="eg-2"
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

document = empCollection.find_one() 
print(type(document)) # dict
print(document)

print(document.get('Eno'))

client.close()
```

## Write a python scrpt to connnect with MongoDB and display all available databases?
```py
# we have o use clicent.list_database_names() method
import pymongo

client = pymongo.MongoClient()
db_list = client.list_database_names()

print('The Available Database are ')
print('#'*40)

for db in db_list:
    print(db)

client.close()

# output
The Available Database are 
########################################
# My_Database
# admin
# chatflowdb
# config
# job_recom_db
# local
```

## WAP to create a database named woth python and in that database create a collection named with employees and insert on document?

```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

document = {
    'Eno': 100,
    'Ename': 'ASHISH',
    'ESAL': 10000000,
    'eaddr': "Punjab"
}

empCollection.insert_one(document)

print('Document Inserted Successfully!!!')
client.close()

# Document Inserted Successfully!!!

```

## To insert multiple  documents :
```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

emplist =[
    {
    'Eno': 101,
    'Ename': 'sonu',
    'ESAL': 10000000,
    'eaddr': "up"
    },  {
    'Eno': 102,
    'Ename': 'krishna',
    'ESAL': 50000000,
    'eaddr': "delhi"
    },  {
    'Eno': 103,
    'Ename': 'vivek',
    'ESAL': 99000,
    'eaddr': "mp"
    },  {
    'Eno': 104,
    'Ename': 'duby',
    'ESAL': 800000,
    'eaddr': "j&k"
    },
]

empCollection.insert_many(emplist)

print('All Documents Inserted Successfully!!!')
client.close()
print(f'{len(emplist)}')

# output
# All Documents Inserted Successfully!!!
# 4
```

## Read Dynamic Data from the end user & inserted into database
> db.employees.deleteMany({}) => delete all data

```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

while True:
    Eno = int(input("Enter eno "))
    Ename = input("enter ename ")   
    ESAL = float(input("enter esalary "))    
    eaddr = input("enter address ")  
     
    document = {
        'Eno': Eno,
        'Ename': Ename,
        'ESAL': ESAL,
        'eaddr': eaddr
        }
    
    empCollection.insert_one(document)
    print('Document Inserted Successfully!!!')
    
    option = input("Do you want to insert more ").lower()
    
    while option not in ('y','yes','n','no') :
        option = input("Invalid Option, [yes/no] ").lower()

    if option in ('no','n'):
        break

print("Thanks")
    
client.close()

# output
# Rnter eno 106
# enter ename aa
# enter esalary 21321
# enter address asdsa
# Document Inserted Successfully!!!
# Do you want to insert moreno
# Thanks
```
***Note:***  
> insert() method is deprecated and hence it is not recommened to use instead. We can use inset_one() or insert_many() methods.

 ##  Find Operation:
 1. find_one()
 2. find()
 
 -----
 1. find_one()
      - return python dict object
      - to find only one matched document
 
 2. find()
      - all match documents to find
      - it return cursor object

## 5. To find only one document
```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

document = empCollection.find_one() 
print(type(document)) # dict

print(document.get('Eno'))

client.close()
```

## To find multiple documents
- WAP to display all documents from employees collections
- here we have to use find() method.

```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

empcursor = empCollection.find() 
print(type(empcursor)) 

for document in empcursor:
    print(type(document))
    print(f"{document.get('Eno')}")
client.close()

# output
# <class 'pymongo.cursor.Cursor'>
# <class 'dict'>
# 100
# <class 'dict'>
# 101
# <class 'dict'>
# 102
# <class 'dict'>
# 103
# <class 'dict'>
# 104
# <class 'dict'>
# 100
```

## To find all employees whose salary is grater than 1500
> shell => db.employee.find({'esal':{$gt:1500}})
> python => empcollection.find({'Esal':{'$gt' 1500}})

```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

empcursor = empCollection.find({'ESAL': {'$gt': 99000}}) #'' is required

print("*"*33)
for document in empcursor:
    print(f"{document.get('ESAL')}")

client.close()

# output
# *********************************
# 10000000
# 10000000
# 50000000
# 800000
# 10000000
```

## 8 To find employees information based on descending order of salary?

> shell : db.employees.find().sort({'ESAL': -1})

> python : empCollection.find().sort('ESAL', -1)
- sort => take 2 arguments second one is dicrection  
```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

empcursor = empCollection.find().sort('ESAL',-1)

print("*"*33)
for document in empcursor:
    print(f"{document.get('Eno')} {document.get('Ename')} {document.get('ESAL')} {document.get('eaddr')}")

# client.close()
# *********************************
# 102 krishna 50000000 delhi
# 100 ASHISH 10000000 Punjab
# 101 sonu 10000000 up
# 100 ASHISH 10000000 Punjab
# 104 duby 800000 j&k
# 103 vivek 99000 mp
```

## 9. To display 3 employee information who are having least salary

>  shell : db.employee.find().sort({'ESAL': 1}).limit(3)
> python : empCollection.find().sort('ESAL', 1).limit(3)

```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

empcursor = empCollection.find().sort('ESAL',1).limit(3)

print("*"*33)
for document in empcursor:
    print(f"{document.get('Eno')} {document.get('Ename')} {document.get('ESAL')} {document.get('eaddr')}")

client.close()

# *********************************
# 103 vivek 99000 mp
# 104 duby 800000 j&k
# 100 ASHISH 10000000 Punjab
```
## 10. Display employee info based on given emp name ?
document = empCollection.findOne({"Ename": name})

```py
import pymongo
client = pymongo.MongoClient()

db = client['pythondb'] # pythondb is db name

empCollection = db.employees # Collection name

document = empCollection.find_one({"Ename": "ASHISH"})
if document:
    print(f"{document.get('Eno')} {document.get('Ename')} {document.get('ESAL')} {document.get('eaddr')}")
else:
    print("element not find")
client.close()

# output
# 100 ASHISH 10000000 Punjab
```


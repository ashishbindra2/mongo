- To implement mongo this website is good  https://mongoplayground.net/
- To delete all the records db.collectionname.deleteMany()

pip => Package manager in Python

By default pymango is not available, we have to install separatly by using commands

### How to install pymongo
`pip install pymongo`

### Important steps in python to MongoDB communication
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

To perform schema validation first we need to 
- edit set admin to builtin role in mongo db atlas in database access clink
- then we have to set `&authSource=admin"` at the end of connections string

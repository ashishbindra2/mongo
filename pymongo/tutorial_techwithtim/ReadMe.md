- first install pymongo `pip install pymongo[srv]`
- `pip install python-dotenv` 

No sql database like mongodb actually stores unstructured data and typically in json format
- Abiltiy to perform frequent changes to struce of the data
- Highly Flexible ()
- Faster quiery 
- saclable

document model
-------------
database -> collections -> documents

Bson type satore

find({})
-----
allow to insert a query object which is different properties that we are tyring to match when we are looking for elemnt or document.
-if we live empty it just find all document in collection
----
a curser is sothing that we can iterate over

oprator
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

schema validation
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

subset
----
it can be time consuming if we are grabing  every single document for a specific document

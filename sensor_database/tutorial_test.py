#first mongod and run python 3

import pymongo
import sys

def main():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]

    mydict = { "_id":1, "name": "John", "address": "Highway 37" }
    x = mycol.insert_one(mydict)
    print("ID of first customer: ", end = ' ')
    print(x.inserted_id)
    print()
    print("Checking for all collections:")
    print(mydb.list_collection_names())
    print()
    print("Checking for all databases:")
    print(myclient.list_database_names())
    print()

    mylist = [
        { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
        { "_id": 3, "name": "Amy", "address": "Apple st 652"},
        { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
        { "_id": 5, "name": "Michael", "address": "Valley 345"},
        { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
        { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
        { "_id": 8, "name": "Richard", "address": "Sky st 331"},
        { "_id": 9, "name": "Susan", "address": "One way 98"},
        { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
        { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
        { "_id": 12, "name": "William", "address": "Central st 954"},
        { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
        { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
    ]

    x = mycol.insert_many(mylist)
    #print("ID of last customer:", end = " ") figure out later
    #x = mycol.distinct("_id", {}).sort("_id", -1).limit(1)
    #print(x[0])
    
    myquery = { "address": "Park Lane 38" }
    mydoc = mycol.find(myquery)
    print("Customer with the address Park Lane 38:")
    for x in mydoc:
        print(x)
    print()

    print("Customers with addresses that start with 'S' or higher:")
    myquery = { "address": { "$gt": "S" } }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)
    print()

    print("Customers whose address starts with 's':")
    myquery = { "address": { "$regex": "^S" } }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)
    print()

    print("All customers in alphabetical order:")
    mydoc = mycol.find().sort("name")
    for x in mydoc:
        print(x)
    print()

    myquery = {"address": "Mountain 21"}
    print("The name of the customer we will be deleting is ", end = '')
    mydoc = mycol.find_one(myquery, {"_id":0,"name":1} )
    print(mydoc)
    mycol.delete_one(myquery)
    print()

    # to delete all docs in a collection, use mycol.delete_many({})
    # to delete a collection, mycol.drop()

    myquery = {"address": "Valley 345" }
    newvalues = { "$set": {"address": "Canyon 123" } }
    print("Updating the address of ", end = '')
    mydoc = mycol.find_one(myquery, {"_id":0, "name":1})
    print(mydoc)
    mycol.update_one(myquery, newvalues)
    print()

    print("List of all customer information: ")
    for x in mycol.find():
        print(x)
    
     
    return

if __name__ == '__main__':
    main()





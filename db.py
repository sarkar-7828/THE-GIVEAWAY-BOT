from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import mongo_uri,db_name

# Create a new client and connect to the server
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client[db_name]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


async def create_db_if_not_exists():
    try:
        db.create_collection("coupons")
        print("Collection created successfully!")
    except Exception as e:
        print(e)


async def add_coupon(coupon):
    try:
        collection = db.coupons
        result =  collection.insert_one(coupon)
        print(f"Coupon added with ID: {result.inserted_id}")
    except Exception as e:
        print(e)

async def fetch_latest_coupon():
    try:
        collection =  db.coupons
        # get all coupons which are not redeemed and sort by _id in descending order
        latest_coupon = collection.find_one({"redeemed": False})
        return latest_coupon
    except Exception as e:
        print(e)

async def fetch_coupon_count():
    try:
        # fetch all coupons grouped by redeemed status and count them like {redeemed: 1, unredeemed:10}
        collection = db.coupons
        pipeline = [
            {
                "$group": {
                    "_id": "$redeemed",
                    "count": {"$sum": 1}
                }
            }
        ]
        result = collection.aggregate(pipeline)

        output = {True: 0, False: 0}
        for doc in result:
            output[doc["_id"]] = doc["count"]

        formatted_output = {
            "redeemed": output.get(True, 0),
            "unredeemed": output.get(False, 0)
        }
        return formatted_output
    except Exception as e:
        print(e)

async def update_coupon(coupon, redeemed):
    coupon_id = coupon["_id"]
    try:
        collection = db.coupons
        result = collection.update_one({"_id": coupon_id}, {"$set": {"redeemed": redeemed}})
        print(f"Coupon updated with ID: {coupon_id}")
    except Exception as e:
        print(e)
        
async def clear_all_redeemed_coupons():
    try:
        collection = db.coupons
        result = collection.delete_many({"redeemed": True})
        print(f"Redeemed coupons cleared: {result.deleted_count}")
    except Exception as e:
        print(e)

async def clear_all_unredeemed_coupons():
    try:
        collection = db.coupons
        result = collection.delete_many({"redeemed": False})
        print(f"Unredeemed coupons cleared: {result.deleted_count}")
    except Exception as e:
        print(e)
        
async def clear_all_coupons():
    try:
        collection = db.coupons
        result = collection.delete_many({})
        print(f"Coupons cleared: {result.deleted_count}")
    except Exception as e:
        print(e)
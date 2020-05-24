import pymongo


client = pymongo.MongoClient(
    "mongodb://agile-sensing-analytics:w77pebv6@ds035995.mlab.com:35995/heroku_vgcclk7m?retryWrites=false")

db = client.imagedata
db.command("createUser", "admin", pwd="password", roles=["root"])
""" data = db.data

testDocument = {
    "url": "https://makerspacequb.github.io/images/QLab.png",
    "points": "{\"name\":\"polyline\",\"all_points_x\":[537,625,649,539],\"all_points_y\":[641,778,652,640]}",
    "anotherRow": "test"
}
data.insert_one(testDocument) """

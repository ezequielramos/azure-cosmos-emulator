import base64
import azure.cosmos.cosmos_client as cosmos_client

DATABASE = "database_name"
COLLECTION = "collection_name"
URL_CONNECTION = "http://localhost:8081/"
MASTER_KEY = base64.b64encode(b"dummy_password")

collection_link = f"dbs/{DATABASE}/colls/{COLLECTION}"

client = cosmos_client.CosmosClient(
    url_connection=URL_CONNECTION, auth={"masterKey": MASTER_KEY}
)

document = {"column1": "value1", "column2": "value2"}

client.CreateItem(database_or_Container_link=collection_link, document=document)
client.CreateItem(database_or_Container_link=collection_link, document=document)
client.CreateItem(database_or_Container_link=collection_link, document=document)
client.CreateItem(database_or_Container_link=collection_link, document=document)
client.CreateItem(database_or_Container_link=collection_link, document=document)
client.CreateItem(database_or_Container_link=collection_link, document=document)

query = {"query": "SELECT * FROM collection"}

result = client.QueryItems(
    collection_link, query, options={"enableCrossPartitionQuery": True}
)

result = list(result)

for item in result:
    options = {"partitionKey": item["column1"]}
    client.DeleteItem(f"{collection_link}/docs/{item['id']}", options)

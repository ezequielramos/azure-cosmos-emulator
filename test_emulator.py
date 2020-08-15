import base64
import unittest

import azure.cosmos.cosmos_client as cosmos_client

DATABASE = "database_name"
COLLECTION = "collection_name"
URL_CONNECTION = "http://localhost:8081/"
MASTER_KEY = base64.b64encode(b"dummy_password")

client = cosmos_client.CosmosClient(
    url_connection=URL_CONNECTION, auth={"masterKey": MASTER_KEY}
)


class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.collection_link = f"dbs/{DATABASE}/colls/{COLLECTION}"

    def test_basic_operations(self):

        document = {"column1": "value1", "column2": "value2"}

        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )
        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )
        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )
        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )
        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )
        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )

        query = {"query": "SELECT * FROM collection"}

        result = client.QueryItems(
            self.collection_link, query, options={"enableCrossPartitionQuery": True}
        )

        result = list(result)

        self.assertEqual(len(result), 6)

        for item in result:
            options = {"partitionKey": item["column1"]}
            client.DeleteItem(f"{self.collection_link}/docs/{item['id']}", options)

    def test_simple_array_contains(self):
        client = cosmos_client.CosmosClient(
            url_connection=URL_CONNECTION, auth={"masterKey": MASTER_KEY}
        )

        document = {"column1": "value1", "column2": "value2"}

        client.CreateItem(
            database_or_Container_link=self.collection_link, document=document
        )

        query = {
            "query": "SELECT * FROM collection WHERE ARRAY_CONTAINS(@column1, collection.column1)"
        }

        parameters = [{"name": "@column1", "value": ["value1"]}]

        result = client.QueryItems(
            self.collection_link,
            query=dict(query=query, parameters=parameters),
            options={"enableCrossPartitionQuery": True},
        )

        result = list(result)

        self.assertEqual(len(result), 1)
        parameters = [{"name": "@column1", "value": ["another_value"]}]

        result = client.QueryItems(
            self.collection_link,
            query=dict(query=query, parameters=parameters),
            options={"enableCrossPartitionQuery": True},
        )

        result = list(result)

        self.assertEqual(len(result), 0)

    def tearDown(self):
        query = {"query": "SELECT * FROM collection"}

        result = client.QueryItems(
            self.collection_link, query, options={"enableCrossPartitionQuery": True}
        )

        for item in result:
            options = {"partitionKey": item["column1"]}
            client.DeleteItem(f"{self.collection_link}/docs/{item['id']}", options)

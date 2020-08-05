import json
import time
import uuid

from flask import Flask, request, Response

app = Flask(__name__)

items = {}


@app.route("/")
def index():
    return_value = {
        "_self": "",
        "id": "localhost",
        "_rid": "localhost",
        "media": "//media/",
        "addresses": "//addresses/",
        "_dbs": "//dbs/",
        "writableLocations": [
            {"name": "East US 2", "databaseAccountEndpoint": "http://localhost:8081"}
        ],
        "readableLocations": [
            {"name": "East US 2", "databaseAccountEndpoint": "http://localhost:8081"}
        ],
        "enableMultipleWriteLocations": False,
        "userReplicationPolicy": {
            "asyncReplication": False,
            "minReplicaSetSize": 3,
            "maxReplicasetSize": 4,
        },
        "userConsistencyPolicy": {"defaultConsistencyLevel": "Session"},
        "systemReplicationPolicy": {"minReplicaSetSize": 3, "maxReplicasetSize": 4},
        "readPolicy": {"primaryReadCoefficient": 1, "secondaryReadCoefficient": 1},
        "queryEngineConfiguration": '{"maxSqlQueryInputLength":262144,"maxJoinsPerSqlQuery":5,"maxLogicalAndPerSqlQuery":500,"maxLogicalOrPerSqlQuery":500,"maxUdfRefPerSqlQuery":10,"maxInExpressionItemsCount":16000,"queryMaxInMemorySortDocumentCount":500,"maxQueryRequestTimeoutFraction":0.9,"sqlAllowNonFiniteNumbers":false,"sqlAllowAggregateFunctions":true,"sqlAllowSubQuery":true,"sqlAllowScalarSubQuery":true,"allowNewKeywords":true,"sqlAllowLike":false,"sqlAllowGroupByClause":true,"maxSpatialQueryCells":12,"spatialMaxGeometryPointCount":256,"sqlDisableQueryILOptimization":false,"sqlAllowTop":true,"enableSpatialIndexing":true}',
    }
    return Response(
        json.dumps(return_value), status=200, content_type="application/json"
    )


def query(database_name, collection_name, query):
    print(query)
    return {
        "_rid": collection_name,
        "Documents": items[database_name][collection_name],
        "_count": len(items[database_name][collection_name]),
    }


def insert_item(database_name, collection_name, item):
    global items

    print(database_name, collection_name, item)

    if database_name not in items:
        items[database_name] = {}

    database = items[database_name]

    if collection_name not in database:
        database[collection_name] = []

    item["_rid"] = item["id"]
    item["_self"] = f"dbs/{database_name}/colls/{collection_name}/docs/{item['id']}/"
    item["_etag"] = f'"{str(uuid.uuid4())}"'
    item["_attachments"] = "attachments/"
    item["_ts"] = int(time.time())

    database[collection_name].append(item)

    print(items)


@app.route("/dbs/<database_name>/colls/<collection_name>/docs/", methods=["POST"])
def docs_post(database_name, collection_name):
    payload = request.get_json()

    if "query" in payload:
        print("It's a query")

        return Response(
            json.dumps(query(database_name, collection_name, payload["query"])),
            200,
            content_type="application/json",
        )
    elif "id" in payload:
        print("It's an insert")
        insert_item(database_name, collection_name, payload)
        return Response("", 200, content_type="application/json")
    else:
        print("I don't know what is it.", payload)
        return Response("", 200, content_type="application/json")


@app.route(
    "/dbs/<database_name>/colls/<collection_name>/docs/<item_id>/", methods=["DELETE"]
)
def delete(database_name, collection_name, item_id):
    payload = request.get_data()

    i = 0

    while len(items[database_name][collection_name]) > i:

        if items[database_name][collection_name][i]["id"] == item_id:
            items[database_name][collection_name].pop(i)
        else:
            i += 1

    return Response("", 200, content_type="application/json")


@app.route("/dbs/<database_name>/colls/<collection_name>/", methods=["GET"])
def get_db_coll_info(database_name, collection_name):
    return_value = {
        "id": "localhost",
        "indexingPolicy": {
            "indexingMode": "consistent",
            "automatic": True,
            "includedPaths": [{"path": "/*"}],
            "excludedPaths": [{"path": '/"_etag"/?'}],
        },
        "partitionKey": {"paths": ["/partitionKeyField"], "kind": "Hash"},
        "conflictResolutionPolicy": {
            "mode": "LastWriterWins",
            "conflictResolutionPath": "/_ts",
            "conflictResolutionProcedure": "",
        },
        "geospatialConfig": {"type": "Geography"},
        "_rid": collection_name,
        "_ts": 1584730007,
        "_self": f"dbs/{database_name}/colls/{collection_name}/",
        "_etag": f'"{str(uuid.uuid4())}"',
        "_docs": "docs/",
        "_sprocs": "sprocs/",
        "_triggers": "triggers/",
        "_udfs": "udfs/",
        "_conflicts": "conflicts/",
    }
    return Response(json.dumps(return_value), 200, content_type="application/json")


app.run(host="0.0.0.0", port=8081)

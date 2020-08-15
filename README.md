# azure-cosmos-emulator

<img src="https://img.shields.io/badge/python-3.7.5-blue"> <img src="https://img.shields.io/github/license/digital-divas/PINP"> ![Python application](https://github.com/ezequielramos/azure-cosmos-emulator/workflows/Python%20application/badge.svg)

azure-cosmos-emulator is a mock to the Azure Cosmos Database using Flask. You can use it to test your application that integrates with CosmosDB.

azure-cosmos-emulator is available on dockerhub. To run it, just execute:

```bash
docker run -d -p 8081:8081 ezequielmr94/azure-cosmos-emulator:latest
```

You can set the environment variable to use SSL.

```bash
docker run -d -p 8081:8081 -e AZURE_EMULATOR_USING_SSL=True ezequielmr94/azure-cosmos-emulator:latest
```

## Common Issues:

- Using the node.js sdk you need to use SSL. You need to disable certificate verification using `process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";`.

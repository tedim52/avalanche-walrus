# avalanche-gossip-research
CS 6410 Project

## Starting a Cluster via cURL
### Requires
1. avalanche-network-runner
1. An avalanchego node executable
1. cURL

### Start the Server
In one terminal run
```
avalanche-network-runner server \
    --log-level debug \
    --port=":8080" \
    --grpc-gateway-port=":8081"
```

### Start the Cluster
In a separate terminal,
1. Set the the path to an avalanchego node executable to the environment variable AVANODE
1. Run `scripts/start_cluster.sh`
This will start up a 5 node cluster using the executable specified.

### Check the Status of the Cluster
In the server terminal, you should see each of the nodes spinning up (each will have a different color).
Run `scripts/get_status.sh` until the "healthy" attribute of the JSON response is true.

### Fund the Network
Run `scripts/fund_network.sh`. Follow the steps in the relevant section of the [Avalanche docs](https://docs.avax.network/quickstart/fund-a-local-test-network) to complete the integration with MetaMask.

## Attaching the ethclient
Compile and run the go module in `ethclient`. Attaches to the node at localhost:9650 and subscribes to new accepted transactions and gets the time first seen.

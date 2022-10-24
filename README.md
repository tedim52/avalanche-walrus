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

### Cluster Configuration
To specify the nodes in the cluster, write a config file with each node executable and number of nodes on separate lines. For example, the following specifies a network with 5 default avalanchego nodes and 6 modified nodes
```
5 /home/qburke/avalanchego/build/avalanchego
3 /home/qburke/walrus/build/nodev1
```

### Starting the Cluster
In a separate terminal run the testbed module passing the filename as the first argument
This will 
1. Start a cluster with the given configuration
1. Fund the network
1. Attach ethclients to each node which will output to the terminal.

### Resetting MetaMask Account
For first time setup, follow the steps in the relevant section of the [Avalanche docs](https://docs.avax.network/quickstart/fund-a-local-test-network) to complete the integration with MetaMask.<br>
For subsequent tests, go to Account Settings > Advanced and Reset Account for the funded account.

## tx-spammer

This code spams transactions to the local network of avalanche node created by the `testbed` module. To start spamming transactions, run the following commands in the `tx-spammer` directory after starting a local avalanche network and running the `testbed` binary (see readme here[https://github.com/tedim52/avalanche-walrus#readme]):

```
go build
./tx-spammer --cluster-info-yaml=.simulator/config.yml
```

This code was adapted from avalanchego/subnet-evm/cmd/simulator[https://github.com/ava-labs/subnet-evm/tree/master/cmd/simulator].
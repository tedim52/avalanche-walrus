## tx-spammer

This code spams transactions to the local network of avalanche node created by the `testbed` module. To start spamming transactions, run the following commands after starting a local avalanche network and running the `testbed` binary (see readme [here](https://github.com/tedim52/avalanche-walrus#readme)):

```
cd tx-spammer/
go build
./tx-spammer --cluster-info-yaml=.simulator/config.yml
```

The output should look like the following:

```
2022/10/31 16:22:22 launching spammer with rpc endpoints [] or cluster info yaml ".simulator/config.yml", timeout 1m0s, concurrentcy 10, base fee 25, priority fee 1
2022/10/31 16:22:22 loading cluster info yaml ".simulator/config.yml"
[http://127.0.0.1:9650/ext/bc/C/rpc http://127.0.0.1:9652/ext/bc/C/rpc http://127.0.0.1:9654/ext/bc/C/rpc http://127.0.0.1:9658/ext/bc/C/rpc http://127.0.0.1:9656/ext/bc/C/rpc]
2022/05/11 09:49:22 loaded worker 0x8db97C7cEcE249c2b98bDC0226Cc4C2A57BF52FC (balance=100000000000000000000000000 nonce=0)
2022/05/11 09:49:22 0xe8859AF6c05b512dF80A66b81dE89FDAB9fE5C1c requesting funds from master
2022/05/11 09:49:22 0xa2B32bcbA31d4dC7728aD73165cdeea5eCeD5e70 requesting funds from master
2022/05/11 09:49:22 0x837438175627A7A2ABbccf1727c5cA46fA7274b5 requesting funds from master
2022/05/11 09:49:22 0x14c908A82047C6bC66cd9282b4D68f3e003659f8 requesting funds from master
2022/05/11 09:49:22 0xbeE6DF853592d3699ac3292D134F59BEF278B048 requesting funds from master
2022/05/11 09:49:22 0x028Bc164dcC1c10f1Db5a1175c58eA84a7Fd34c9 requesting funds from master
2022/05/11 09:49:22 0x664D97348Bdb73fc3bC4447B4676573dbF6eEE5A requesting funds from master
2022/05/11 09:49:22 0x455aAB371261DC41a048e42Bf147ced4FaDE5fCF requesting funds from master
2022/05/11 09:49:22 0xA9b5C64E057F50730CA4Ba6205d55fa08C03ff75 requesting funds from master
2022/05/11 09:49:22 0x57645A2bdCEb6cFbC95e6a5Cac70F0c05B8d8515 requesting funds from master
2022/05/11 09:49:24 [block created] t: 2022-05-11 09:49:22 -0600 MDT index: 1 base fee: 1 block gas cost: 0 block txs: 1 gas used: 21000
2022/05/11 09:49:24 [block created] t: 2022-05-11 09:49:24 -0600 MDT index: 2 base fee: 1 block gas cost: 0 block txs: 1 gas used: 21000
2022/05/11 09:49:24 [stats] historical TPS: 1.00 last 10s TPS: 0.10 total txs: 2 historical GPS: 21000.0, last 10s GPS: 2100.0 elapsed: 2s
2022/05/11 09:49:26 [block created] t: 2022-05-11 09:49:26 -0600 MDT index: 3 base fee: 1 block gas cost: 0 block txs: 1 gas used: 21000
2022/05/11 09:49:26 [stats] historical TPS: 0.75 last 10s TPS: 0.20 total txs: 3 historical GPS: 15750.0, last 10s GPS: 4200.0 elapsed: 4s
2022/05/11 09:49:28 [block created] t: 2022-05-11 09:49:28 -0600 MDT index: 4 base fee: 1 block gas cost: 0 block txs: 2 gas used: 42000
2022/05/11 09:49:28 [stats] historical TPS: 0.83 last 10s TPS: 0.30 total txs: 5 historical GPS: 17500.0, last 10s GPS: 6300.0 elapsed: 6s
2022/05/11 09:49:30 [block created] t: 2022-05-11 09:49:30 -0600 MDT index: 5 base fee: 1 block gas cost: 0 block txs: 4 gas used: 84000
2022/05/11 09:49:30 [stats] historical TPS: 1.12 last 10s TPS: 0.50 total txs: 9 historical GPS: 23625.0, last 10s GPS: 10500.0 elapsed: 8s
```

This code was adapted from [avalanchego/subnet-evm/cmd/simulator](https://github.com/ava-labs/subnet-evm/tree/master/cmd/simulator).

TODO: add functionality to spam pregenerated transaction workloads.
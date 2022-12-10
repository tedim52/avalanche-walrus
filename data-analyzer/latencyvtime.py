import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import sys

'''
Creates a graph comparing transaction latency and gas used / TPS
Expects two types of CSV with headers:
1. Hash,Start,End,NodeID,Blockhash
2. Blockhash,GasUsed,TPS
And 6 CSV files. Each pair of CSV files has one file of each type above.
The pairs correspond to the experiments as follows:
1. control
2. proposer
3. scorer
So calling the script should look like this:
python3 latencyvtime.py control-txs.csv control-meta.csv proposer-txs.csv proposer-meta.csv scorer-txs.csv scorer-meta.csv
'''

def bhashes_from_interval(key, interval, df):
    l = []
    df.sort_values(key)
    max_val = df[key].iat[-1]
    upper = interval
    bucket = []
    for idx in df.index:
        while df[key][idx] > upper:
            # New interval: append old, move window and new bucket
            l.append(bucket)
            upper += interval
            bucket = []
        bucket.append(df[key])
    return l

def avg_latencies(bhashes, df_txs):
    avg_latency = [0] * len(bhashes)
    tx_count = [0] * len(bhashes)
    # flatten into lookup table
    bhash_to_interval = {}
    for i, b in bhashes:
        for h in b:
            bhash_to_interval[h] = i
    # iterate through txs and sum
    for idx in df_txs.index:
        interval_idx = bhash_to_interval[df_txs['BlockHash'][idx]]
        latency = df_idx['End'][idx] - df_idx['Start'][idx]
        avg_latency[interval_idx] += latency
        tx_count[interval_idx] += 1
    # Take average
    for i in range(len(avg_latency)):
        if tx_count[i] > 0:
            avg_latency[i] /= tx_count[i]
    return avg_latency

def main():
    if len(sys.argv) != 7:
        print("Usage: python3 latencyvtime.py control-txs.csv control-meta.csv proposer-txs.csv proposer-meta.csv scorer-txs.csv scorer-meta.csv")
        exit(1)
    
    # Assumes csv well formatted
    ctrl_txs = pd.read_csv(sys.argv[1])
    ctrl_meta = pd.read_csv(sys.argv[2])
    prop_txs = pd.read_csv(sys.argv[3])
    prop_meta = pd.read_csv(sys.argv[4])
    scor_txs = pd.read_csv(sys.argv[5])
    scor_meta = pd.read_csv(sys.argv[6])

    # Create gas used and tps ranges
    gu_interval_size = 100000
    tps_interval_size = 10
    # Create list of blockhashes for each range
    ctrl_gu_bhashes = bhashes_from_interval('GasUsed', gu_interval_size, ctrl_meta)
    ctrl_tps_bhashes = bhashes_from_interval('TPS', tps_interval_size, ctrl_meta)
    prop_gu_bhashes = bhashes_from_interval('GasUsed', gu_interval_size, prop_meta)
    prop_tps_bhashes = bhashes_from_interval('TPS', tps_interval_size, prop_meta)
    scor_gu_bhashes = bhashes_from_interval('GasUsed', gu_interval_size, scor_meta)
    scor_tps_bhashes = bhashes_from_interval('TPS', tps_interval_size, scor_meta)

    # Average latency for all txhashes corresponding to blocks
    ctrl_gu_y = avg_latencies(ctrl_gu_bhashes, ctrl_txs)
    ctrl_tps_y = avg_latencies(ctrl_tps_bhashes, ctrl_txs)
    prop_gu_y = avg_latencies(prop_gu_bhashes, prop_txs)
    prop_tps_y = avg_latencies(prop_tps_bhashes, prop_txs)
    scor_gu_y = avg_latencies(scor_gu_bhashes, scor_txs)
    scor_tps_y = avg_latencies(scor_tps_bhashes, scor_txs)

    # Create x-axes
    ctrl_gu_x = list(range(gu_interval_size, gu_interval_size*(len(ctrl_gu_bhashes)+1), gu_interval_size))
    ctrl_tps_x = list(range(gu_interval_size, gu_interval_size*(len(ctrl_tps_bhashes)+1), gu_interval_size))
    prop_gu_x = list(range(gu_interval_size, gu_interval_size*(len(prop_gu_bhashes)+1), gu_interval_size))
    prop_tps_x = list(range(gu_interval_size, gu_interval_size*(len(prop_tps_bhashes)+1), gu_interval_size))
    scor_gu_x = list(range(gu_interval_size, gu_interval_size*(len(scor_gu_bhashes)+1), gu_interval_size))
    scor_tps_x = list(range(gu_interval_size, gu_interval_size*(len(scor_tps_bhashes)+1), gu_interval_size))

    plt.plot(ctrl_gu_x, ctrl_gu_y, label='Control')
    plt.plot(prop_gu_x, prop_gu_y, label='Proposer Gossip')
    plt.plot(scor_gu_x, scor_gu_y, label='Tx Scoring')

    plt.title("Tx Latency vs Gas Used for Different Implementations")
    plt.xlabel("Gas Used")
    plt.ylabel("Avg Tx RTT")
    plt.show()

    plt.plot(ctrl_tps_x, ctrl_tps_y, label='Control')
    plt.plot(prop_tps_x, prop_tps_y, label='Proposer Gossip')
    plt.plot(scor_tps_x, scor_tps_y, label='Tx Scoring')

    plt.title("Tx Latency vs TPS for Different Implementations")
    plt.xlabel("TPS")
    plt.ylabel("Avg Tx RTT")
    plt.show()

if __name__ == '__main__':
    main()

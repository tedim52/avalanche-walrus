import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py path-to-csv")
        exit(1)
    
    # Assumes csv well formatted
    # TODO may want to do some checks
    df = pd.read_csv(sys.argv[1])

    # Create RTT column
    rtt_part = {}
    for ind in df.index:
        node=df['NodeID'][ind]
        if not node in rtt_part:
            rtt_part[node] = []
        rtt_part[node].append(df['End'][ind] - df['Start'][ind])

    plt.title("RTT of Transactions")
    plt.xlabel("RTT (ms)")
    plt.ylabel("# of Tx")
    plt.hist(list(rtt_part.values()), 8, stacked=True)
    plt.show()

if __name__ == '__main__':
    main()

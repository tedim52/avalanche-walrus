package main

import (
	"context"
	"fmt"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ava-labs/coreth/ethclient"
)

func main() {
	//ctx, cancel := context.WithTimeout(context.Background(), 12*time.Second)
	//defer cancel()
	//addr := "127.0.0.1:8080"
//	client, err := rpc.DialContext(ctx, "http://"+addr)
//	if err != nil {
	//	fmt.Print("can't dial", err)
//	}
//	defer client.Close()
	client, err := ethclient.Dial("ws://127.0.0.1:9650/ext/bc/C/ws")
	if err != nil {
		fmt.Println("can't dial", err)
	}

	hash_channel := make(chan *common.Hash)

	sub, err := client.SubscribeNewAcceptedTransactions(context.Background(), hash_channel)
	if err != nil {
		fmt.Println("sub failed", err)
	}

    	fmt.Println("listening..") 
	for {
	  select {
  	    case err := <-sub.Err():
    	      fmt.Println(err)
  	    case vLog := <-hash_channel:
    	      //fmt.Println(vLog) // pointer to event log
	      tx, _, err := client.TransactionByHash(context.Background(), *vLog) 
	      if err != nil {
		fmt.Println("tx lookup failed", err)
	      } else {
		fmt.Println(vLog, " => ", tx.FirstSeen())
	      }
      	    }
	}
}

package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/tedim52/avalanche-walrus/tx-spammer/worker"
	"github.com/spf13/cobra"
	"sigs.k8s.io/yaml"
)

func init() {
	cobra.EnablePrefixMatching = true
}

func main() {
	rootCmd := newCommand()
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "transaction spammer failed %v\n", err)
		os.Exit(1)
	}
}

var (
	timeout time.Duration
	keysDir string

	clusterInfoYamlPath string
	rpcEndpoints            []string

	concurrency int
	baseFee     uint64
	priorityFee uint64
)

func newCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:        "tx-spammer",
		Short:      "Transaction spammmer for avalanche walrus testbed",
		SuggestFor: []string{"simulators"},
		Run:        runFunc,
	}

	cmd.PersistentFlags().DurationVarP(&timeout, "timeout", "t", 5 * time.Minute, "Duration to run simulator")
	cmd.PersistentFlags().StringVarP(&keysDir, "keys", "k", ".simulator/keys", "Directory for key files")
	cmd.PersistentFlags().StringVarP(&clusterInfoYamlPath, "cluster-info-yaml", "o", ".simulator/config.yml", "If non-empty, it loads the endpoints from the YAML and overwrites --config")
	cmd.PersistentFlags().StringSliceVarP(&rpcEndpoints, "endpoints", "e", nil, "If non-empty, it loads the endpoints from the YAML and overwrites --config")
	cmd.PersistentFlags().IntVarP(&concurrency, "concurrency", "c", 10, "Concurrency")
	cmd.PersistentFlags().Uint64VarP(&baseFee, "base-fee", "f", 225, "Base fee")
	cmd.PersistentFlags().Uint64VarP(&priorityFee, "priority-fee", "p", 1, "Base fee")

	return cmd
}

func runFunc(cmd *cobra.Command, args []string) {
	log.Printf("launching spammer with rpc endpoints %q or cluster info yaml %q, timeout %v, concurrentcy %d, base fee %d, priority fee %d",
		rpcEndpoints, clusterInfoYamlPath, timeout, concurrency, baseFee, priorityFee)

	cfg := &worker.Config{
		Endpoints:   rpcEndpoints,
		Concurrency: concurrency,
		BaseFee:     baseFee,
		PriorityFee: priorityFee,
	}

	if clusterInfoYamlPath != "" {
		log.Printf("loading cluster info yaml %q", clusterInfoYamlPath)
		b, err := os.ReadFile(clusterInfoYamlPath)
		if err != nil {
			log.Fatalf("failed to read cluster info yaml %v", err)
		}
		var ci networkRunnerClusterInfo
		if err = yaml.Unmarshal(b, &ci); err != nil {
			log.Fatalf("failed to parse cluster info yaml %v", err)
		}

		eps := make([]string, len(ci.URIs))
		for i := range eps {
			/*
			   e.g.,
			   uris:
			   - http://127.0.0.1:32945
			   - http://127.0.0.1:38948
			   - http://127.0.0.1:47203
			   - http://127.0.0.1:54708
			   - http://127.0.0.1:64435
			   endpoint: /ext/bc/oFzgVk4nzHApgcBAPXa7JLX5mhqAJnxQkiYD915tZ6LMPcPRu
			*/
			eps[i] = ci.URIs[i] + ci.Endpoint + "/rpc"
		}
		cfg.Endpoints = eps
	}

	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	errc := make(chan error)
	go func() {
		errc <- worker.Run(ctx, cfg, keysDir)
	}()

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGTERM, syscall.SIGINT)
	select {
	case sig := <-sigs:
		log.Printf("received OS signal %v; canceling context", sig.String())
		cancel()
	case err := <-errc:
		cancel()
		if !errors.Is(err, context.DeadlineExceeded) {
			log.Fatalf("worker.Run returned an error %v", err)
		}
	}
}

type networkRunnerClusterInfo struct {
	URIs     []string `json:"uris"`
	Endpoint string   `json:"endpoint"`
}

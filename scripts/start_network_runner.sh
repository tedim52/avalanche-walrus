#!/bin/bash
avalanche-network-runner server \
    --log-level debug \
    --port=":8080" \
    --grpc-gateway-port=":8081"

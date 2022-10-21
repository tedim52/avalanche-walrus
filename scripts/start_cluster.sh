echo $AVANODE
# Start 5 nodes
curl -X POST -k http://localhost:8081/v1/control/start -d '{"execPath":"'$AVANODE'","numNodes":5,"logLevel":"INFO"}'

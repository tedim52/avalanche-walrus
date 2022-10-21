
# Create User
set ava_pword YY0*id@K#A29
curl --location --request POST '127.0.0.1:9650/ext/keystore' \
--header 'Content-Type: application/json' \
--data-raw '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"keystore.createUser",
    "params" :{
        "username": "username",
        "password": "$ava_pword"
    }
}'

# Import Key
curl --location --request POST '127.0.0.1:9650/ext/bc/X' \
--header 'Content-Type: application/json' \
--data-raw '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"avm.importKey",
    "params" :{
        "username": "username",
        "password": "$ava_pword",
        "privateKey":"PrivateKey-ewoqjP7PxY4yr3iLTpLisriqt94hdyDFNgchSxGGztUrTXtNN"
    }
}'

# Check Balance
curl --location --request POST '127.0.0.1:9650/ext/bc/X' \
--header 'Content-Type: application/json' \
--data-raw '{
  "jsonrpc":"2.0",
  "id"     : 1,
  "method" :"avm.getBalance",
  "params" :{
      "address":"X-custom18jma8ppw3nhx5r4ap8clazz0dps7rv5u9xde7p",
      "assetID": "AVAX"
  }
} '

echo 'Steps for integrating with MetaMask: https://docs.avax.network/quickstart/fund-a-local-test-network'
echo 'Remember to add a new account to send txns!'

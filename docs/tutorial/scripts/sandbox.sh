#!/bin/sh
cd src/test/sandbox || exit
./sandbox up testnet -v

# Then:
# ./sandbox enter algod
# goal wallet new mywallet
# goal account new -w mywallet
# goal account new -w mywallet
# fund accounts using https://bank.testnet.algorand.network/
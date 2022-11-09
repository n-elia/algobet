#!/bin/sh
cd src/test/sandbox || exit
./sandbox up dev

# Create additional_accounts, funding them from the main one
additional_accounts=5
source_addr=$(./sandbox goal account list | awk 'NR==1{print $3}')
echo "Attempting to create $additional_accounts more accounts, funding them from $source_addr ..."

i=0
while [ $i -lt "$additional_accounts" ]; do
  true $((i = i + 1))
  echo "Creating account $i ..."
  new_addr=$(./sandbox goal account new | awk 'NR==1{print $6}')
  ./sandbox goal clerk send -a 50000000 -f "$source_addr" -t "$new_addr"
done

./sandbox goal account list
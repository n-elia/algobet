import time

from beaker import consts
from beaker import sandbox
from beaker.client import ApplicationClient

from contract import AlgoBet

#######################################################
# Get the accounts
#######################################################

# Get sandbox `algod` client
sandbox_client = sandbox.get_algod_client()

# Retrieve sandbox accounts
wallet_name = "mywallet"  # <-- put wallet's name here
wallet_password = "mywalletpass"  # <-- put wallet's password here
sandbox_accounts = sandbox.get_accounts(
    wallet_name=wallet_name,
    wallet_password=wallet_password,
)
print(f"Found {len(sandbox_accounts)} accounts into the wallet")

# Pop accounts from sandbox
manager_acct = sandbox_accounts.pop()
print(f"Manager account: {manager_acct.address}")

oracle_acct = sandbox_accounts.pop()
print(f"Oracle account: {oracle_acct.address}")

participant_1_acct = sandbox_accounts.pop()
print(f"Participant 1 account: {participant_1_acct.address}")

participant_2_acct = sandbox_accounts.pop()
print(f"Participant 2 account: {participant_2_acct.address}")

#######################################################
# Delete the deployed dApp
#######################################################

APP_ID = 145117913  # <-- put dApp ID here
APP_ADDR = "GZV7XH2AWIKAAEQQMEPPY7VERX7FVH5P6QKSDCUILA4JTKM75TIITUM6O4"  # <-- put dApp Address

# Create an Application client signed by Manager account
app_client_manager = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=AlgoBet(),
    # Provide a deployed AlgoBet dApp ID
    app_id=APP_ID,
    # Select the Manager account as transaction signer
    signer=manager_acct.signer
)

# Perform a delete application call
tx_id = app_client_manager.delete()

# Print the result
print(f"Deleted AlgoBet dApp with id: {APP_ID} in tx: {tx_id}")

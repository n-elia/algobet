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
# Create the event-related dApp
#######################################################

# Create an Application client
app_client_manager = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=AlgoBet(),
    # Select the Manager account as transaction signer
    signer=manager_acct.signer
)

# Unix timestamp of the event start, computed as 5minutes since code execution
event_start_unix_timestamp = int(time.time() + 5 * 60)
# Unix timestamp of the event end, computed as 10 minutes since event start
event_end_unix_timestamp = event_start_unix_timestamp + 10 * 60
# Minimum time that participants are allowed for requesting the payout, set to 15 minutes
payout_time_window_s = int(15 * 60)

# Create the application on chain using the Application Client signed by Manager account
app_id, app_addr, tx_id = app_client_manager.create(
    # Address of the Manager account
    manager_addr=manager_acct.address,
    # Address of the oracle  account
    oracle_addr=oracle_acct.address,
    # Unix timestamp of the event start
    event_start_unix_timestamp=event_start_unix_timestamp,
    # Unix timestamp of the event end
    event_end_unix_timestamp=event_end_unix_timestamp,
    # Minimum time that participants are allowed for requesting the payout
    payout_time_window_s=payout_time_window_s
)

# Print the Application ID, the Application account address and the ID of creation transaction
print(f"Created AlgoBet dApp with id: {app_id} and address: {app_addr} in tx: {tx_id}")

# Fund the app account with 1 algo
app_client_manager.fund(1 * consts.algo)

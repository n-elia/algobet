import time
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.future import transaction
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
# Participant 2 requests the payout
#######################################################

APP_ID = 145117913  # <-- put dApp ID here
APP_ADDR = "GZV7XH2AWIKAAEQQMEPPY7VERX7FVH5P6QKSDCUILA4JTKM75TIITUM6O4"  # <-- put dApp Address

# Create an Application client signed by Participant 2
app_client_participant_2 = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=AlgoBet(),
    # Provide a deployed AlgoBet dApp ID
    app_id=APP_ID,
    # Select the Participant 2 account as transaction signer
    signer=participant_2_acct.signer
)

# Query the account balance before payout
participant_2_acct_balance_before = sandbox_client.account_info(participant_2_acct.address)['amount']
print(f"Account balance before requesting the payout: {participant_2_acct_balance_before}")

# Request the payout
result = app_client_participant_2.call(
    # Transaction to be requested
    AlgoBet.payout
)

# This line shouldn't be reached because this Participant is not a winner
print("Should not get here!")

# Output the transaction ID
print(f"Transaction completed with ID: {result.tx_id}")

# Query the account balance after payout
participant_2_acct_balance_after = sandbox_client.account_info(participant_2_acct.address)['amount']
print(f"Account balance after requesting the payout: {participant_2_acct_balance_after}")

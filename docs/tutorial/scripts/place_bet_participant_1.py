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
# Participant 1 places a bet
#######################################################

APP_ID = 145117913  # <-- put dApp ID here
APP_ADDR = "GZV7XH2AWIKAAEQQMEPPY7VERX7FVH5P6QKSDCUILA4JTKM75TIITUM6O4"  # <-- put dApp Address

# Create an Application client signed by Participant 1
app_client_participant_1 = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=AlgoBet(),
    # Provide a deployed AlgoBet dApp ID
    app_id=APP_ID,
    # Select the Participant 1 account as transaction signer
    signer=participant_1_acct.signer
)

# Opt-in into the dApp
app_client_participant_1.opt_in()

# Place a bet as Participant 1 forecasting a home team win
result = app_client_participant_1.call(
    # Transaction to be requested
    AlgoBet.bet,
    # Bet deposit transaction
    bet_deposit_tx=TransactionWithSigner(
        # Transaction of type PaymentTxn
        txn=transaction.PaymentTxn(
            # Address of the account requesting the transfer
            participant_1_acct.address,
            # Transaction parameters (use suggested)
            app_client_participant_1.client.suggested_params(),
            # Receiver account address
            APP_ADDR,
            # Transfer amount
            140 * consts.milli_algo),
        # Payment transaction signer
        signer=participant_1_acct.signer
    ),
    # Option to bet on: home team win
    opt=0
)

# Output the transaction ID.
print(f"Transaction completed with ID: {result.tx_id}")

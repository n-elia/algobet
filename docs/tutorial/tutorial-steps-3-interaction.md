# 6. Define the event

At this point, we need to define an event. Then, we will properly instantiate and AlgoBet dApp to bet on the defined event.

To instantiate the AlgoBet dApp, we will need:
- An Algorand account which will serve as manager of the dApp.
- An Algorand account which will serve as oracle of the dApp.
- The Unix timestamp which represents the event start time.
- The Unix timestamp which represents the event end time.
- The minimum allowed amount of time for winning participants to claim their rewards.

Let's suppose that we want to build a bet system for the soccer match _Catanzaro - Crotone_, which starts _5 minutes_ after the creation of the associated AlgoBet dApp and lasts for _10 minutes_. Also suppose that we want to allow the winning participants to request the payout for at least _15 minutes_ after the end of the match.

We will use the Algorand accounts that we created and funded in the previous steps.
Taking advantage of `beaker.sandbox`, we can easily pop the accounts from the sandbox within a Python script. Please notice that `sandbox.get_accounts()` returns an ordered list of sandbox accounts. Therefore, among the code snippets of the remaining tutorial steps, we will always pop the accounts in the same order to ensure consistency:

```python
from beaker import sandbox

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
```

The first popped account will be the manager account; the second one will be the oracle account; the remaining two accounts will be two different participant accounts. Each account will be identified by means of its address.

# 7. Create the AlgoBet dApp as Manager

We're now ready to deploy our AlboBet dApp, associated to _Catanzaro - Crotone_ soccer match.

To deploy our dApp we will leverage Beaker. Let's build a Python script together.

At first, we have to retrieve sandbox accounts as explained in previous steps:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient` ([docs](https://algorand-devrel.github.io/beaker/html/application_client.html#application-client)), which will provide us a convenient way to interact with AlgoBet. The client's operations will be signed using the Manager account.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

# Create an Application client
app_client_manager = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=AlgoBet(),
    # Select the Manager account as transaction signer
    signer=manager_acct.signer
)
```

We are now ready to call the `ApplicationClient.create()` method, that will submit an Application Call of type [Create](https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/#create) transaction signed by the _Manager_ account to create the AlgoBet application. The method's arguments are chosen based on the event.

```python
import time
from beaker import consts

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

# Print the current application state
print(f"Current application state: {app_client_manager.get_application_state()}")
```

Save the Python script as `create_algobet_dapp.py`, then open a terminal and execute the script by issuing:

```shell
$> python create_algobet_dapp.py
```

The script should have an output similar to:

```text
Found 5 accounts into the wallet

Manager account: SKBBUTCFKLPOGWMHLMA2ME3OAR4D2KIXLBXX366R2N7EOBS56QNYWN3SKE
Oracle account: P7LUQ4IIU43LGBHSEMDQ2K7OK75ZMLJC2ACEVX2BUAGCCYOGQIQ3LTJGWM
Participant 1 account: FLD3ATI6H3MTVBVE6X3OF7DJF7PC42Z4XTCVXQ3DMDK6O3NRRCQMGUFDKU
Participant 2 account: DB6U6AAH56T2SIMQVUMI4O3SFKTY2QIU2GAPI3N2PRXTNATWFTYGXJUBKI

Created AlgoBet dApp with id: 144934470 and address: EVTLVHOMFDKGWUJN54TBZB5KIIMVKI3A65T77O6ZWUIX5UXE3YTPN754NI in tx: KO5OMLN34ZVRYBGLN5OM3BP4YX5M26CG5HVBUAIOQWR5WCDHICJQ

Process finished with exit code 0
```

> Warning: please take note of the Application ID and the Application Account Address as they will enable us to interact with the application during the next steps.

The AlgoBet dApp related to _Catanzaro - Crotone_ soccer match is now deployed on the testnet, and it is reachable through its Application Id.

# 8. Place a bet as Participant 1

We're now ready to place our bets on _Catanzaro - Crotone_ soccer match, by interacting with the deployed AlgoBet dApp. Let's suppose that _Giovanni_, which is the _Participant 1_, is forecasting a _win of the home team_.

To interact with the deployed dApp, we will leverage Beaker. Let's build a Python script together.

At first, we have to retrieve sandbox accounts as explained in previous steps:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient` ([docs](https://algorand-devrel.github.io/beaker/html/application_client.html#application-client)), which will provide us a convenient way to interact with AlgoBet.
This time, the application client must be signed by the _Participant 1_ account, and it must interact with the already deployed AlgoBet instance.

> Warning: please remember to paste the Application ID and the Application Account Address copied before.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

Before a _Participant_ account can interact with AlgoBet dApp it must opt-in. An [opt-in transaction](https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/?from_query=opt-in#opt-in) is simply an asset transfer with an amount of 0. When using Beaker framework, the opt-in call can be automatically issued using the `ApplicationClient.opt_in()` method.

Once the opt-in is completed, we are ready to call the `ApplicationClient.call()` method, that will submit an Application Call transaction to the AlgoBet application signed by the _Participant 1_ account.

The transaction that we are willing to request an execution to is `AlgoBet.bet`. This transaction requires a contextual deposit transaction, that must transfer _140 milliAlgo_ to the dApp account as bet deposit. We will therefore compose an atomic transaction group using Beaker.

> Note: learn more about Algorand Atomic Transfers [here](https://developer.algorand.org/articles/algorand-atomic-transfers/) on the developer portal or [here](https://developer.algorand.org/docs/get-details/atomic_transfers/) on the Algorand documentation.

The bet option must be chosen, too. It's possible to choose among 0 (Home team wins), 1 (Away team wins) or 2 (Draw). In this case, since the _Participant 1_ wants to bet on the home team victory, the chosen option is _0_.

```python
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.future import transaction

from beaker import consts

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
```

Save the Python script as `algobet_participant_1_bet.py`, then open a terminal and execute the script by issuing:

```shell
$> python algobet_participant_1_bet.py
```

The script should have an output similar to:

```text
Transaction completed with ID: CTV34P2G5G2DO6VHOM436JTJP6RUBVNIE57MNPHRDX7QRJPFY46Q
```

**Troubleshooting tip**: if you obtain the following error, then the event start timestamp is already passed, therefore _Participants_ are no more allowed to place bets. You can go back to the dApp creation step to restart the tutorial with a fresh AlgoBet instance.

```text
global LatestTimestamp
bytec 13 // "event_start_timestamp"
app_global_get
<
// Event has already started
assert		<-- Error
load 8
gtxns Amount
bytec 14 // "bet_amount"
app_global_get
```

# 9. (optional) Inspect Application State

Beaker framework refers to _Global State_ as [Application State](https://algorand-devrel.github.io/beaker/html/state.html#application-state).

We can query the Application State of our deployed dApp to observe the values of global variables, such as the `oracle_addr` which stores the address of the _Oracle_ account.

Let's build a Python script together. At first, we have to retrieve sandbox accounts and create an Application client signed by Participant 1, as explained in previous steps.
Please note that any account may be used for querying the application state.

```python
from beaker import sandbox
from beaker.client import ApplicationClient

from contract import AlgoBet

# Application ID and address
APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

Then, we can use the `ApplicationClient.get_application_state()` method to retrieve the current application state:

```python
# Print the current application state
print(f"Current application state: {app_client_participant_1.get_application_state()}")
```

Save the Python script as `inspect_application_state.py`, then open a terminal and execute the script by issuing:

```shell
$> python inspect_application_state.py
```

The script should have an output similar to:

```text
Current application state: {'counter_opt_1': 0, 'counter_opt_2': 0,
 'oracle_addr': '7a7a63bdf93c4ef87ba758a439023c423d9e44eedd3c79a03f7f01b6a26c3d5f', 'event_result': 99, 'counter_opt_0': 1, 'event_start_timestamp': 1668789100, 'manager': '9110d3abec8f898b606bd36cfdd518e0b5ac7b5723e1c42a0ee8311fbd439a66', 'event_end_timestamp': 1668789400, 'bet_amount': 140000, 'winning_count': 0, 'stake_amount': 140000, 'winning_payout': 0, 'payout_time_window_s': 900}
```

The output string is a JSON document. It represents the key-value variables stored into the AlgoBet dApp Global State. 

# 10. (optional) Inspect Participant 1 Account State

Beaker framework refers to _Local State_ as [Account State](https://algorand-devrel.github.io/beaker/html/state.html#account-state).

We can query the Account State of our deployed dApp to observe the values of local variables, such as `chosen_opt`, which stores the bet forecast chosen by the account.

Let's build a Python script together. At first, we have to retrieve sandbox accounts and create an Application client signed by Participant 1, as explained in previous steps.
Please note that each account may be used for querying its own local state only after having opted-in.

```python
from beaker import sandbox
from beaker.client import ApplicationClient

from contract import AlgoBet

# Application ID and address
APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

Then, we can use the `ApplicationClient.get_application_state()` method to retrieve the current application state:

```python
# Print the current account state
print(f"Current account state: {app_client_participant_1.get_account_state()}")
```

Save the Python script as `inspect_account_state.py`, then open a terminal and execute the script by issuing:

```shell
$> python inspect_account_state.py
```

The script should have an output similar to:

```text
Current account state: {'has_placed_bet': 1, 'chosen_opt': 0, 'has_requested_payout': 0}
```

The output string is a JSON document. It represents the key-value variables stored into the AlgoBet dApp Local State inherent to the account of _Participant 1_.

# 11. Place a bet as Participant 2

We can place a bet as _Participant 2_ using the same script we already used for _Participant 1_. The only difference that we will introduce is that the Application Client will be signed by the _Participant 2_ account instead of _Participant 1_ one.

At first, we have to retrieve sandbox accounts:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient`. This time, the application client must be signed by the _Participant 2_ account.

> Warning: please remember to paste the Application ID and the Application Account Address copied before.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

We can then opt-in and place a bet. We will make _Participant 2_ choose a different option than _Participant 1_: `1` (Away team wins).

> Warning: please remember that Participants may bet until the match starts. Therefore, you must complete the bet steps before the event start timestamp.

```python
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.future import transaction

from beaker import consts

# Opt-in into the dApp
app_client_participant_2.opt_in()

# Place a bet as Participant 2 forecasting an away team win
result = app_client_participant_2.call(
    # Transaction to be requested
    AlgoBet.bet,
    # Bet deposit transaction
    bet_deposit_tx=TransactionWithSigner(
        # Transaction of type PaymentTxn
        txn=transaction.PaymentTxn(
            # Address of the account requesting the transfer
            participant_2_acct.address,
            # Transaction parameters (use suggested)
            app_client_participant_2.client.suggested_params(),
            # Receiver account address
            APP_ADDR,
            # Transfer amount
            140 * consts.milli_algo),
        # Payment transaction signer
        signer=participant_2_acct.signer
    ),
    # Option to bet on: away team win
    opt=1
)

# Output the transaction ID.
print(f"Transaction completed with ID: {result.tx_id}")
```

Save the Python script as `algobet_participant_2_bet.py`, then open a terminal and execute the script by issuing:

```shell
$> python algobet_participant_2_bet.py
```

The script should have an output similar to:

```text
Transaction completed with ID: CTV34P2G5G2DO6VHOM436JTJP6RUBVNIE57MNPHRDX7QRJPFY46Q
```

# 12. Set the result as Oracle

Now that bets are placed, we must wait for the event to start. We set the event start 5 minutes after the dApp creation.

Please note that _Participants_ are not allowed to bet after the event start, and therefore bet transactions that occur after event start timestamp will fail.

Moreover, the _Oracle_ account won't be able of setting the event result before the event end.
We set the event end timestamp 10 minutes after the event start. Thus, after 15 minutes from its creation, our AlgoBet dApp will consider the event finished, and will allow the _Oracle_ account to set the event result.

Let's assume that Catanzaro finally scored twice, winning the game 2–1. Therefore, the winning option is "Home team win", represented by option `0`.

We can set the result as _Oracle_ using another Python script. Similar as we did with _Participants_ to make them bet, we will instantiate an Application Client signed by the _Oracle_ account to allow it requesting transactions against the deployed dApp.

At first, we have to retrieve sandbox accounts:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient`. This time, the application client must be signed by the _Oracle_ account.

> Warning: please remember to paste the Application ID and the Application Account Address copied before.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

# Create an Application client signed by Oracle account
app_client_oracle = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=AlgoBet(),
    # Provide a deployed AlgoBet dApp ID
    app_id=APP_ID,
    # Select the Oracle account as transaction signer
    signer=oracle_acct.signer
)
```

We don't need to opt-in, because the Oracle account won't use the Local State. We will make _Oracle_ account to choose `0` (Home team wins) as winning option.

> Warning: please remember that Oracles must wait the match end before being allowed to set the event result.

```python
# Set the result "Home team win"
result = app_client_oracle.call(
    # Transaction to be requested
    AlgoBet.set_event_result,
    # Winning option: home team win
    opt=0
)

# Output the transaction ID.
print(f"Transaction completed with ID: {result.tx_id}")
```

Save the Python script as `set_result.py`, then open a terminal and execute the script by issuing:

```shell
$> python set_result.py
```

The script should have an output similar to:

```text
Transaction completed with ID: CTV34P2G5G2DO6VHOM436JTJP6RUBVNIE57MNPHRDX7QRJPFY46Q
```

**Troubleshooting tip**: if you obtain the following error, then the event end timestamp has not been reached yet, therefore _Oracle_ is not yet allowed to set the event result. You shall wait the event end time before requesting the execution of this transaction.

```text
global LatestTimestamp
bytec_1 // "event_end_timestamp"
app_global_get
>=
// Event expiry time not reached, yet.
assert		<-- Error
load 19
intc_0 // 0
==
bnz seteventresult_10_l16
```
# 13. Request the payout as Participant 1 (winner)

At this point, the winning _Participants_ are allowed to claim their rewards.

In this tutorial, we made _Participant 1_ to bet on "Home team win" (option `0`), and _Participant 2_ to bet on "Away team win" (option `1`). Thus, the former will be a winner while the latter will be a looser.

Let's write a Python script that requests the payout as _Participant 1_.
At first, we have to retrieve sandbox accounts:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient`. This time, the application client must be signed by the _Participant 1_ account.

> Warning: please remember to paste the Application ID and the Application Account Address copied before.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

Let's now request the payout transaction. The account balance is also printed before and after the payout, to make you see the effect of payout transaction.

```python
# Query the account balance before payout
participant_1_acct_balance_before = sandbox_client.account_info(participant_1_acct.address)['amount']
print(f"Account balance before requesting the payout: {participant_1_acct_balance_before}")

# Request the payout
result = app_client_participant_1.call(
    # Transaction to be requested
    AlgoBet.payout
)

# Output the transaction ID
print(f"Transaction completed with ID: {result.tx_id}")

# Query the account balance after payout
participant_1_acct_balance_after = sandbox_client.account_info(participant_1_acct.address)['amount']
print(f"Account balance after requesting the payout: {participant_1_acct_balance_after}")
```

Save the Python script as `payout_participant_1.py`, then open a terminal and execute the script by issuing:

```shell
$> python payout_participant_1.py
```

The script should have an output similar to:

```text
Account balance before requesting the payout: 7855000
Transaction completed with ID: RHZQQQQ4KPQUCMKFSTPKYNJZJG5J3E2W2BB33TMTK42MMEDN6S5A
Account balance after requesting the payout: 7993000
```

# 14. (optional) Request the payout as Participant 2 (looser)

_Participants_ which did not choose the winning option will not be allowed to claim their rewards.

In this tutorial, we made _Participant 2_ to bet on "Away team win" (option `1`), which does not correspond to the winning option.

Let's write a Python script that requests the payout as _Participant 2_. The expected result is that the AlgoBet dApp refuses the execution of the payout transaction.
At first, we have to retrieve sandbox accounts:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient`. This time, the application client must be signed by the _Participant 2_ account.

> Warning: please remember to paste the Application ID and the Application Account Address copied before.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

Let's now request the payout transaction.

```python
# Query the account balance before payout
participant_2_acct_balance_before = sandbox_client.account_info(participant_2_acct.address)['amount']
print(f"Account balance before requesting the payout: {participant_2_acct_balance_before}")

# Request the payout
result = app_client_participant_2.call(
    # Transaction to be requested
    AlgoBet.payout
)

print("This line should not be reached.")
```

Save the Python script as `payout_participant_2.py`, then open a terminal and execute the script by issuing:

```shell
$> python payout_participant_2.py
```

We expect this Python script to throw an error, since the _Participant 2_ is not a winner participant.

The script should have an output similar to:

```text
Found 5 accounts into the wallet
Manager account: SKBBUTCFKLPOGWMHLMA2ME3OAR4D2KIXLBXX366R2N7EOBS56QNYWN3SKE
Oracle account: P7LUQ4IIU43LGBHSEMDQ2K7OK75ZMLJC2ACEVX2BUAGCCYOGQIQ3LTJGWM
Participant 1 account: FLD3ATI6H3MTVBVE6X3OF7DJF7PC42Z4XTCVXQ3DMDK6O3NRRCQMGUFDKU
Participant 2 account: DB6U6AAH56T2SIMQVUMI4O3SFKTY2QIU2GAPI3N2PRXTNATWFTYGXJUBKI

Account balance before requesting the payout: 9714000

Traceback (most recent call last):
  [...]
urllib.error.HTTPError: HTTP Error 400: Bad Request

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  [...]
algosdk.error.AlgodHTTPError: TransactionPool.Remember: transaction RZMP642OUQZ63HPLUH7E6C77TUAEDGABYFIVICDGBDJFL7AQ4POQ: logic eval error: assert failed pc=834. Details: pc=834, opcodes=app_local_get
==
assert

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  [...]
beaker.client.logic_error.LogicException: Txn RZMP642OUQZ63HPLUH7E6C77TUAEDGABYFIVICDGBDJFL7AQ4POQ had error 'assert failed pc=834' at PC 834 and Source Line 416: 

	txn Sender
	bytec 10 // "chosen_opt"
	app_local_get
	==
	// You did not choose the winning option
	assert		<-- Error
	txn Sender
	bytec 12 // "has_requested_payout"
	app_local_get
	intc_0 // 0
```


# 15. (optional) Delete the AlgoBet dApp

Let's write a Python script that deletes the AlgoBet dApp as _Manager_ account. 

> Remember that you will be allowed to request the AlgoBet dApp deletion only if the time allowed for payouts is elapsed. In this tutorial, we set a 15 minutes time interval.

At first, we have to retrieve sandbox accounts:

```python
from beaker import sandbox

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
```

Next, we instantiate a Beaker's `ApplicationClient`. This time, the application client must be signed by the _Manager_ account.

> Warning: please remember to paste the Application ID and the Application Account Address copied before.

```python
from beaker.client import ApplicationClient

from contract import AlgoBet

APP_ID = 888  # <-- Paste Application ID here
APP_ADDR = 'XXXXXX'  # <-- Paste Application Account Address here

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
```

Let's now request the delete transaction.

```python
# Perform a delete application call
tx_id = app_client_manager.delete()

# Print the result
print(f"Deleted AlgoBet dApp with id: {APP_ID} in tx: {tx_id}")
```

Save the Python script as `delete_algobet_dapp.py`, then open a terminal and execute the script by issuing:

```shell
$> python delete_algobet_dapp.py
```

The script should have an output similar to:

```text
Found 5 accounts into the wallet

Manager account: SKBBUTCFKLPOGWMHLMA2ME3OAR4D2KIXLBXX366R2N7EOBS56QNYWN3SKE
Oracle account: P7LUQ4IIU43LGBHSEMDQ2K7OK75ZMLJC2ACEVX2BUAGCCYOGQIQ3LTJGWM
Participant 1 account: FLD3ATI6H3MTVBVE6X3OF7DJF7PC42Z4XTCVXQ3DMDK6O3NRRCQMGUFDKU
Participant 2 account: DB6U6AAH56T2SIMQVUMI4O3SFKTY2QIU2GAPI3N2PRXTNATWFTYGXJUBKI

Deleted AlgoBet dApp with id: 145117913 in tx: LHFJ2KROWM5XAHPYYRVGQ2CGPZA5J6HW6SIB7QYGFPNUU7K5TWZQ
```

> Note that the _Manager_ account which requests the dApp deletion will receive, with a payment transaction, all the content of dApp account at the moment of its deletion.


# Summary

Congrats, you reached the end of the tutorial!

So far, you learned:

* how to setup an Algorand environment for developing Smart Contracts using Beaker framework and for deploying them leveraging the sandbox;
* how to generate TEAL code from a Beaker Smart Contract;
* how to deploy a Beaker dApp on Algorand testnet;
* how to setup a decentralized bet system running on Algorand network, using AlgoBet Smart Contract.

Have fun with Beaker!
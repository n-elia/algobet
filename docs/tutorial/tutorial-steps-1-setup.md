# 1. Environment setup

In this section you will find the instructions to setup a suitable environment to deploy and interact with an AlgoBet smart contract instance by yourself. This setup was tested in a Ubuntu environment.

At first, please create a new folder to put all the stuff needed for going through this tutorial, naming it as you prefer. From now on, we will refer to that folder as _root directory_.

You will need to install some dependencies in order to execute the smart contract:

- **Python**: we recommend to install Python 3.10+, due to _Beaker_ framework requirements. Most of the time, a Python installation is already available in your operating system. To check your current Python version, open a terminal and issue `python3 --version`. If the Python version is less than 3.10, please refer to [Python documentation](https://docs.python.org/3/using/index.html#python-setup-and-usage) to install a newer version.

We recommend to instantiate a virtual environment (venv) before proceeding with this tutorial. To do it, open a terminal,move to _root directory_ and issue:

```
# On Ubuntu or MacOS
python3 -m venv venv
source ./venv/bin/activate

# On Windows
python3 -m venv venv
.\venv\Scripts\activate
```

This will create a virtual env for you. The virtual environment will be successfully activated if your command prompt starts with the *(venv)* word.

- **Beaker**: it is a Python framework for building Smart Contracts on Algorand using PyTeal. The AlgoBet smart contract has been developed using this framework.

    This tutorial has been developed on top of Beaker version 0.3.6. It can be installed using `pip`:

        pip install beaker-pyteal==0.3.6

- **Docker and Docker Compose**: a working Docker installation is needed in order to execute the Algorand sandbox. If you are new to Docker, we recommend referring to [Docker documentation](https://docs.docker.com/get-docker/) to install Docker Desktop.


- **Algorand Sandbox**: this tool provides a quick and easy way to create, configure and deploy an Algorand node using Docker. The containerized node may be joined to any of the three Algorand networks, and you will be able to manage it through the sandbox environment.

    To install the Algorand sandbox, move into the _root directory_ and then clone the sandbox repository:

    > Note for Windows users: you may need to perform some more steps before being able to run the Algorand sandbox. Please follow the instructions provided [here](https://github.com/algorand/sandbox#windows).
  
        git clone https://github.com/algorand/sandbox.git

    To spin up the sandbox and attach it to the Algorand _testnet_, make sure that Docker is running, and then execute:

        cd sandbox
        ./sandbox up testnet

At this point, your environment satisfies all the requirements, and we can start to dive into the core of this tutorial!

# 2. Wallet and accounts creation

To deploy and interact with AlgoBet, we will pick and use some accounts from sandbox. When using the sandbox in _testnet_ mode, it will be necessary to manually create a new wallet, populate it with new accounts and fund them using a testnet faucet.

You can use the terminal that is running the sandbox to do that. Execute the following commands:

```
./sandbox enter algod
goal wallet new <walletName>
```

You first have to enter into the node, then you can start the wallet creation passing the wallet name.
The command execution will ask for a password for the wallet, and some security settings.
Once the process is over, you can check if the wallet was correctly instantiated executing:

```sh
goal wallet list
```

And look for your just created wallet.
If everything is fine, you can go further adding to the wallet some accounts. Staying in the `algod` node, you can execute:

```sh
goal account new -w <walletName>
```

We need to create 4 accounts.
You can check if the account are correctly created by typing:

```sh
goal account list
```

If everything is correct, you can finally exit from the `algod` node:

```sh
exit
```

And this will lead you to the standard terminal.

# 3. Account funding

To provide your test accounts with some virtual funds, you can use [this](https://bank.testnet.algorand.network) testnet dispenser.

Each account may be funded by following these steps:

* complete the Captcha puzzle
* copy and paste the account address into the _target address_ textbox
* press the "Dispense" button

You can check your accounts balances at any time by using the `goal account list` command seen in the previous step.

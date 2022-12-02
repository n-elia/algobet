## Tutorial breakthrough
The first step will be the setup of a suitable environment, which comprises a working installation of _Beaker_ and the _Algorand sandbox_ connected to the testnet.
It will be necessary to create a _wallet_, populate it with at least two _accounts_ and fund those accounts using any of the available testnet _faucets_.
The next step will be to clone the repository containing the AlgoBet _smart contract_, compile it into _TEAL code_ and deploy it on the testnet.
Finally, we will interact with the deployed dApp to place a bet, set the result and claim the reward.

All the scripts created through this tutorial are provided into AlgoBet ([github repository](https://github.com/n-elia/algobet)), inside `docs/tutorial/scripts` directory.

## Target smart contract
**AlgoBet** is a basic decentralized betting system based on Algorand smart contract, in which users can bet on the result of a particular event. The betting system is inspired by the classical sport bets, such as football or basketball. In these sports, the typical bet can cover three results for the game: _Home team wins_, _Away team wins_, _Draw_.
Each instance of AlgoBet will handle a particular event, therefore it will be necessary to deploy multiple AlgoBet instances to manage multiple events.

The bet stake is *fixed* in 140 milliAlgos. Users are not allowed to bet more than this fixed stake, neither to place more than one bet each. Events, and therefore related bets, are handled using a time management system to set the event start and end as two timestamps, and to define a payout time window. This mechanism also prevents the manager to delete the contract until the winning bets are paid.

*Three actors* are involved in the AlgoBet workflow:

* **Manager**: the manager handles the smart contract instance lifecycle phases, such as creation and deletion, plus a manager can set the oracle account;
* **Oracle**: the oracle account can set the event result once it terminates. Ideally, it is the link between the smart contract and the real world, and practically it is an Algorand account chosen by the manager at creation time;
* **Users**: the users interact with the smart contract placing bets on the event and claiming their earnings if they placed a bet on the correct result. They need to opt-in to che contract in order to use these features.

AlgoBet was developed using **Beaker**, a novel development framework that makes easier to write PyTeal code, then it was tested on the Algorand sandbox.

## Oracles
In order to work properly, a betting service needs to retrieve the necessary information about the relevant event. In blockchain enviroments, data-feeds from the real world are operated through [**Oracles**](https://medium.com/@teexofficial/what-are-oracles-smart-contracts-the-oracle-problem-911f16821b53), i.e., entities (human, software, sensor etc.) included in a smart contract to bridge on- and off-chain ecosystems. 
AlgoBet needs to interact with an oracle for retrieving the event result. In this tutorial, you will create an Agorand account that will serve as oracle account.

## Beaker
**Beaker** is a [new programming framework](https://developer.algorand.org/articles/hello-beaker/?from_query=hello%20bea) for building smart contracts on Algorand. The traditional [PyTeal](https://pyteal.readthedocs.io/en/stable/) framework has proven to be troublesome for may in that it may result unfamiliar, complex and with a counter-intuitive structure. 
Beaker's goal is to improve development experience both for current algorand developers and for newcomers.
Because of its recent release, few attempts were made in employing Beaker for DApps implementations. Such an activity is needed in order to test its potentialites and to identify what is to be improved.

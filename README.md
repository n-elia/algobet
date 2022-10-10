# Group 5 - Project proposal: “AlgoBet”

_Authors: Nicola Elia, Alessandro Parenti, Domenico Tortola_

This project work proposal was developed by team #5 during the International School on Algorand Smart Contracts ([link](https://algorand-school.github.io/algorand-school/)).

Current state: the proposal has been approved by the School's organising committee.

## Project goal

The project goal consists in implementing a **decentralized bet system**, in which several participants may bet on the result of a particular event. The smart contract would collect the bids and - at the end of the event - the Algorand network will autonomously distribute the payouts between the winning participants.

The project will be developed in a **step-by-step** fashion, in which each step is a bit more complex than the previous one, either from functionalities or implementation points of view. Each step will be developed if the previous one has been successfully implemented and deployed within a test network.

_Step 1_ - The goal at this step is to build a basic bet system. Participants can bet on the result of a particular, pre-defined event, created by a designated member. The event, as well as the bet, must be uniquely described by sets of predefined information. In this step, the bet stake is predefined. After the end of the event, winning participants can have the payout transferred to his or her wallet by calling the relative function. Non-winning participants would not be able to claim any reward.

Further steps or extensions will be defined if _Step 1_ gets completed.

## Smart Contract Specifications

The Smart Contract specifications vary based on the development step.

Each step’s use case is described in the previous section of this document.

_Step 1_

- Involved actors
  - _E_: creates an event
  - _Px_: participant _x_, which places a bet on the event
  - _O_: at the end of the event, sets the final result
- Exposed transactions
  - `EventCreate` (Smart Contract creation): may be used by the authorized actor _E_ only, to issue the creation of a new Smart Contract related to a particular event (disposable Smart Contract fashion). The event is uniquely described by a set of predefined information, for instance: `event_desc = {event_type, event_timestamp, involved_actors, possible_forecast_options}`, which is passed as a parameter during the Smart Contract creation.
  - `EventPlaceBet`: may be used by any participant _Px_ to place a bet on a particular event. A bet must be uniquely identified by a set of information passed as a parameter, for instance: `bet_obj = {event_obj, Px_address, forecast_option, bet_amount}`. The forecast option must be one of the options specified into `possible_forecast_options`.
  - `EventResultSet`: may be used by the oracle account _O_ only, for setting the final result of the event related to that Smart Contract.
  - `EventBetOutcomeGet`: may be used by any winning participant to retrieve their outcome.
- Logics
  - The Smart Contract stores the event descriptor, and manages the bids related to that particular event.
  - The Smart Contract takes a predefined amount of Algos from each participant _Px_ willing to place a bet. It also takes a small amount of Algos used as a fee for rewarding the oracle _O_.
  - The Smart Contract can be deleted only if all the winning participants have got their profits.

Further steps will be defined if _Step 1_ gets completed. They may include:

- Implementation of a backup mechanism that refunds the participants _Px_ if the oracle _O_ does not provide the event result within a particular period of time.
- Implementation of custom stake and consequent payout relative to the stake.
- Implementation of `EventDelete` transaction, which may be requested by the authorized actor _E_ only, to issue the deletion of the Smart Contract, and which is allowed only after a certain expiry date or if all the winner accounts have already taken their profits.
- Implementation of oracle actor _O_ as another Smart Contract to improve flexibility
- Anonymization of each participant’s bets, which are revealed only at the end of the event.

## State of the Art

To our knowledge, a state-of-the-art decentralized bet system based on Algorand does not exist, while decentralized betting is a relevant topic, especially from the oracles implementation point of view.

- A [post](https://forum.algorand.org/t/algorand-bet-my-first-attempt-at-a-dapp/3957) exists on the Algorand Forum, regarding the realization of a bet system DApp. The project seems dismissed.
- References to sports decentralized bet systems may be also found on [Goracle](https://www.goracle.io/post/algorand-the-future-of-sports-betting). Goracle aims to implement Algorand oracles as data feeds from real-world data providers.

In this proposal context, oracle services are relevant since the proposed solution, integrated with a suitable oracle, could lead to a fully decentralized bet system in which the participants' fees are only used for rewarding the oracles.

## Technical Challenges

_Step 1_

- Implementation of Smart Contracts application using [Beaker](https://github.com/algorand-devrel/beaker).
- Implementation of a logic which comprises an oracle.
- Implementation of a scalable system with an unknown number of participants.
- Unique identification of events.

Further steps will be defined based on next steps requirements and proposed functionalities.


## 4. Clone repository
Once our sandbox environment has been set up, we need to retrieve the AlgoBet repository.  
To do so, open a terminal from the _root folder_ and clone the `algobet` repository:

```sh
git clone https://github.com/n-elia/algobet.git
```

The `algobet` directory will be created and populated with the repository content. There you will find all the files necessary to set up and deploy an AlgoBet DApp:
* `docs/`: contains the project documentation;
* `src/`: contains the Smart Contract source code.
  * `src/teal/`: stores the Smart Contract, compiled into TEAL code;
  * `src/test/`: stores the Smart Contract tests;
  * `src/contract.py`: Smart Contract source code;
  * `src/requirements.txt`: Python requirements to be installed for managing the Smart Contract;
* `README.md`: readme file.

Now, install the requirements needed from the .txt file in the *src* folder by opening up a terminal and executing:

```sh
cd algobet/src/

pip install -r requirements.txt
```

Your Python environment is now ready to deploy an AlgoBet DApp.


## 5. (optional) Compile to TEAL

One of the most user-friendly features of the Beaker framework is that it allows deploying a Smart Contract on the Algorand network without having to go through the manual generation of the TEAL bytecode. Indeed, this step is operated automatically by Beaker upon the moment of the Smart Contract _create_ Application Call. 

However, knowing the TEAL code might be important to understand how an application interacts with the Algorand Virtual Machine or to identify bugs and issues which occur during its execution.

In order to compile our Beaker contract into TEAL bytecode, we can exploit Beaker functionalities.
Create a new Python script with the content proposed below. 

```python
import json

from src.contract import AlgoBet as App

app = App()
print(app.approval_program)
print(app.clear_program)
print(json.dumps(app.contract.dictify()))

for filename, content in [
    ("approval_program.teal", app.approval_program),
    ("clear_program.teal", app.clear_program),
    ("contract.json", json.dumps(app.contract.dictify()))
]:
    with open(filename, "w") as fp:
        fp.write(content)
```

Through this script we are going to generate the [two programs](https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/) that ultimately constitute the TEAL code: the *Approval Program* and the *Clear State Program*. The latter is used to handle accounts using the clear call to remove the smart contract from their balance record while the former is responsible for processing all application calls to the contract.

Once created the script, save it as `src/teal/compile.py`. 

Now open the terminal and, from the `algobet` directory, run the Python script:

```sh
python src/teal/compile.py
```

This will generate the `approval_program.teal` and `clear_program.teal` files, that you can inspect and that you could also use for manually deploying the AlgoBet Smart Contract.

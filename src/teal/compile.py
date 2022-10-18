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

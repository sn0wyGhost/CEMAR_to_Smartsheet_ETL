import os
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd

### Define dependencies ###
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

cemar_public_key = os.getenv("cemar_public_key")
cemar_private_key = os.getenv("cemar_private_key")

if not cemar_public_key:
    raise RuntimeError("cemar_public_key is not set")
if not cemar_private_key:
    raise RuntimeError("cemar_private_key is not set")

### App ###
from cemar_sdk import sdk
client = sdk()
client.InitialiseSession(cemar_public_key, cemar_private_key)

pageNumber = 0 
pageSize =  100000

# Get contracts list
contracts_json = client.GetContracts(pageNumber, pageSize)

# Create contracts data frame
contracts_df = pd.DataFrame(contracts_json["data"])
contracts_df.to_csv("contracts.csv", index=False, encoding="utf-8")

# Get task orders data
task_orders_data = []
for row in contracts_df.itertuples(index=False):
    contract_id = row.contractId
    task_orders_json = client.GetTaskOrders(contract_id, pageNumber, pageSize)
    try:
        for item in task_orders_json["data"]:
            item["contractId"] = contract_id
        task_orders_data.extend(task_orders_json["data"]) 
    except:
        print(f"Contract {contract_id} task orders contained no data")

# Create task orders data frame
task_orders_df = pd.DataFrame(task_orders_data)
task_orders_df.to_csv("task_orders.csv", index=False, encoding="utf-8")

# Get compensation events data
compensation_events_data = []
for row in contracts_df.itertuples(index=False):
    contract_id = row.contractId
    compensation_events_json = client.GetCompensationEvents(contract_id, pageNumber, pageSize)
    try:
        for item in compensation_events_json["data"]:
            item["contractId"] = contract_id
        compensation_events_data.extend(compensation_events_json["data"]) 
    except:
        print(f"Contract {contract_id} compensation events contained no data")

# Create task orders data frame
compensation_events_df = pd.DataFrame(compensation_events_data)
compensation_events_df.to_csv("compensation_events.csv", index=False, encoding="utf-8")

# Upload data to pre-established Smartsheet sheets
from smartsheet_handler import handler
sh = handler()
sh.UpdateSheet(contracts_df, sh.contracts_sheet_id)
sh.UpdateSheet(task_orders_df, sh.task_orders_sheet_id)
sh.UpdateSheet(compensation_events_df, sh.compensation_events_sheet_id)

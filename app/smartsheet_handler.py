import os
from pathlib import Path
from dotenv import load_dotenv

import numpy as np
import pandas as pd
import smartsheet
from datetime import datetime

class handler:

    ### Define dependencies ###
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_PATH = BASE_DIR / ".env"
    load_dotenv(ENV_PATH)

    smartsheet_access_token = os.getenv("smartsheet_access_token")

    if not smartsheet_access_token:
        raise RuntimeError("smartsheet_access_token is not set")

    contracts_sheet_id = os.getenv("contracts_sheet_id")
    task_orders_sheet_id = os.getenv("task_orders_sheet_id")
    compensation_events_sheet_id = os.getenv("compensation_events_sheet_id")

    ### App ###
    smart = None

    def __init__(self):
        self.smart = smartsheet.Smartsheet(access_token=self.smartsheet_access_token, api_base="https://api.smartsheet.eu/2.0/")

    def  UpdateSheet(self, dataframe, sheet_id):
        # Get sheet
        sheet = self.smart.Sheets.get_sheet(sheet_id)

        # Extract column names from dataframe into an array
        columns = dataframe.columns.tolist()

        # Create an array of Smartsheet sheet's column IDs in same order as dataframe
        column_ids = []
        for column in columns:
            id = sheet.get_column_by_title(column).id
            column_ids.append(id)
        
        # Create new rows for upload, disregard cells containing arrays
        upload_rows = []
        for row in dataframe.itertuples(index=False):
            new_row = smartsheet.models.Row()
            new_row.to_bottom = True
            for col_id, value in zip(column_ids, row):
                if value != None:
                    if isinstance(value, (list, tuple)):
                        continue
                    else:
                        string = str(value) # Clean dataframe isn't working, intermediate fix
                        try:
                            dt = datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")
                            string = dt.strftime("%d/%m/%Y")
                        except:
                            None
                        new_row.cells.append({
                            'column_id': col_id,
                            'value': string, 
                            'strict': False
                        })
            upload_rows.append(new_row)

        # Upload new rows to sheet
        batch_size = 250

        upload_rows_count = len(upload_rows)
        for start in range(0, upload_rows_count, batch_size):
            end = min(start + batch_size, upload_rows_count)
            batch = upload_rows[start:end]
            self.smart.Sheets.add_rows(sheet_id, batch)        

        # Remove old rows from sheet
        delete_rows_ids = [row.id for row in sheet.rows]
        delete_rows_ids_count = len(delete_rows_ids)
        for start in range(0, delete_rows_ids_count, batch_size):
            end = min(start + batch_size, delete_rows_ids_count)
            batch = delete_rows_ids[start:end]
            self.smart.Sheets.delete_rows(sheet_id, batch, True)

        print(f"{sheet.name} sheet successfully updated")

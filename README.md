Instructions:
1. Install the relevant packages if you do not already have them:
    py -m pip install python-dotenv
    py -m pip install pandas
    py -m pip install requests
    py -m pip install numpy
    py -m pip install smartsheet-python-sdk

2. Obtain a CEMAR public and private key, as well as a Smartsheet access token.
3. Input these keys into the provided .env_template file.
4. Rename the .env_template file to .env.
5. Conduct your first run of the _main.py script. This will fail on the upload to Smartsheet because the sheets have not yet been created, but it will generate three CSV files:
    contracts.csv
    task_orders.csv
    compensation_events.csv

6. Upload these files to Smartsheet using the “Import Microsoft Excel…” method within a Smartsheet workspace. This will create the necessary sheets that the program will overwrite on each future upload.
7. From the uploaded sheets, extract their Sheet ID from the sheet properties and input these IDs into your .env file.
8. Future runs will now overwrite data directly into these sheets. CSV file creation can be commented out in the code if preferred.

Purpose of the program:
The purpose of this program is to batch extract, transform, and upload relevant contract data from CEMAR into Smartsheet, where it can be used for BI reporting, analysis, and data mirroring within a separate business environment. Only the mirroring of contracts, task orders, and compensation events has been scripted so far, as this is all that is currently required.

Data flow summary:
1. The program extracts every contract the user has access to within their CEMAR account in JSON format via the CEMAR API. This JSON data is then transformed into a pandas DataFrame, which is also made available as a CSV file.
2. In the subsequent data extraction scripts (task orders, etc.), the contracts DataFrame is used to navigate CEMAR using each contract ID.
3. Each subsequent API call uses this ID to access each contract’s data, extracting the required information in JSON format. During this process, each row has a new data point added — the contract ID it relates to — ensuring all data points can later be schema‑mapped. This data is then transformed into a pandas DataFrame and made available as a CSV file.
4. Once all extraction scripts have completed, the DataFrames are prepared for upload to the identified Smartsheet sheets using the Sheet ID.
5. The data is transformed into a Smartsheet‑compatible format. Transformations include:
    Creation of new row objects
    Creation of new cell objects within each row
        Cell objects are assigned values from the extracted CEMAR data
        DateTime values are reformatted into strings (Smartsheet reliably converts date‑like strings into date fields upon upload)
   
6. The row objects are uploaded in batches of 250. Old rows are then deleted in batches of 250. This ensures only recent data is retained. This upload method was chosen over creating new sheets or retaining old data to ensure:
    Sheet references relevant to the sheet are not broken or require reassignment
    Consistent uploads over time do not cause the sheet to exceed the 20,000‑row limit

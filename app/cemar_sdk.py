import requests

class sdk:

    base_url = "https://api.cemar.co.uk"

    session_token = None
    headers = None

    def DefineHeaders(self):
        self.headers = { 
            "Authorization" : f"Bearer {self.session_token}" 
        }

    # Authorization
    def InitialiseSession(self, public_key, private_key):
        url = f"{self.base_url}/authorization-api/connect/token"
        data = [
            ("grant_type", "client_credentials"),
            ("client_id", public_key),
            ("client_secret", private_key),
        ]
        response = requests.post(url, data=data)
        try:
            self.session_token = response.json()["access_token"]
            self.DefineHeaders()
        except:
            print("Error at InitialiseSession()")
            print(response.content)

    # Contracts
    def GetContracts(self, pageNumber, pageSize):
        url = f"{self.base_url}/contracts-api/v2/contracts"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetContractsList({pageNumber}, {pageSize})")
            print(response.content)

    # Compensation Events
    def GetCompensationEvents(self, contractId, pageNumber, pageSize):
        url = f"{self.base_url}/compensationevents-api/contract/{contractId}/compensationevents"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetCompensationEvents({contractId}, {pageNumber}, {pageSize})")
            print(response.content)

    # Task Orders
    def GetTaskOrders(self, contractId, pageNumber, pageSize):
        url = f"{self.base_url}/taskorders-api/contract/{contractId}/taskorders"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetTaskOrders({contractId}, {pageNumber}, {pageSize})")
            print(response.content)

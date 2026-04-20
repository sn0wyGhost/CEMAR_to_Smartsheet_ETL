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

    def GetContractPrice(self, contractId):
        url = f"{self.base_url}/contracts-api/v2/contracts/{contractId}/currentprice"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetContractPrice({contractId})")
            print(response.content)

    def GetContractUsers(self, contractId):
        url = f"{self.base_url}/contracts-api/contracts/{contractId}/users"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetContractPrice({contractId})")
            print(response.content)

    # Activities
    def GetActivitiesPrices(self, contractId, pageNumber, pageSize):
        url = f"{self.base_url}/activities-api/contract/{contractId}/activities"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetActivitiesPrices({contractId}, {pageNumber}, {pageSize})")
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

    def GetCompensationEvent(self, contractId, compensationEventId):
        url = f"{self.base_url}/compensationevents-api/contract/{contractId}/compensationevents/{compensationEventId}"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetCompensationEvent({contractId}, {compensationEventId})")
            print(response.content)

    def GetCompensationEventTypes(self, contractId):
        url = f"{self.base_url}/compensationevents-api/contract/{contractId}/compensationeventtypes"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetCompensationEventTypes({contractId})")
            print(response.content)

    # Defects ### UNTESTED ###
    def GetDefects(self, contractId, pageNumber, pageSize):
        url = f"{self.base_url}/defects-api/contract/{contractId}/defects"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetDefects({contractId}, {pageNumber}, {pageSize})")
            print(response.content)

    def GetDefectsCurrent(self, contractId, pageNumber, pageSize):
        url = f"{self.base_url}/defects-api/contract/{contractId}/defects/current"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetDefectsCurrent({contractId}, {pageNumber}, {pageSize})")
            print(response.content)

    def GetDefect(self, contractId, defectId):
        url = f"{self.base_url}/defects-api/contract/{contractId}/defects/{defectId}"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetDefect({contractId, defectId})")
            print(response.content)

    # Early Warnings ### UNTESTED ###
    def GetEarlyWarnings(self, contractId, pageNumber, pageSize):
        url = f"{self.base_url}/earlywarnings-api/contract/{contractId}/earlywarnings"
        params = {
            "pageNumber" : pageNumber,
            "pageSize" : pageSize
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return(response.json())
        except:
            print(f"Error at GetEarlyWarnings({contractId}, {pageNumber}, {pageSize})")
            print(response.content)

    def GetEarlyWarning(self, contractId, earlyWarningId):
        url = f"{self.base_url}/earlywarnings-api/contract/{contractId}/earlywarnings/{earlyWarningId}"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetEarlyWarning({contractId, earlyWarningId})")
            print(response.content)

    # Instructions (FIDIC)

    # Instructions (NEC)

    # Payment Assessments

    # Payments

    # Programmes

    # Quotations / Assessments

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

    def GetTaskOrder(self, contractId, taskOrderId):
        url = f"{self.base_url}/taskorders-api/contract/{contractId}/taskorders/{taskOrderId}"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetTaskOrder({contractId, taskOrderId})")
            print(response.content)

    def GetPriceList(self, contractId):
        url = f"{self.base_url}/taskorders-api/contract/{contractId}/pricelist"
        response = requests.get(url, headers=self.headers)
        try:
            return(response.json())
        except:
            print(f"Error at GetCompensationEventTypes({contractId})")
            print(response.content)

    # Technical Queries / Requests for Information

    # Variations

    # Organisations

    # Attachments

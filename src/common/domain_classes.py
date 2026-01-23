from dataclasses import dataclass

@dataclass
class OpenInvestmentAccountInput:
    client_id: str
    account_name: str
    initial_amount: float

@dataclass
class OpenInvestmentAccountOutput:
    account_created: bool = False
    message : str = None

@dataclass
class WealthManagementClient:
    first_name: str = None
    last_name: str = None
    address: str = None
    phone: str = None
    email: str = None
    marital_status: str= None
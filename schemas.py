from pydantic import BaseModel
from datetime import date

class PersonInput(BaseModel):
    documentTypeId: int
    documentNumber: str
    firstName: str
    lastName: str
    secondLastName: str
    gender: str
    maritalStatus: str
    birthdate: date

class PersonOutput(BaseModel):
    personId: int
    documentTypeId: int
    documentNumber: str
    firstName: str
    lastName: str
    secondLastName: str
    gender: str
    maritalStatus: str
    birthdate: date
    isCustomer: bool

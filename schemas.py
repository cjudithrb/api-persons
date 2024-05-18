from pydantic import BaseModel, constr
from datetime import date, datetime 

class DocumentType(BaseModel):
    id: int
    description: str

class DocumentTypeInput(BaseModel):
    id: int

class PersonInput(BaseModel):
    documentType: DocumentTypeInput
    documentNumber: constr(max_length=12)  # Limitar la longitud del número de documento
    firstName: constr(max_length=50)  # Limitar la longitud del nombre y requerir un mínimo de 2 caracteres
    lastName: constr(max_length=50)
    secondLastName: constr(max_length=50)
    gender: str
    maritalStatus: str
    birthdate: date

class PersonOutput(BaseModel):
    personId: int
    documentType: DocumentType
    documentNumber: str
    firstName: str
    lastName: str
    secondLastName: str
    gender: str
    maritalStatus: str
    birthdate: date
    isCustomer: bool
    registerDate: datetime

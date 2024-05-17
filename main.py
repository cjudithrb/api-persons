from fastapi import FastAPI, HTTPException, status
from typing import List
import mysql.connector
import schemas
import random
import uuid

app = FastAPI()

host_name = "34.236.117.148"  # Agrega el nombre del host de la base de datos
port_number = "8005"  # Agrega el número de puerto de la base de datos
user_name = "root"
password_db = "utec"
database_name = "bd_api_persons"  # Modifica el nombre de la base de datos

# Conexión a la base de datos
def connect_to_db():
    return mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )

# Obtener todas las personas
@app.get("/api/v1/person", response_model=List[schemas.PersonOutput])
def get_persons():
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Person")
    result = cursor.fetchall()
    mydb.close()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No persons found")
    
    persons = [schemas.PersonOutput(**dict(zip(schemas.PersonOutput.__fields__, person))) for person in result]
    
    return persons


# Obtener una persona por su ID
@app.get("/api/v1/person/{personId}", response_model=schemas.PersonOutput)
def get_person(personId: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Person WHERE personId = %s", (personId,))
    result = cursor.fetchone()
    mydb.close()
    if not result:
        trace_id = str(uuid.uuid4())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error-code": "ERR0003",
            "error-message": "Error, person not found",
            "trace-id": trace_id,
        })
    
    person_dict = dict(zip(schemas.PersonOutput.__fields__, result))
    return person_dict



# Agregar una nueva persona
@app.post("/api/v1/person", response_model=schemas.PersonOutput, status_code=status.HTTP_201_CREATED)
def add_person(item: schemas.PersonInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    is_customer = random.choice([True, False])
    sql = "INSERT INTO Person (documentTypeId, documentNumber, firstName, lastName, secondLastName, gender, maritalStatus, birthdate, isCustomer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (item.documentTypeId, item.documentNumber, item.firstName, item.lastName, item.secondLastName, item.gender, item.maritalStatus, item.birthdate, is_customer)
    cursor.execute(sql, val)
    mydb.commit()
    inserted_id = cursor.lastrowid
    mydb.close()
    return {**item.dict(), "personId": inserted_id, "isCustomer": is_customer}


# Modificar una persona por su ID
@app.put("/api/v1/person/{personId}", response_model=schemas.PersonOutput)
def update_person(personId: int, item: schemas.PersonInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # Verificar si el personId existe en la base de datos
    cursor.execute("SELECT COUNT(*) FROM Person WHERE personId = %s", (personId,))
    if cursor.fetchone()[0] == 0:
        trace_id = str(uuid.uuid4())
        raise HTTPException(
            status_code=404,
            detail={
                "error-code": "ERR0003",
                "error-message": "Error, person not found",
                "trace-id": trace_id,
            }
        )

    sql = "UPDATE Person SET documentTypeId=%s, documentNumber=%s, firstName=%s, lastName=%s, secondLastName=%s, gender=%s, maritalStatus=%s, birthdate=%s WHERE personId=%s"
    val = (item.documentTypeId, item.documentNumber, item.firstName, item.lastName, item.secondLastName, item.gender, item.maritalStatus, item.birthdate, personId)
    cursor.execute(sql, val)
    mydb.commit()

    # Obtener el valor de isCustomer de la base de datos
    cursor.execute("SELECT isCustomer FROM Person WHERE personId = %s", (personId,))
    is_customer = cursor.fetchone()[0]

    mydb.close()

    return {**item.dict(), "personId": personId, "isCustomer": is_customer}


# Eliminar una persona por su ID
@app.delete("/api/v1/person/{personId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(personId: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM Person WHERE personId = %s", (personId,))
    mydb.commit()
    if cursor.rowcount == 0:
        trace_id = str(uuid.uuid4())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error-code": "ERR0003",
            "error-message": "Error, person not found",
            "trace-id": trace_id,
        })
    return {"message": "Person deleted successfully"}

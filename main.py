from fastapi import FastAPI, HTTPException, status
from typing import List
from fastapi import Query
import mysql.connector
import schemas
import random
import uuid
import datetime

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
@app.get("/api/v1/persons", response_model=List[schemas.PersonOutput])
def get_persons():
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor()

        cursor.execute("""SELECT p.personId, d.documentTypeId, d.documentTypeName, p.documentNumber, p.firstName, p.lastName, 
                                 p.secondLastName, p.gender, p.maritalStatus, p.birthdate, p.isCustomer, p.registerDate
                          FROM Person p
                          INNER JOIN DocumentType d ON p.documentTypeId = d.DocumentTypeId
                          WHERE p.status = 'active'""")
        result = cursor.fetchall()

        if not result:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No persons found")

        persons = [schemas.PersonOutput(
            personId=person[0],
            documentType=schemas.DocumentType(id=person[1], description=person[2]),
            documentNumber=person[3],
            firstName=person[4],
            lastName=person[5],
            secondLastName=person[6],
            gender=person[7],
            maritalStatus=person[8],
            birthdate=person[9],
            isCustomer=person[10],
            registerDate=person[11].strftime("%Y-%m-%dT%H:%M:%S")
        ) for person in result]

        return persons

    except mysql.connector.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        if 'mydb' in locals():
            mydb.close()



@app.get("/api/v1/person", response_model=schemas.PersonOutput)
def get_person(personId: int = Query(..., description="ID of the person")):
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor()

        cursor.execute("SELECT p.personId, p.documentTypeId, dt.documentTypeName, p.documentNumber, p.firstName, p.lastName, p.secondLastName, p.gender, p.maritalStatus, p.birthdate, p.isCustomer, p.registerDate FROM Person p INNER JOIN DocumentType dt ON p.documentTypeId = dt.DocumentTypeId WHERE p.personId = %s AND p.status = 'active'", (personId,))
        result = cursor.fetchone()
        
        if not result:
            trace_id = str(uuid4())
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "error-code": "ERR0003",
                "error-message": "Error, person not found",
                "trace-id": trace_id,
            })

        person_output = schemas.PersonOutput(
            personId=result[0],
            documentType=schemas.DocumentType(id=result[1], description=result[2]),
            documentNumber=result[3],
            firstName=result[4],
            lastName=result[5],
            secondLastName=result[6],
            gender=result[7],
            maritalStatus=result[8],
            birthdate=result[9],
            isCustomer=result[10],
            registerDate=result[11].strftime("%Y-%m-%dT%H:%M:%S")
        )

        return person_output

    except mysql.connector.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        if 'mydb' in locals():
            mydb.close()


@app.post("/api/v1/person", response_model=schemas.PersonOutput, status_code=status.HTTP_201_CREATED)
def add_person(item: schemas.PersonInput):
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor()

        # Extraemos el documentTypeId del objeto documentType
        documentTypeId = item.documentType.id

        # Obtenemos la descripción del tipo de documento de la base de datos
        cursor.execute("SELECT documentTypeName FROM DocumentType WHERE DocumentTypeId = %s", (documentTypeId,))
        document_type_result = cursor.fetchone()
        if document_type_result is not None:
            document_type_description = document_type_result[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error-code": "ERR0005",
                    "error-message": "Error, invalid documentType",
                    "trace-id": str(uuid.uuid4())
                }
            )

        is_customer = random.choice([True, False])
        register_date = datetime.datetime.now()
        
        sql = """INSERT INTO Person (documentTypeId, documentNumber, firstName, lastName, secondLastName, gender, maritalStatus, birthdate, isCustomer, registerDate, status) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (documentTypeId, item.documentNumber, item.firstName, item.lastName, item.secondLastName, 
               item.gender, item.maritalStatus, item.birthdate, is_customer, register_date, 'active')
        
        cursor.execute(sql, val)
        mydb.commit()
        
        inserted_id = cursor.lastrowid

        person_output = schemas.PersonOutput(
            personId=inserted_id,
            documentType=schemas.DocumentType(id=documentTypeId, description=document_type_description),
            documentNumber=item.documentNumber,
            firstName=item.firstName,
            lastName=item.lastName,
            secondLastName=item.secondLastName,
            gender=item.gender,
            maritalStatus=item.maritalStatus,
            birthdate=item.birthdate,
            isCustomer=is_customer,
            registerDate=register_date.strftime("%Y-%m-%dT%H:%M:%S")
        )

        return person_output

    except mysql.connector.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        if 'mydb' in locals():
            mydb.close()



# Modificar una persona por su ID
@app.put("/api/v1/person")
def update_person(
    item: schemas.PersonInput,
    personId: int = Query(..., description="ID of the person to update")
):
    try:
        mydb = connect_to_db()
        cursor = mydb.cursor()

        # Verificar si el personId existe en la base de datos
        cursor.execute("SELECT COUNT(*) FROM Person WHERE personId = %s AND status = 'active'", (personId,))
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
        val = (item.documentType.id, item.documentNumber, item.firstName, item.lastName, item.secondLastName, item.gender, item.maritalStatus, item.birthdate, personId)
        cursor.execute(sql, val)
        mydb.commit()

        # Obtener el valor de isCustomer de la base de datos
        cursor.execute("SELECT isCustomer, registerDate FROM Person WHERE personId = %s", (personId,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

        is_customer = result[0]
        register_date = result[1]

        return {
            **item.dict(),
            "personId": personId,
            "isCustomer": is_customer,
            "registerDate": register_date.strftime("%Y-%m-%d %H:%M:%S") if register_date else None
        }

    except mysql.connector.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        if 'mydb' in locals():
            mydb.close()


# Eliminar logicamente una persona por su ID
@app.delete("/api/v1/person", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(personId: int = Query(..., description="ID of the person to delete")):

    mydb = connect_to_db()
    cursor = mydb.cursor()
    sql = "UPDATE Person SET status = %s WHERE personId = %s"
    val = ("inactive", personId)  # O cambia "inactive" al estado deseado
    cursor.execute(sql, val)
    mydb.commit()

    if cursor.rowcount == 0:
        trace_id = str(uuid.uuid4())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error-code": "ERR0003",
            "error-message": "Error, person not found",
            "trace-id": trace_id,
        })

    mydb.close()

    return {"message": "Person deleted successfully"}

# Eliminar fiscamente una persona por su ID
@app.delete("/api/v1/person/totallydelete", status_code=status.HTTP_204_NO_CONTENT)
def delete_person_fis(personId: int = Query(..., description="ID of the person to delete")):
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
    return {"message": "Person deleted totally successfully"}
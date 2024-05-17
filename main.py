from fastapi import FastAPI, HTTPException, status
import mysql.connector
import schemas

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
@app.get("/api/v1/person", response_model=list[schemas.PersonOutput])
def get_persons():
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Person")
    result = cursor.fetchall()
    mydb.close()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No persons found")
    return result

# Obtener una persona por su ID
@app.get("/api/v1/person/{id}", response_model=schemas.PersonOutput)
def get_person(id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Person WHERE personId = %s", (id,))
    result = cursor.fetchone()
    mydb.close()
    if not result:
        error_code = "ERR0017"
        error_message = "Error, codigo de empleado invalido"
        trace_id = str(uuid.uuid4())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error-code": error_code, "error-message": error_message, "trace-id": trace_id}
        )
    return result

# Agregar una nueva persona
@app.post("/api/v1/person", response_model=schemas.PersonOutput, status_code=status.HTTP_201_CREATED)
def add_person(item: schemas.PersonInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    is_customer = random.choice([True, False])  # Genera aleatoriamente True o False para isCustomer
    sql = "INSERT INTO Person (documentTypeId, documentNumber, firstName, lastName, gender, maritalStatus, birthdate, isCustomer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (item.documentTypeId, item.documentNumber, item.firstName, item.lastName, item.gender, item.maritalStatus, item.birthdate, is_customer)
    cursor.execute(sql, val)
    mydb.commit()
    inserted_id = cursor.lastrowid
    mydb.close()
    return {"personId": inserted_id, **item.dict()}

# Modificar una persona por su ID
@app.put("/api/v1/person/{id}", response_model=schemas.PersonOutput)
def update_person(id: int, item: schemas.PersonInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    sql = "UPDATE Person SET documentTypeId=%s, documentNumber=%s, firstName=%s, lastName=%s, gender=%s, maritalStatus=%s, birthdate=%s WHERE personId=%s"
    val = (item.documentTypeId, item.documentNumber, item.firstName, item.lastName, item.gender, item.maritalStatus, item.birthdate, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return {"personId": id, **item.dict()}

# Eliminar una persona por su ID
@app.delete("/api/v1/person/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM Person WHERE personId = %s", (id,))
    mydb.commit()
    mydb.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

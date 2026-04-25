# API REST de Personas con FastAPI y Docker

El repositorio **api-persons** de GitHub incluye un archivo `README.md` que describe cómo levantar una API de personas usando Python y Docker. A continuación se muestra el contenido completo del README.

---

## 📄 README del repositorio api-persons

# api-persons

Este proyecto implementa una API REST para gestionar información de personas utilizando **FastAPI** y una base de datos relacional.

## 🚀 Requisitos

* Python 3.9+
* FastAPI
* Uvicorn
* Docker

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/cjudithrb/api-persons.git
cd api-persons
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución local

Para correr la aplicación en modo desarrollo:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

http://127.0.0.1:8000

## 🐳 Ejecución con Docker

1. Construir la imagen:

```bash
docker build -t api-persons .
```

2. Ejecutar el contenedor:

```bash
docker run -d -p 8000:8000 api-persons
```

## 📑 Endpoints principales

* `GET /persons` → Lista todas las personas
* `GET /persons/{id}` → Obtiene una persona por ID
* `POST /persons` → Crea una nueva persona
* `PUT /persons/{id}` → Actualiza una persona existente
* `DELETE /persons/{id}` → Elimina una persona

## 🗄️ Base de datos

El archivo `scriptDB.sql` contiene la definición de la base de datos y tablas necesarias para la API.

## 📂 Estructura del proyecto

```
api-persons/
│── Dockerfile
│── README.md
│── main.py
│── schemas.py
│── scriptDB.sql
```

* **main.py**: Punto de entrada de la aplicación FastAPI.
* **schemas.py**: Define los modelos de datos (Pydantic).
* **scriptDB.sql**: Script para inicializar la base de datos.
* **Dockerfile**: Configuración para construir la imagen Docker.

## ✨ Autor

Creado por **cjudithrb**.

---

👉 Con este README puedes levantar la API tanto en tu entorno local como dentro de un contenedor Docker.

# Rabbit AI

Rabbit AI es un proyecto de prueba de concepto desarrollado con Django ASGI que explora las capacidades de los Model Context Protocols (MCPs) y la biblioteca Pydantic AI. Este proyecto permite la creación de prompts, la definición de estructuras de respuesta utilizando Pydantic, y la adición de información adicional a los prompts.

## Características principales

- **Creación de Prompts**: Permite a los usuarios crear prompts personalizados.
- **Estructuración de Respuestas**: Define la estructura de las respuestas utilizando Pydantic, asegurando validación y consistencia.
- **Proveedores Soportados**: Actualmente, el proyecto soporta los proveedores google, Ollama/Lmstudio y OpenAI.
- **Interfaz HTML**: Incluye una interfaz web básica para interactuar con el sistema, ubicada en el archivo `templates/index.html`.

## Tecnologías utilizadas

- **Django ASGI**: Framework web para manejar solicitudes asíncronas y sincronas.
- **Pydantic AI**: Biblioteca para la validación de datos y definición de estructuras de respuesta.
- **MCPs (Model Context Protocols)**: Protocolo para gestionar el contexto de los modelos.

## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

```
├── manage.py
├── pyproject.toml
├── README.md
├── handler/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── structure_tools.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── clients.py
│   │   ├── database.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── ...
├── rabbiat/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── templates/
│   ├── index.html
```

## Instalación y configuración

1. Clona este repositorio:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd rabbit_ai
   ```

2. Crea un entorno virtual:

   ```bash
   uv venv && source venv/bin/activate
   ```

2. Instala las dependencias:

   ```bash
   uv lock
   ```

3. Realiza las migraciones de la base de datos:

   ```bash
   python manage.py migrate
   ```

4. Inserta las variables de entorno que se ve en el fichero settings.py


5. Inicia el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

6. Accede a la interfaz web en `http://127.0.0.1:8000/`.

## Proveedores soportados

Por motivos de la prueba, este proyecto soporta únicamente los siguientes proveedores:

- **Google**
- **Ollama/Lmstudio**
- **OpenAI**

## Contribuciones

Este proyecto es una prueba de concepto y no está diseñado para producción. Sin embargo, las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Vista previa
![Vista previa de la interfaz web](static/image.webp)
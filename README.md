# 📖 CRUDApp - Sistema de Gestión (Productos y Proveedores)

Este es un sistema de escritorio completo para la gestión de inventario, desarrollado en Python con **PyQt5** y conectado a una base de datos **SQL Server**.

La aplicación permite a los usuarios registrarse, iniciar sesión y administrar dos módulos principales: **Productos** y **Proveedores**. Toda la lógica de negocio y la autenticación se manejan de forma segura a través de procedimientos almacenados en la base de datos.



## 🌟 Características Principales

* **Autenticación Segura:**
    * Sistema completo de **Login** y **Registro** de usuarios.
    * **Seguridad de Contraseñas:** Implementación de hashing `SHA2_512` + **Salting** (con `NEWID()`) directamente en SQL Server para proteger las credenciales del usuario. Las contraseñas en texto plano nunca se almacenan.

* **Módulo de Productos:**
    * **Gestión CRUD** completa (Crear, Leer, Actualizar, Eliminar).
    * Formularios dedicados para cada operación (Agregar, Actualizar, Eliminar, Buscar).
    * Consulta y visualización de todos los productos en una tabla.

* **Módulo de Proveedores:**
    * **Gestión CRUD** completa (Crear, Leer, Actualizar, Eliminar).
    * Lógica de negocio y UI separadas del módulo de productos.
    * Búsqueda de proveedores por nombre.

* **Base de Datos Robusta:**
    * Toda la lógica de negocio (CRUD, login, registro) se maneja a través de **Procedimientos Almacenados (Stored Procedures)**. Esto aumenta la seguridad (previene inyección SQL) y hace que la aplicación Python sea más mantenible.

* **Interfaz de Usuario Moderna:**
    * Interfaz de usuario creada con Qt Designer (`.ui`).
    * Ventana principal sin bordes con capacidad de movimiento.
    * Animación de **menú lateral deslizable** para la navegación.
    * Múltiples páginas gestionadas eficientemente mediante `QStackedWidget`.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Interfaz Gráfica (GUI):** PyQt5
* **Base de Datos:** SQL Server
* **Bibliotecas Clave de Python:**
    * `pyodbc`: Para la conexión nativa con SQL Server.

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Prerrequisitos

* Python 3.10 o superior
* SQL Server (Express, Standard, etc.)
* SQL Server Management Studio (SSMS)
* Git (opcional, para clonar)

### 2. Configuración de la Base de Datos

1.  **Crear la Base de Datos:**
    * Abre SSMS y conéctate a tu instancia de SQL Server.
    * Crea una nueva base de datos (ej. `CrudAppDB`).

2.  **Crear Tablas:**
    * Ejecuta los scripts SQL para crear las tablas:
        * `usuarios` (con `id_usuario`, `nombre_usuario`, `contrasena_hash`, `salt`).
        * `productos` (con `id_producto`, `clave`, `descripcion`, `existencia`, `precio`).
        * `proveedores` (con `id_proveedores`, `clave`, `nombre`, `telefono`, `direccion`, `email`).

3.  **Crear Procedimientos Almacenados (SPs):**
    * Ejecuta los scripts SQL para todos los Stored Procedures necesarios:
        * `sp_validar_usuario`
        * `sp_registrar_usuario`
        * `sp_insertar_producto`, `sp_buscar_productos`, `sp_actualizar_producto`, `sp_eliminar_producto`, `sp_listar_productos`.
        * `sp_insertar_proveedor`, `sp_buscar_proveedor` (por nombre), `sp_actualizar_proveedor`, `sp_eliminar_proveedor`, `sp_listar_proveedores`.

### 3. Configuración del Entorno de Python

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/maubtw/examen-segundo-parcial.git)
    cd examen-segundo-parcial
    ```

2.  **Crear un Entorno Virtual:**
    ```bash
    python -m venv venv
    ```

3.  **Activar el Entorno Virtual:**
    * En Windows (PowerShell/CMD):
        ```bash
        .\venv\Scripts\activate
        ```
    * En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Instalar Dependencias:**
    
    ```bash
    pip install -r requirements.txt
    ```

### 4. Configurar la Conexión

1.  Abre el archivo `modelo/conexiondb.py`.
2.  Modifica la variable `self.connection_string` con tus propias credenciales de SQL Server (servidor, nombre de la base de datos, usuario y contraseña).

### 5. Ejecutar la Aplicación

Una vez que la base de datos y el entorno estén configurados, ejecuta el archivo principal:

```bash
python main.py
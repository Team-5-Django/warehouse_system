# warehouse_system

## Getting Started
Follow these steps to set up and run the project on your local machine.

### Prerequisites
- Python installed (Recommended: Python 3.x)
- PostgreSQL installed and running
- Git installed

### Installation & Setup
1. Clone the repository
   git clone <git@github.com:Team-5-Django/warehouse_system.git>
   cd warehouse_system
   
2. Remove old migrations (except `__init__.py`)
   find . -path "*/migrations/*.py" ! -name "__init__.py" -delete

3. Create a PostgreSQL database and user
   ```sql
   CREATE DATABASE warehouse_db;
   CREATE USER warehouse_user WITH PASSWORD '123456';
   ALTER ROLE warehouse_user SET client_encoding TO 'utf8';
   ALTER ROLE warehouse_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE warehouse_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE warehouse_db TO warehouse_user;
   ```
   OR if using a different database, update `warehouse/settings.py` with your database credentials.

4. Apply migrations
    python manage.py makemigrations
    python manage.py migrate

5. Create a superuser (to access the admin panel)
        python manage.py createsuperuser
          ->  Follow the prompts to set up a username, email, and password.

6. Run the server
    cd warehouse
    python manage.py runserver

7. Access the application
   Open your browser and go to:
        http://127.0.0.1:8000/


### Additional Notes
- Ensure your PostgreSQL service is running before executing database commands.
- If you encounter permission issues, ensure your user has the necessary privileges.
- Consider using a virtual environment for dependency management.


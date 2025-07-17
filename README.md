# Django-Unchained

* Restful API server for Single Page Application (SPA) using Django
* Multi-tenant application working with Postgresql and gunicorn
* Pytest for unit testing, not with Django test
* Dockerized

## Setup (Without Docker)

1. 📋 Clone repository -> 
```git clone https://github.com/Anktw/django-unchained.git```

2. 📦 Install dependencies:
Note: virtualenv is strongly recommended.
``` python -m venv .venv```
```.\venv\Scripts\activate```(windows)
```source .venv/bin/activate```(Linux)
Then install dependencies:
```pip install -r requirements.txt```

3. 🔑 Setup environment variables -> rename env.example to .env and fill the values
```cp env.example .env```

4. 📊 Create a database in PostgreSQL.
using pgAdmin or by command line:
```psql -U postgres -c "CREATE DATABASE db_name;"```

5. 🏗️ Run migrations
```python manage.py makemigrations```
```python manage.py migrate```

If you mess up database tables for some reasons and would like to reset db, you can drop all tables by follow. You don't need to call the follow for test because reset_db and migrate are called every time pytest is executed.
```
$ python manage.py reset_db
```
and then make migrations.
```
6. 🧪 Run Tests
```pytest```

7. 🏃 Run the Development Server
```python manage.py runserver```

8. 🌐 Access the Application
Navigate to `http://localhost:8000/api/docs/` in your web browser to access the API documentation.

## Docker Setup

1. 🐳 Build and Run the Docker Containers
```docker-compose up --build```

2. 🌐 Access the Application
Navigate to `http://localhost:8000/api/docs/` in your web browser to access the API documentation.

3. 🧪 Run Tests in Docker
```docker-compose exec web pytest```

4. ✔️ Check Running Containers
```docker ps -a```

## Installed Packages



## API Endpoints

| Endpoint | Usage | Request | Auth Required |
| -------- | ----- | --------| ------------- |
| <sup><b>POST /api/v1/token/</b></sup> | Get access token and refresh token | email, password | False |
| <sup><b>POST /api/v1/token/refresh/</b></sup> | Refresh access token | refresh | True |
| <sup><b>POST /api/v1/token/verify/</b></sup> | Verify access token validity | N/A | True |
| <sup><b>POST /api/v1/token/revoke/</b></sup> | Revoke access token and refresh token | refresh | True |
| <sup><b>POST /api/v1/users/</b></sup> | Create user account | first_name, last_name, email, image, password, verification_code or invitation_code | True |
| <sup><b>GET /api/v1/users/\<int:id\>/</b></sup> | Get user data | N/A | True |
| <sup><b>PUT /api/v1/users/\<int:id\>/</b></sup> | Update user data | first_name and\/or last_name and\/or image | True |
| <sup><b>DELETE /api/v1/users/\<int:id\>/</b></sup> | Delete user account | N/A | True |
| <sup><b>PUT /api/v1/users/\<int:id\>/password/</b></sup> | Update user password | password, new_password | True |
| <sup><b>GET /api/v1/users/\<int:id\>/tenants/</b></sup> | Get associated tenant list | N/A | True |
| <sup><b>POST /api/v1/email/signup/verification/</b></sup> | Create email verification code and send signup link by email | email | False |
| <sup><b>POST /api/v1/password/reset-code/</b></sup> | Create password reset code and send reset link by email | email | False |
| <sup><b>POST /api/v1/password/reset/</b></sup> | Reset password with reset code | email, reset_code | False |
| <sup><b>POST /api/v1/tenants/</b></sup> | Create tenant | name, description | True |
| <sup><b>GET /api/v1/tenants/\<str:domain\>/</b></sup> | Get tenant data | N/A | True |
| <sup><b>POST /api/v1/tenants/\<str:domain\>/invitation-codes/</b></sup> | Create invitation code to tenant and send link by email | tenant_id, tenant_user_id, email | True |
| <sup><b>POST /api/v1/tenants/invited/</b></sup> | Get invited tenant data | email, invitation_code | True |
| <sup><b>GET /api/v1/tenants/\<str:domain\>/users/</b></sup> | Get tenant user list of tenant with specified domain | N/A | True |
| <sup><b>POST /api/v1/tenants/\<str:domain\>/users/</b></sup> | Create tenant user | tenant_id, user_id, invitation_code | True |
| <sup><b>GET /api/v1/tenants/\<str:domain\>/users/\<int:id\>/</b></sup> | Get tenant user data | N/A | True |


#### Table of Environmental Variables
| Variable Name | Definition | Example |
| ------------- | ---------- | ------- | 
| <sup><b>APP_NAME</b></sup> | Application name. Used description in email, for example. | 'My Web App' |
| <sup><b>APP_DOMAIN</b></sup> | URL of app | '`http://localhost:8000`' |
| <sup><b>TENANT_DOMAIN_LENGTH</b></sup> | Length of tenant domain which is an identifier of each tenant used internally. | 32 |
| <sup><b>TENANT_INVITATION_CODE_LENGTH</b></sup> | Length of secret code randomly generated which is used to invite user(s) to a tenant | 32 |
| <sup><b>TENANT_INVITATION_CODE_LIFETIME_MINS</b></sup> | If minutes of this value passed, invitation code expires. | 360 |
| <sup><b>TENANT_INVITATION_CODE_REQUEST_MAX_SIZE</b></sup> | This number of users can be invited at the same time. | 50 |
| <sup><b>DJANGO_DEBUG</b></sup> | The same as Django build-in DJANGO_DEBUG flag. | True |
| <sup><b>DJANGO_SECRET_KEY</b></sup> | Secret key used to identify running Django application. | some-random-letters-hard-to-guess |
| <sup><b>POSTGRES_HOST</b></sup> | IP address of server where docker container for postgres runs. | 'localhost' |
| <sup><b>POSTGRES_CONTAINER_NAME</b></sup> | Docker container name for postgres service. | postgres_server_dev |
| <sup><b>POSTGRES_DB</b></sup> | Used DB name of postgres. | postgres_db_dev |
| <sup><b>POSTGRES_HOST_PORT</b></sup> | Port used for postgres docker container. | 5432 |
| <sup><b>POSTGRES_USER</b></sup> | User name for postgres. | user_dev |
| <sup><b>POSTGRES_PASSWORD</b></sup> | Password of postgres. | secret_password_hard_to_guess |
| <sup><b>POSTGRES_MOUNTED_VOLUME</b></sup> | Relative path to directory mounted to postgres docker container. | ./data/postgres_dev |
| <sup><b>DJANGO_TEMPLATE_DIR</b></sup> | Path to directory containing index.html. Relative to parent directory of root directory of this project. | vue-root-dir/dist/ |
| <sup><b>DJANGO_STATIC_DIR</b></sup> | Path to directory containing static files(css, js files). Relative to parent directory of root directory of this project. | vue-root-dir/dist/static/ |
| <sup><b>ACCESS_TOKEN_LIFETIME_MINS</b></sup> | Access token expires in this minutes. | 30 |
| <sup><b>REFRESH_TOKEN_LIFETIME_DAYS</b></sup> | Access token expires in this days. | 30 |
| <sup><b>UPDATE_LAST_LOGIN</b></sup> | If true, last_login data in users table is recorded. | True |
| <sup><b>EMAIL_VERIFICATION_CODE_LENGTH</b></sup> | Length of code randomly generated, which is used to verify email. | 32 |
| <sup><b>EMAIL_VERIFICATION_CODE_LIFETIME_MINS</b></sup> | If this minutes passed, email verification code expires. | 30 |
| <sup><b>EMAIL_BACKEND</b></sup> | Backend to send email. | django.core.mail.backends.smtp.EmailBackend |
| <sup><b>EMAIL_HOST</b></sup> | URL of used email server. | smtp.gmail.com (If use gmail.) |
| <sup><b>EMAIL_HOST_USER</b></sup> | Email address of sender. | `sender.my.awesome.app@xyz.xyz` |
| <sup><b>EMAIL_HOST_PASSWORD</b></sup> | Password of used email address. | secret-password-hard-to-guess |
| <sup><b>EMAIL_PORT</b></sup> | Port used by email server. | 587 |
| <sup><b>EMAIL_USE_TLS</b></sup> | Flag to indicate use of TLS. | True |
| <sup><b>MEDIA_ROOT</b></sup> | Directory name used to store media data(files). | media |
| <sup><b>MEDIA_URL</b></sup> | Relative path starting with '/' and ending with '/' to directory to store media data. | /media/ |
| <sup><b>PASSWORD_RESET_CODE_LENGTH</b></sup> | Length of code randomly generated, which is used to reset user password. | 32 |
| <sup><b>PASSWORD_RESET_CODE_LIFETIME_MINS</b></sup> | Password reset code expires if this minutes passed. | 30 |


## Directory Structure

### Clearning up database
You may need to delete directory mounted to postgres docker container, especially when you clean up all relevant docker containers to start over the setup.
```
Eg.)
$ sudo rm -r ./data/postgres_dev
```
Or you may like to clear all record in db and reset sequences as well. In the case drop all tables and rebuild tables again.
```
$ python manage.py reset_db
$ python manage.py migrate
```
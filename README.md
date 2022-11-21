<h1 align="center"> ms-user-candidate </h1> <br>

## Table of Contents

- [Create virtualenv & Install modules](#create-virtualenv--install-modules)
- [How to build & How to run](#how-to-build--how-to-run)
- [API](#api)

## Create virtualenv & Install modules

**With `poetry`**

```shell
poetry shell
poetry install
```

**Or without `poetry`**

```shell
python3 -m venv .venv
source .venv/bin/activate # (for windows use  ->  $.venv\Scripts\activate.bat)
pip install -r requirements.txt
```

Generate requirements.txt

```shell
poetry export -f requirements.txt --output requirements.txt
```

## How to build & How to run

**with `Docker Compose`**

The following command automatically prepare MongoDB and FastAPI service to run

```shell
docker-compose up -d
```

**without `Docker Compose`**

You should have MongoDB server and put configs of it to ".dev.env" file

```shell
source .dev.env
uvicorn app.main:app --host localhost --port 8000 --reload
```

## How to use

You can reach to service with the URL: "<http://localhost:8000/ms-user-candidate/>*"

When the service starts the first time, it will create the default user and password, then print them to the terminal.

Please login with the default user/password via /ms-user-candidate/login endpoint, get the access token from the response, and use in headers the token when sending requests to other APIs

## API

# ms-user-candidate endpoints

<details>
<summary>ENDPOINTS</summary>

- #### Create access and refresh tokens for user

    <details>
    <summary>/ms-user-candidate/login - HTTP POST:
    Form data:
        *username: realhuseynli@gmail.com
        *password: 12345678
    </summary>

    Status Code: 200 OK

    ```json
        {
           "access_token": "XXXX",
           "refresh_token": "XXXX"
        }
    ```

    Status Code: 400 Bad request

    ```json
        {
           "detail": "Incorrect email or password"
        }
    ```

    </details>

- #### Create a new user

    <details>
    <summary>/ms-user-candidate/user - HTTP POST:
    Form data:
        *first_name: Real
        *last_name: Huseyn
        *email: realhuseynli@gmail.com
        *password: 12345678
    Header:
        *Authorization: Bearer some_jwt_token
    </summary>

    Status Code: 201 Created

    ```json
        {
         "uuid": "60012b84-5d86-48dd-9f65-6a056a7a02be",
         "first_name": "Real",
         "last_name": "Huseyn",
         "email": "realhuseynli@gmail.com",
         "password": "$2b$12$2rcTbeXwqkAfxdxoTfRxvekwcREEtIKuP4UiNvZIYNV81ibAP80JG"
        }
    ```

    Status Code: 400 Bad request

    ```json
        {
           "detail": "User with this email already exist"
        }
    ```

    Status Code: 403 Forbidden

    ```json
        {
           "detail": "Could not validate credentials"
        }
    ```

    </details>

**You can find other APIs on the swagger: "http://localhost:8000/docs"**
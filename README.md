An Address book APIs using Fast API python.

## Preconditions:

- Python 3

## Clone the project

```
git clone https://github.com/Akashlv7/address-book-fastapi
```

## Run local

## Create and Activate virtual environment
```
https://www.geeksforgeeks.org/python-virtual-environment/
```

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
uvicorn controller:app --reload
```

### Reset Database

```
Delete the address_book.db file to reset DB and start fresh
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```

## List of API routes

```
1. Get all addresses present in the address book
        Method: GET
        API: http://127.0.0.1:8000/getAllAddresses

2. Get address by name
        Method: GET
        API: http://127.0.0.1:8000/getAddress/<name>

3. Get address within the range
        Method: GET
        API: http://127.0.0.1:8000/getAddressWithinRange/<range>/<location>
        *Range in kilometers

        Eg: http://127.0.0.1:8000/getAddressWithinRange/100/72.85,85.26

4. Add address
        Method: POST
        API: http://127.0.0.1:8000/createAddress
        Body: {
                "address_name": "station",
                "location": "10.85, 18.28"
            }

5. Update address by name
        Method: PUT
        API: http://127.0.0.1:8000/updateAddress
        Body: {
                "address_name": "station",
                "location": "10.85, 18.28"
            }

6. Delete address by name
        Method: DELETE
        API: http://127.0.0.1:8000/deleteAddress/<name>
```
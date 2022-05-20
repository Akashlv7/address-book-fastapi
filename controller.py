from urllib import response
from fastapi import FastAPI

from pydantic import BaseModel
from typing import Optional

from models import Address

app = FastAPI (
    title = "Address Book API",
    description = "Adds, updates, deletes Addresses.",
    version = "1.0",
)

class UserAddress(BaseModel):
    address_name: Optional[str] = None
    location: Optional[str] = None


############################################### GET ALL ADDRESSES ###############################################

@app.get("/getAllAddresses")
async def getAllAddresses():
    """Get all addresses API endpoint
    """
    addresses_from_db = Address.get_address()
    response = list()

    if not addresses_from_db:
        return "No Addresses found in the Book"

    for each_address in addresses_from_db:
        each_user_address = {
                            "address_name": each_address[0],
                            "location": {
                                            "latitude": each_address[1],
                                            "longitude": each_address[2],
                            }
                            
        }
        response.append(each_user_address)
    return response

############################################### GET ADDRESS BY ID ###############################################

@app.get("/getAddress/{address_name}")
async def getAddressByname(address_name: str):
    """Get address by name API endpoint
    """
    addresses_from_db = Address.get_address(query_address_name = address_name)
    if addresses_from_db:
        response_data = {
                            "address_name": addresses_from_db[0][0],
                            "location": {
                                            "latitude": addresses_from_db[0][1],
                                            "longitude": addresses_from_db[0][2],
                            }
                            
        }
        return response_data
    return "No Data Found for the given address name"

############################################### GET ADDRESSES WITHIN RANGE ###############################################

@app.get("/getAddressWithinRange/{range}/{location}")
async def getAddressWithinRange(range: int, location: str):
    """Get address within range API endpoint
    """
    addresses_from_db = Address.get_address_in_range(range, location)
    response = list()

    if not addresses_from_db:
        return "No Address found within the range"

    for each_address in addresses_from_db:
        each_user_address = {
                            "address_name": each_address[0],
                            "location": {
                                            "latitude": each_address[1],
                                            "longitude": each_address[2],
                            }
                            
        }
        response.append(each_user_address)
    return response

############################################### CREATE/ADD ADDRESS ###############################################

@app.post("/createAddress")
async def addAddress(address: UserAddress):
    """Create/Add address API endpoint
    """
    location = address.location.split(",")
    validation_response =  validate_address(location[0], location[1])
    if validation_response != 1002:
        return validation_response

    try:
        location = address.location.split(",")

        try:
            address_table = Address(address.address_name, location[0], location[1])
            add_response = address_table.add_address()
        except Exception as err:
            return str(err)
    
        if add_response == 1000:
            return "Address ID already exists - Please Enter the Unique Address Name"

        if add_response == 1001:
            return "Address already exists - Same location already present"

        return "User Address added successfully"

    except Exception as err:
        return err

############################################### UPDATE ADDRESS ###############################################

@app.put("/updateAddress")
async def updateAddress(address: UserAddress):
    """Update address API endpoint
    """
    try:
        location = address.location.split(",")

        try:
            address_table = Address(address.address_name, location[0], location[1])
            update_response = address_table.update_address()
            print(update_response)
        except Exception as err:
            raise

        if update_response == 1003:
            return "Address not found"

        if update_response == 1000:
            return "Address Name not found"

        if update_response == 1001:
            return "Address already exists - Same location already present"

        return "User Address updated successfully"

    except Exception as err:
        return str(err)
    
############################################### DELETE ADDRESS ###############################################

@app.delete("/deleteAddress/{address_name}")
async def deleteAddressByName(address_name: str):
    """Delete Address by name API endpoint
    """
    try:
        if not Address.delete_address(query_address_name = address_name):
            return "Address ID does not exist - Please Enter a valid address name"

        return "Successfully deleted the address"

    except Exception as err:
        return str(err)


#############################################################################################################


def validate_address(latitude, longitude):
    """ The latitude value should be within range of -90 to +90 degress
        The longiutude value should be within range of -180 to +180 degress
    """
    
    #Latitude Check
    if float(latitude) < -90 or float(latitude) > 90:
        return "Enter a Valid location - Latitude is out of range"

    #Longitude Check
    if float(longitude) < -180 or float(longitude) > 180:
        return "Enter a Valid location - Longitude is out of range"


    return 1002




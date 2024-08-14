from passlib.context import CryptContext
from passlib.exc import UnknownHashError



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash(password: str) -> str:
    return pwd_context.hash(password)



# TO COMPARE HASHED PASSWOD OF DB TO PLAIN PASSWORD ENTERED BY THE USER, WE ARE CONVERTING THE PLAIN 
# PASSWORD TO HASH AND THEN COMPARING BOTH hash 



def verify(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        raise ValueError("The hashed password format is unknown or not supported.")
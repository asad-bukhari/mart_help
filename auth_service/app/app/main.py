from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

ALGORITHM = "HS256"
SECRET_KEY = " A Secure Secret Key"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
fake_users_db: dict[str, dict[str, str]] = {
    "asad": {
        "username": "asad",
        "full_name": "Asad Zaib",
        "email": "ameenalam@example.com",
        "password": "122192",
    },
    "mjunaid": {
        "username": "mjunaid",
        "full_name": "Muhammad Junaid",
        "email": "mjunaid@example.com",
        "password": "mjunaidsecret",
    },
}



def create_access_token(subject: str, exipres_delta: timedelta) ->str:
    expire = datetime.utcnow() + exipres_delta
    to_encode = {"exp":expire,"sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_jwt

@app.get("/")
def read_root():
    return {"message" : "Hello World"}

@app.get("/new_route")
def get_access_token(user_name:str):
    access_token_expires = timedelta(minutes=50)
    access_token = create_access_token(subject=user_name, exipres_delta=access_token_expires)
    return {"access_token": access_token}


    
@app.get("/decode_token")
def decoding_token(access_token: str):
    """
    Understanding the access token decoding and validation
    """
    try:
        decoded_token_data = decode_access_token(access_token)
        return {"decoded_token": decoded_token_data}
    except JWTError as e:
        return {"error": str(e)}
    



@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    """
    Understanding the login system
    -> Takes form_data that have username and password
    """
    user_in_fake_db = fake_users_db.get(form_data.username)
    if not user_in_fake_db:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if not form_data.password == user_in_fake_db["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token_expires = timedelta(minutes=60)

    access_token = create_access_token(
        subject=user_in_fake_db["username"], exipres_delta= access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires.total_seconds() }


@app.get("/users/me")
def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    user_token_data = decode_access_token(token)
    
    user_in_db = fake_users_db.get(user_token_data["sub"])
    
    return user_in_db
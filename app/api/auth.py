from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import os
from app.core.database import get_db
from dotenv import load_dotenv 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.models.Location import DeliveryTracking,LocationTrack
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from app.schemas.Location import LocationRequest
from app.models.User import User ,Client, DeliveryPerson, Restaurant, Admin
from app.schemas.User import UserInDB,BeDelivery,DeliveryRole ,Token, UserLogin,UserUpdate,UserOut,EmailRequest


security = HTTPBearer()
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

EMAIL_USER=os.getenv("EMAIL_USER")
PASS_USER= os.getenv("EMAIL_PASS")

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----- Helpers -----
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = None):
    """Génère un JWT pour ton application"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_activation_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=30)

    activation_token=jwt.encode(
        {
            "sub": email,
            "type": "activation",
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return activation_token


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        print(f"JWT Error: {str(e)}") # Log the error on the server
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication error")


def build_activation_email(name: str, link: str):
    return f"""
    <html>
      <body style="font-family: Arial; background:#f4f4f4; padding:20px;">
        <div style="max-width:500px;margin:auto;background:white;padding:20px;border-radius:10px;">
          
          <h2 style="color:#1d4ed8;">Activate your account</h2>

          <p>Hi <b>{name}</b>,</p>

          <p>Thank you for signing up. Please click the button below to activate your account:</p>

          <a href="{link}" 
             style="
               display:inline-block;
               padding:12px 20px;
               background:#1d4ed8;
               color:white;
               text-decoration:none;
               border-radius:8px;
               margin-top:10px;
             ">
             Activate Account
          </a>

          <p style="margin-top:20px;font-size:12px;color:gray;">
            If you didn’t request this, ignore this email.
          </p>

        </div>
      </body>
    </html>
    """


def send_activation_email(name: str,to_email:str,token:str):
    activation_link = f"http://localhost:3000/auth/signup/verify?token={token}"
    html_content = build_activation_email(name, activation_link)

    msg = MIMEText(html_content, "html")
    msg["Subject"]="Activate your account"
    msg["From"]=os.getenv("EMAIL_USER")
    msg["To"]=to_email
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(EMAIL_USER,PASS_USER)
        server.send_message(msg)
   
   
@auth_router.post("/set-rights")
def set_rights(db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user["user_id"]).first()
    db_user.rights = 1
    db.commit()
    return {"message": "Rights enabled"}
   


        
# ----- Login -----
@auth_router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.active != 1:
        raise HTTPException(status_code=403, detail="Account not activated")
    token = create_access_token({
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role,
        "firstname": db_user.firstname,
        "lastname": db_user.lastname
    })
    return {"access_token": token, "token_type": "bearer","user_id": db_user.id }


# ----- Register -----
@auth_router.post("/register")
def register(user: UserInDB, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hash_password(user.password),

        phone=user.phone,
        address=user.address,

        role=user.role or "client",
        active=0,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token=create_activation_token(new_user.email)
    send_activation_email(new_user.firstname,new_user.email,token)
    return {"message": "User created successfully", "user_id": new_user.id,"token":token}


@auth_router.put("/be_delivery_person")
def be_delivery_person(
    data: BeDelivery,
    id_user: int,
    db: Session = Depends(get_db)
):

    # check user exists
    client = db.query(User).filter(User.id == id_user).first()

    if not client:
        raise HTTPException(status_code=404, detail="User not found")

    # check if already delivery person
    existing_delivery = db.query(DeliveryPerson).filter(
        DeliveryPerson.user_id == id_user
    ).first()

    if existing_delivery:
        raise HTTPException(
            status_code=400,
            detail="Delivery person already exists"
        )

    # update role
    client.role = "delivery_person"

    # create delivery person
    new_delivery_person = DeliveryPerson(
        user_id=id_user,
        vehicle_type=data.vehicle_type,
        birth_date=data.birth_date,
        available=data.available,
    )

    db.add(new_delivery_person)

    db.commit()
    db.refresh(new_delivery_person)

    return {
        "message": "User became delivery person successfully",
        "delivery_person": new_delivery_person
    }



@auth_router.get("/activate")
def activate_account(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "activation":
            raise HTTPException(status_code=400, detail="Invalid token")

        email = payload["sub"]

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.active = 1
        db.commit()

        return {"message": "Account activated successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    
    
@auth_router.post("/resend-activation")
def resend(data: EmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(404, "User not found")

    token = create_activation_token(user.email)
    send_activation_email(user.firstname, user.email, token)

    return {"message": "Activation email sent"}


# ----- Update -----
@auth_router.put("/update_user/{user_id}")
def update_user(user_id: int,user: UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not exists")
    
    existing_user.firstname=user.firstname
    existing_user.lastname=user.lastname
    existing_user.email=user.email
    existing_user.password=hash_password(user.password)
    existing_user.phone=user.phone
    existing_user.address=user.address
    existing_user.role=user.role or "client"
    existing_user.active=user.active

    existing_user.updated_at=datetime.utcnow()
    db.commit()
    db.refresh(existing_user)
    
    return {"message": "User updated successfully", "user_id": existing_user.firstname}


@auth_router.get("/me", response_model=UserOut)
def get_me(db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_id = user["user_id"]  # ← JWT stores it as "user_id" not "id"
    existing = db.query(User).filter(User.id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return existing


@auth_router.post("/logout")
def logout():
    return {"message": "Logged out"}


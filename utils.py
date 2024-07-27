from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import PyJWTError
import jwt
from settings import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

class PasswordUtils:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        return PasswordUtils.pwd_context.verify(raw_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return PasswordUtils.pwd_context.hash(password)
    
class EmailUtils:
    @staticmethod
    def send_email(to_email: str, from_email: str = settings.EMAIL_ADDRESS, password: str = settings.EMAIL_PASSWORD,registration_data=None,Subject=None,body=None) -> None:
        """Send an email using SMTP."""
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = Subject
        if body ==None:
            body=f"your login details are\n{registration_data}"
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            
            server.login(from_email, password)
            
            server.sendmail(from_email, to_email, msg.as_string())
            
            server.quit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

class JWTUtils:
    SECRET_KEY = settings.SECRET_KEY 
    ALGORITHM = settings.ALGORITHM

    @staticmethod
    def encode_jwt(payload: dict) -> str:
        if "exp" not in payload:
            payload["exp"] = datetime.utcnow() + timedelta(hours=1)
        encoded_jwt = jwt.encode(payload, JWTUtils.SECRET_KEY, algorithm=JWTUtils.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_payload = jwt.decode(token, JWTUtils.SECRET_KEY, algorithms=[JWTUtils.ALGORITHM])
        except PyJWTError:
            raise HTTPException(detail="Invalid JWT Token", status_code=401)
        return decoded_payload
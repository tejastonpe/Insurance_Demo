from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env")
    #Database
    DB_URL:str

    #JWT
    SECRET_KEY:str
    ALGORITHM:str

    #email
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

settings=Settings()
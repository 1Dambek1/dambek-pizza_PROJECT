from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
class DbConfig(BaseSettings):
 DATABASE_URL:str

 model_config = SettingsConfigDict(env_file= ".env.test",extra="ignore")

class AuthConfig(BaseSettings):
 ALGORITHM:str
 SECRET_KEY:str

 model_config = SettingsConfigDict(env_file= ".env.test",extra="ignore")


class Config(BaseModel):
 db_config:DbConfig = DbConfig()
 auth_config:AuthConfig =AuthConfig()



config = Config()

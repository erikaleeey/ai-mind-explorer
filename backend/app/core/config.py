from pydantic_settings import BaseSettings # type: ignore
from pydantic import SecretStr, field_validator, ConfigDict
from typing import Optional
import os

"""
config.py uses Pydantic Settings to create a centralized,
  validated configuration system that loads from environment
  variables and .env files.

  basesettings auto loads from env variables
  also loads from .env files

"""


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    # API Settings, default values for development, can be overriden with env vars
    api_title: str = "CSO Knowledge System"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Security settings
    secret_key: SecretStr #no default, this must be provided, never logs or prints actual value
    algorithm: str = "HS256" #JSON web token signing algorithm
    access_token_expire_minutes: int = 30
    
    # Database URLs, all required 
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: SecretStr
    postgres_url: str
    redis_url: str
    
    # Environment, set in .env file 
    environment: str = "development"

    # Feature flags (default OFF)
    enable_graph: bool = False
    
    @field_validator("environment")
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError("Invalid environment")
        return v
    
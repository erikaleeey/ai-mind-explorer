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
    model_config = ConfigDict(env_file="../.env", case_sensitive=False)

    # API Settings, default values for development, can be overriden with env vars
    api_title: str = "AI Mind Explorer"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Security settings
    secret_key: SecretStr = SecretStr("dev-secret-key-change-in-production")  # Default for development
    algorithm: str = "HS256" #JSON web token signing algorithm
    access_token_expire_minutes: int = 30

    # Database URLs, all required 
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: SecretStr

    # Database URLs
    #neo4j_uri: str = "neo4j://localhost:7687"
    #neo4j_user: str = "neo4j"
    #neo4j_password: SecretStr = SecretStr("password")

    # AI API Keys
    openai_api_key: Optional[SecretStr] = None
    anthropic_api_key: Optional[SecretStr] = None
    gemini_api_key: Optional[SecretStr] = None

    # Environment, set in .env file
    environment: str = "development"

    # CORS Origins
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    @field_validator("environment")
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError("Invalid environment")
        return v
    
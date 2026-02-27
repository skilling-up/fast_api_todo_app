"""
Configuration management for the application using Pydantic Settings.

This module defines the Settings class, which loads environment variables
from a .env file and provides typed access to configuration values,
including dynamically constructed database URLs.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from urllib.parse import quote_plus 

class Settings(BaseSettings):
    """
     Application settings loaded from environment variables.

    The class automatically reads values from a .env file (or system environment)
    and constructs the full database URLs for both main and test databases.

    Attributes:
        db_user (str): Database username.
        db_pass (str): Database password.
        db_host (str): Database host address.
        db_port (int): Database port number.
        db_name (str): Name of the main database.
        db_name_test (str): Name of the test database.
        database_url (str): Full asynchronous PostgreSQL URL for the main database (computed).
        test_database_url (str): Full asynchronous PostgreSQL URL for the test database (computed).
    """
    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str



    db_name_test: str

    @computed_field
    def database_url(self) -> str:
        safe_pass = quote_plus(self.db_pass)
        return f"postgresql+asyncpg://{self.db_user}:{safe_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @computed_field
    def test_database_url(self) -> str:
        safe_pass = quote_plus(self.db_pass)
        return f"postgresql+asyncpg://{self.db_user}:{safe_pass}@{self.db_host}:{self.db_port}/{self.db_name_test}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

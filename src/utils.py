"""
Utility functions for the chatbot application.
"""

import os
from dotenv import load_dotenv


def load_environment_variables():
    load_dotenv()


def get_api_key(key_name: str) -> str:
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in environment variables. Please check your .env file.")
    return api_key


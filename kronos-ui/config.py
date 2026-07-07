import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "kronos-dev-key-change-in-prod")

    DB_BACKEND = os.getenv("KRONOS_DB_BACKEND", "sqlite")

    if DB_BACKEND == "postgresql":
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "postgresql://localhost:5432/kronos",
        )
    elif DB_BACKEND == "snowflake":
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "snowflake://{user}:{password}@{account}/{database}/{schema}".format(
                user=os.getenv("SNOWFLAKE_USER", ""),
                password=os.getenv("SNOWFLAKE_PASSWORD", ""),
                account=os.getenv("SNOWFLAKE_ACCOUNT", ""),
                database=os.getenv("SNOWFLAKE_DATABASE", "KRONOS"),
                schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
            ),
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///kronos.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

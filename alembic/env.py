import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Read settings YAML file
from pathlib import Path  # noqa: E402
from yaml import safe_load  # noqa: E402
import os  # noqa: E402

app_settings_path = os.getenv("CONFIG", "config/config.dev.yaml")
app_settings = safe_load(Path(app_settings_path).read_text())
# get database uri from settings.yaml
config.set_main_option("sqlalchemy.url", app_settings["database"]["url"])

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from babyhelm.models import Base  # noqa F402

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


DATABASE_URL = context.config.get_main_option("sqlalchemy.url")

# Create asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


# Define a method to run migrations
async def run_migrations_online():
    # Connect to the database
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


# Define a method to run the migrations
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()


# Run the asynchronous migration runner
if context.is_offline_mode():
    context.configure(url=DATABASE_URL)
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(run_migrations_online())

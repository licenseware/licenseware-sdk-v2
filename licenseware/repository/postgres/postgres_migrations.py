import os

from alembic import command as alembic_run
from alembic.config import Config


class PostgresMigrations:
    def __init__(self, db_url: str, target_metadata):

        # print(target_metadata)
        # print(dir(target_metadata))
        # print(vars(target_metadata))
        # self.target_metadata = target_metadata # TODO - integrate env.py from migrations here

        self.db_url = db_url
        self.cfg = Config("alembic.ini")

    def create_alembic_ini(self):

        # alembic.ini
        default_url = "sqlalchemy.url = driver://user:pass@localhost/dbname"
        # alembic_ini_path = os.path.join(os.getcwd(), 'migrations', 'alembic.ini')
        # os.replace(os.path.join(os.getcwd(), 'alembic.ini'), alembic_ini_path)
        alembic_ini_path = "alembic.ini"

        with open(alembic_ini_path, "r") as f:
            alembic_ini_data = f.read()

        if default_url in alembic_ini_data:

            alembic_ini_data = alembic_ini_data.replace(
                default_url, f"sqlalchemy.url = {self.db_url}"
            )

            alembic_ini_data = alembic_ini_data.replace(
                "# path to migration scripts", "version_locations = ./local_migrations"
            )

            alembic_ini_data = alembic_ini_data.replace(
                "version_path_separator = os  # default: use os.pathsep",
                "version_path_separator = ;",
            )

            with open(alembic_ini_path, "w") as f:
                f.write(alembic_ini_data)

    def create_migration_files(self):

        # Create folder local_migrations
        local_migrations = os.path.join(os.getcwd(), "local_migrations")
        if not os.path.exists(local_migrations):
            os.makedirs(local_migrations)

        # Create migrations folder and alembic.ini file
        if not os.path.exists("migrations"):
            alembic_run.init(self.cfg, "migrations")

    def add_target_metadata_to_env_file(self):

        env_path = os.path.join("migrations", "env.py")

        with open(env_path, "r") as f:
            env_data = f.read()

        example_import = "# from myapp import mymodel"

        if example_import not in env_data:
            return

        env_data = env_data.replace(example_import, "from main import db")
        env_data = env_data.replace(
            "target_metadata = None", "target_metadata = db.Base.metadata"
        )

        with open(env_path, "w") as f:
            f.write(env_data)

    def migrate(self):

        alembic_run.stamp(self.cfg, "head")
        alembic_run.revision(self.cfg, message="rev", autogenerate=True)
        # alembic_run.upgrade(self.cfg, revision='new')

    def make_migrations(self):

        self.create_migration_files()
        self.create_alembic_ini()
        self.add_target_metadata_to_env_file()
        self.migrate()

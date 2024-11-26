from alembic.config import Config
from alembic.command import check, revision, upgrade
from alembic.util import AutogenerateDiffsDetected


config = Config("alembic.ini")

if __name__ == '__main__':
    try:
        check(config)
    except AutogenerateDiffsDetected:
        revision(config=config, autogenerate=True)
        upgrade(config=config, revision="head")


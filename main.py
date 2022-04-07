from db_repo import DbRepo
from db_config import local_session, create_all_entities

repo = DbRepo(local_session)

repo.drop_all_tables()
create_all_entities()
repo.reset_db()
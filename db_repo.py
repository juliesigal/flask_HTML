from Users import Users
from werkzeug.security import generate_password_hash


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def get_user_by_id(self, id_to_get):
        return self.local_session.query(Users).get(id_to_get).all()

    def get_all_users(self):
        return self.local_session.query(Users).all()

    def post_user(self, user):
        self.local_session.add(user)
        self.local_session.commit()

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()

    def get_user_by_username(self, value):
        return self.local_session.query(Users).filter(Users.username == value).all()

    def get_user_by_email(self, value):
        return self.local_session.query(Users).filter(Users.email == value).all()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def delete_user_by_id(self, id_column_name, id_to_remove):
        self.local_session.query(Users).filter(id_column_name == id_to_remove).delete(synchronize_session=False)
        self.local_session.commit()

    def put_by_id(self, id_column_name, id_to_update, data):
        exist_object = self.local_session.query(Users).filter(id_column_name == id_to_update)
        if not exist_object:
            self.local_session.add(exist_object)
        exist_object.update(data)
        self.local_session.commit()

    def patch_by_id(self, id_column_name, id_to_update, data):
        exist_object = self.local_session.query(Users).filter(id_column_name == id_to_update)
        if not exist_object:
            return
        exist_object.update(data)
        self.local_session.commit()

    def drop_all_tables(self):
        self.local_session.execute('drop TABLE users CASCADE')
        self.local_session.commit()

    def reset_db(self):
        self.add_all([Users(username='Dave1', email='New1@gmail.com', password=generate_password_hash('12345')),
                      Users(username='Jane', email='New2@gmail.com', password=generate_password_hash('22345')),
                      Users(username='Danny', email='New3@gmail.com', password=generate_password_hash('32345')),
                      Users(username='Loren', email='New4@gmail.com', password=generate_password_hash('42345')),
                      Users(username='Julie', email='New5@gmail.com', password=generate_password_hash('52345'))])



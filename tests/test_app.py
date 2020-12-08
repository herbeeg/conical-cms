import json
import pytest

from pathlib import Path
from werkzeug.security import check_password_hash

from app.database import db
from app.main import create_app
from tests.utils import register

TEST_DB = 'test.db'

class TestMainCase:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        self.app = create_app()
        self.app.app_context().push()

        self.app.config['TESTING'] = True
        self.app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR.joinpath(TEST_DB)}'

        self.app.config['EMAIL'] = 'admin@test.com'
        self.app.config['USERNAME'] = 'admin'
        self.app.config['PASSWORD'] = 'password'

        db.create_all()

        with self.app.test_client(self) as client:
            yield client
        
        db.drop_all()

    def testIndex(self, client):
        response = client.get(
            '/',
            content_type='html/text'
        )

        assert 200 == response.status_code
        assert b'There is no ignorance, there is knowledge.' == response.data

    def testDatabase(self):
        assert Path(TEST_DB).is_file()

    def testRegister(self, client):
        rv = register(
            client,
            self.app.config['EMAIL'],
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )

        assert 'Registration successful.' in json.loads(rv.data)['message']

        user = db.session.query(
            User
        ).filter_by(
            id=1
        ).one()

        assert 1 == user.id
        assert self.app.config['EMAIL'] == user.email
        assert self.app.config['USERNAME'] == user.username
        assert check_password_hash(user.password, self.app.config['PASSWORD'])

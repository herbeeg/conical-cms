import datetime
import json
import pytest

from pathlib import Path
from werkzeug.security import check_password_hash

from app.database import db
from app.main import create_app
from app.models.user import User
from tests.utils import login, logout, register

TEST_DB = 'test.db'

class TestAuthentication:
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

    def testRegister(self, client):
        timestamp = int(datetime.datetime.utcnow().timestamp())
        """Take a timestamp value now to compare against when a user is registered in the database."""

        rv = register(
            client,
            self.app.config['EMAIL'],
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )

        assert 200 == rv.status_code
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

        assert timestamp <= user.created_at
        assert timestamp <= user.updated_at

        rv = register(
            client,
            self.app.config['EMAIL'],
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )

        assert 400 == rv.status_code
        assert 'A user with that email address or username already exists.' in json.loads(rv.data)['message']

    def testLogin(self, client):
        rv = register(
            client,
            self.app.config['EMAIL'],
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )
        rv = login(
            client,
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )

        assert 200 == rv.status_code
        assert 'Login successful.' in json.loads(rv.data)['message']

        rv = login(
            client,
            self.app.config['USERNAME'] + 'log',
            self.app.config['PASSWORD']
        )

        assert 400 == rv.status_code
        assert 'Invalid username or password.' in json.loads(rv.data)['message']

        rv = login(
            client,
            self.app.config['USERNAME'],
            self.app.config['PASSWORD'] + 'log'
        )

        assert 400 == rv.status_code
        assert 'Invalid username or password.' in json.loads(rv.data)['message']

    def testLogout(self, client):
        rv = register(
            client,
            self.app.config['EMAIL'],
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )
        rv = login(
            client,
            self.app.config['USERNAME'],
            self.app.config['PASSWORD']
        )

        response = logout(client)

        assert 200 == response.status_code
        assert 'Logout successful.' in response.json['message']

from flask import Blueprint

overview = Blueprint('overview', __name__)

@overview.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'

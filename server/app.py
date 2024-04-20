from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#DATABASE = f"postgresql://vendersweets_user:4BvmBhqnSQAdnGAsx6U2Fpl39duG2uBs@dpg-cohr1tv79t8c7386khr0-a.oregon-postgres.render.com/vendersweets"
DATABASE= os.environ.get('DATABASE_URI')
app = Flask(__name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

from routes import *
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)

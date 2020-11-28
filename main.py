import os
from flask import Flask
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:31102000aA@localhost/recipes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.TEXT)
    pack = db.Column(db.TEXT)
    link = db.Column(db.TEXT)
    name = db.Column(db.TEXT)
    summary = db.Column(db.TEXT)
    image = db.Column(db.TEXT)
    meta = db.Column(db.TEXT)
    ingred = db.Column(db.TEXT)
    direction = db.Column(db.TEXT)
    facts = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        self.type = kwargs['type']
        self.pack = kwargs['pack']
        self.link = kwargs['link']
        self.name = kwargs['name']
        self.summary = kwargs['summary']
        self.image = kwargs['image']
        self.meta = kwargs['meta']
        self.ingred = kwargs['ingred']
        self.direction = kwargs['direction']
        self.facts = kwargs['facts']

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Recipe name={self.name}'


class RecipesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Food
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    type = fields.String(required=True)
    pack = fields.String(required=True)
    link = fields.String(required=True)
    name = fields.String(required=True)
    summary = fields.String(required=True)
    image = fields.String(required=True)
    meta = fields.String(required=True)
    ingred = fields.String(required=True)
    direction = fields.String(required=True)
    facts = fields.String(required=True)


db.create_all()

@app.route('/')
def hello_world():
    return '<h1> RECIPES </h1>'

@app.route('/recipes', methods = ['GET'])
def get_all_recipes():
    get_food = Food.query.all()
    recipe_schema = RecipesSchema(many=True)
    recipe = recipe_schema.dump(get_food)
    return make_response(jsonify({"recipe": recipe}))

@app.route('/recipe/<id>', methods = ['GET'])
def get_recipe_by_id(id):
    get_food = Food.query.get(id)
    recipe_schema = RecipesSchema()
    recipe = recipe_schema.dump(get_food)
    return make_response(jsonify({"recipe": recipe}))

@app.route('/recipe/<name>', methods = ['GET'])
def get_recipe_by_name(name):
    get_food = Food.query.get(name)
    recipe_schema = RecipesSchema()
    recipe = recipe_schema.dump(get_food)
    return make_response(jsonify({"recipe": recipe}))

@app.route('/recipes/<type>', methods = ['GET'])
def get_recipes_by_type(type):
    get_food = Food.query.filter_by(type=str(type)).all()
    recipe_schema = RecipesSchema(many=True)
    recipe = recipe_schema.dump(get_food)
    return make_response(jsonify({"recipe": recipe}))

@app.route('/recipes/<pack>', methods = ['GET'])
def get_recipes_by_pack(pack):
    get_food = Food.query.filter_by(pack=str(pack)).all()
    recipe_schema = RecipesSchema(many=True)
    recipe = recipe_schema.dump(get_food)
    return make_response(jsonify({"recipe": recipe}))

# Breakfast Cups

if __name__ == "__main__":
    app.run()
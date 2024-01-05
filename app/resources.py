# app/resources.py
from flask_restful import Resource, reqparse
from .models import db, Item

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Item name')
parser.add_argument('description', type=str, help='Item description')

class ItemResource(Resource):
    def get(self, item_id):
        item = Item.query.filter_by(id=item_id).first()
        if item:
            return {'name': item.name, 'description': item.description}
        return {'message': 'Item not found'}, 404

    def put(self, item_id):
        args = parser.parse_args()
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.name = args['name']
            item.description = args['description']
            db.session.commit()
            return {'message': 'Item updated successfully'}
        return {'message': 'Item not found'}, 404

    def delete(self, item_id):
        item = Item.query.filter_by(id=item_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'message': 'Item deleted successfully'}
        return {'message': 'Item not found'}, 404

class ItemListResource(Resource):
    def get(self):
        items = Item.query.all()
        item_list = [{'name': item.name, 'description': item.description} for item in items]
        return {'items': item_list}

    def post(self):
        args = parser.parse_args()
        new_item = Item(name=args['name'], description=args['description'])
        db.session.add(new_item)
        db.session.commit()
        return {'message': 'Item created successfully'}

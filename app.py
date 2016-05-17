import os
import tornado.ioloop
import tornado.web
import json
from bson import json_util
from pymongo import MongoClient

# Config templates and static path
settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True
}

# Db config
client = MongoClient('localhost', 27017)
db = client['lending_front']


class IndexHandler(tornado.web.RequestHandler):
    """ Index Controller."""

    def get(self):
        self.render('index.html')


class OwnerHandler(tornado.web.RequestHandler):
    def get(self):
        owners = db.owners.find()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(owners), default=json_util.default))

    def post(self):
        owner_data = json.loads(self.request.body)
        db.owners.insert(owner_data)
        self.set_header("Content-Type", "application/json")
        self.set_status(201)


class BusinessHandler(tornado.web.RequestHandler):
    def get(self):
        business = db.business.find()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(business), default=json_util.default))

    def post(self):
        business_data = json.loads(self.request.body)
        db.business.insert(business_data)
        decision = analyze_data_and_take_decision(
            business_data['requested_amount'])
        response = {
            'amount': business_data['requested_amount'],
            'status': decision,
            'company': business_data['name'],
            'owner': 'Jorge Galvis'
        }
        self.set_header("Content-Type", "application/json")
        self.set_status(201)
        self.write(json.dumps(response, default=json_util.default))


# This simulates to be the model
def analyze_data_and_take_decision(requested_amount):
    """This function checks the requested_amount and determines if money can be
        funded."""
    if requested_amount > 50000:
        return 'Declined'
    if requested_amount == 50000:
        return 'Undecided'
    if requested_amount < 50000:
        return 'Approved'


def make_app():
    """ This function creates an app and return it."""
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/api/v1/owners', OwnerHandler),
        (r'/api/v1/business', BusinessHandler)
    ], **settings)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

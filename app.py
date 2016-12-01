import os
import tornado.ioloop
import tornado.web
import json
from bson import json_util
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime


# Config templates and static path
settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True
}

# Db config
try:
    client = MongoClient('localhost', 27017)
    db = client['lending_front']
except PyMongoError:
    # Better to log this instead or print it
    print('Error trying to connect to the DB')
    import sys
    sys.exit()


class IndexHandler(tornado.web.RequestHandler):
    """ Index Controller."""

    def get(self):
        self.render('index.html')


class OwnerHandler(tornado.web.RequestHandler):
    def post(self):
        """Save owners info."""
        owner_data = json.loads(self.request.body)

        response = {}
        try:
            db.owners.replace_one(
                {
                    'social_security_number':
                        owner_data['social_security_number']
                },
                owner_data,
                True
            )
            response['error'] = False
            response['message'] = 'Owner recorded'
            response['owner_id'] = owner_data['social_security_number']
            response['first_name'] = owner_data['first_name']
            response['last_name'] = owner_data['last_name']
        except PyMongoError as e:
            print(e.message)
            response['error'] = True
            response['data'] = 'Internal DB error'

        self.set_header("Content-Type", "application/json")
        if response['error']:
            self.set_status(500)
        else:
            self.set_status(201)
        self.write(json.dumps(response, default=json_util.default))


class BusinessHandler(tornado.web.RequestHandler):
    def post(self):
        business_data = json.loads(self.request.body)
        business_data['date'] = datetime.now()
        try:
            db.business.insert(business_data)
            decision = analyze_data_and_take_decision(
                business_data['requested_amount'])

            owner = db.owners.find_one(
                {"social_security_number": business_data['owner_id']})
            full_name = "{} {}".format(owner["first_name"], owner["last_name"])

            response = {
                'amount': business_data['requested_amount'],
                'status': decision,
                'company': business_data['name'],
                'owner_id': business_data['owner_id'],
                'full_name': full_name
            }
            self.set_status(201)
        except (PyMongoError, ValueError) as e:
            print(e.message)
            self.set_status(500)
            response['error'] = True
            response['data'] = 'Internal data error'

        self.set_header("Content-Type", "application/json")
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

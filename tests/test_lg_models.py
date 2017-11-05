import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import LG


class LGModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_lg_init(self):
        l = LG(no='1234567',type=1,companyname='some a comp.',amt='1000.10',createdate='20100101',status=0)
        self.assertTrue(l is not None)
        db.session.add(l)
        db.session.commit()
        lg = LG.get_by_no('1234567')
        self.assertFalse(lg is None)




from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_zoom.utilities import fdao_zoom_override
from uw_zoom import ZOOM
import datetime
import pytz


@fdao_zoom_override
class GWSGroupTest(TestCase):
    def test_request_headers(self):
        zoom = ZOOM()
        self.assertEquals(zoom._headers(), {'Accept': 'application/json'})

    def test_get_users(self):
        zoom = ZOOM()
        users = zoom.get_all_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].first_name, "Melina")
        self.assertEqual(users[1].first_name, "Bill")
        created_dt = datetime.datetime(year=2018,
                                       month=11,
                                       day=15,
                                       hour=1,
                                       minute=10,
                                       second=8,
                                       tzinfo=pytz.UTC)
        self.assertEqual(users[0].created_at, created_dt)

    def test_delete_user(self):
        zoom = ZOOM()
        with self.assertRaises(DataFailureException):
            zoom.delete_user('z8yAAAAA8bbbQ', is_delete=True)
        resp = zoom.delete_user('z8yAAAAA8bbbQ')
        self.assertEqual(resp.status, 200)

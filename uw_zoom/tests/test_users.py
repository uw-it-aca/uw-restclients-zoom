from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_zoom.utilities import fdao_zoom_override
from uw_zoom.models import ZoomUser
from uw_zoom.users import Users
import datetime
import pytz
import mock


@fdao_zoom_override
class UsersAPITest(TestCase):
    def test_get_users(self):
        zoom = Users()
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

    @mock.patch.object(Users, '_patch_resource')
    def test_update_type(self, mock_patch):
        zoom = Users()
        resp = zoom.update_user_type('z8yAAAAA8bbbQ', ZoomUser.TYPE_BASIC)
        mock_patch.assert_called_with(
            '/v2/users/z8yAAAAA8bbbQ', {'type': ZoomUser.TYPE_BASIC})

    def test_delete_user(self):
        zoom = Users()
        with self.assertRaises(DataFailureException):
            zoom.delete_user('z8yAAAAA8bbbQ', is_delete=True)
        resp = zoom.delete_user('z8yAAAAA8bbbQ')
        self.assertEqual(resp.status, 200)
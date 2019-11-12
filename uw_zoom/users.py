from uw_zoom import ZOOM
from uw_zoom.models import ZoomUser

USERS_API = '/v2/users'


class Users(ZOOM):
    def get_all_users(self, **kwargs):
        users = []
        for user_data in self._get_paged_resource(USERS_API, data_key='users'):
            users.append(ZoomUser.from_json(user_data))
        return users

    def update_user_type(self, user_id, type_id):
        url = '{}/{}'.format(USERS_API, user_id)
        body = {'type': type_id}
        return self._patch_resource(url, body)

    def delete_user(self, user_id, is_delete=False):
        url = '{}/{}'.format(USERS_API, user_id)
        # default behavior is to disassociate if action isn't passed
        params = {'action': 'delete'} if is_delete else {}
        return self._delete_resource(url, params)
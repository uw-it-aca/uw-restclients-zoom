import json
import re
from uw_zoom.dao import ZOOM_DAO
from uw_zoom.models import ZoomUser
from restclients_core.exceptions import DataFailureException
from urllib.parse import urlencode

# max page size 300
PAGE_SIZE = 300
USERS_API = '/v2/users'


class ZOOM(object):
    def __init__(self, config={}):
        self.DAO = ZOOM_DAO()

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

    def _get_paged_resource(self, url, data_key):
        params = {'page_size': PAGE_SIZE}
        response = self._get_resource(url, params)
        data = response[data_key]

        if response.get('page_count', 1) > 1:
            for page_number in range(2, response['page_count'] + 1):
                params['page_number'] = page_number
                response = self._get_resource(url, params)
                data.extend(response[data_key])
        return data

    def _get_resource(self, url, params={}):
        if len(params):
            url += '?' + urlencode(params)
        response = self.DAO.getURL(url, self._headers())

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _patch_resource(self, url, body):
        response = self.DAO.patchURL(url, body, self._headers())

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _delete_resource(self, url, params={}):
        if len(params):
            url += '?' + urlencode(params)
        response = self.DAO.deleteURL(url, self._headers())

        if response.status != 204 and response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        return response

    def _headers(self):
        headers = {"Accept": "application/json"}
        return headers

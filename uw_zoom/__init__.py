"""
This is the interface for interacting with the Group Web Service.
"""

from datetime import datetime
from copy import deepcopy
import json
import logging
import re
from urllib.parse import urlencode
from restclients_core.exceptions import DataFailureException
from uw_zoom.dao import ZOOM_DAO
from uw_zoom.models import ZoomUser
import dateparser


logger = logging.getLogger(__name__)

# max page size 300
PAGE_SIZE = 300


class ZOOM(object):
    """
    The ZOOM object has methods for interacting with the Zoom API.
    """
    API = '/v2'

    def __init__(self, config={}):
        self.DAO = ZOOM_DAO()

    def get_all_users(self, **kwargs):
        url = "{}/users?page_size={}".format(self.API, PAGE_SIZE)
        response = self._get_resource(url)
        users = self._users_from_json(response['users'])
        if response['page_count'] > 1:
            for page in range(2, response['page_count']+1):
                users += self._users_from_json(self._get_users_page(page))
        return users

    def _get_users_page(self, page_number):
        url = "{}/users?page_size={}&page_number={}".format(self.API,
                                                            PAGE_SIZE,
                                                            page_number)
        response = self._get_resource(url)
        return response['users']

    def _users_from_json(self, data):
        users = []
        for user_data in data:
            user = ZoomUser()
            user.id = user_data['id']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            user.type = user_data['type']
            user.status = user_data['status']
            user.pmi = user_data['pmi']
            user.timezone = user_data['timezone']
            user.dept = user_data['dept']
            user.verified = user_data['verified']
            user.created_at = dateparser.parse(user_data['created_at'])
            user.last_login_time = dateparser.parse(user_data['last_login_time'])
            users.append(user)
        return users

    def delete_user(self, user_id, is_delete=False):
        # default behavior is to disassociate if is_delete isn't passed
        url = "{}/users/{}".format(self.API, user_id)
        if is_delete:
            url += "?action=delete"
        response = self._delete_resource(url)
        return response



    def _get_resource(self, url):
        response = self.DAO.getURL(url, self._headers())

        if response.status != 200:
            self._log_error(url, response)
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _put_resource(self, url, headers, body={}):
        headers["Content-Type"] = "application/json"
        headers.update(self._headers())

        response = self.DAO.putURL(url, headers, json.dumps(body))

        if response.status != 200 and response.status != 201:
            self._log_error(url, response)
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _delete_resource(self, url):
        response = self.DAO.deleteURL(url, self._headers())

        if response.status != 204 and response.status != 200:
            self._log_error(url, response)
            raise DataFailureException(url, response.status, response.data)
        return response

    def _headers(self):
        headers = {"Accept": "application/json"}
        return headers

    def _log_error(self, url, response):
        logger.error("{0} ==> status:{1} data:{2}".format(
            url, response.status, response.data))
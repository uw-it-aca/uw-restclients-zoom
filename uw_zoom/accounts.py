from uw_zoom import ZOOM
from uw_zoom.models import ZoomAccount, ZoomUser

ACCOUNTS_API = '/v2/accounts'


class Accounts(ZOOM):
    def get_sub_accounts(self, **kwargs):
        accounts = []
        for data in self._get_paged_resource(ACCOUNTS_API, key='accounts'):
            accounts.append(ZoomAccount.from_json(data))
        return accounts

    def get_account_users(self, account_id):
        url = ACCOUNTS_API + '/{}/users'.format(account_id)
        users = []
        for data in self._get_paged_resource(url, key='users'):
            users.append(ZoomUser.from_json(data))
        return users

    def update_account_user_type(self, account_id, user_id, type_id):
        url = ACCOUNTS_API + '/{}/users/{}'.format(account_id, user_id)
        body = {'type': type_id}
        return self._patch_resource(url, body)

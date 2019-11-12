from unittest import TestCase
from uw_zoom import ZOOM
import mock


class ZoomAPITest(TestCase):
    @mock.patch.object(ZOOM, '_get_resource')
    def test_get_paged_resource(self, mock_get):
        zoom = ZOOM()

        # One page returned
        mock_get.return_value = {'page_count': 1, 'test': []}
        resp = zoom._get_paged_resource('/api/test', 'test')
        mock_get.assert_called_with(
            '/api/test', {'page_size': zoom.PAGE_SIZE})

        # More than one page returned
        mock_get.return_value = {'page_count': 2, 'test': []}
        resp = zoom._get_paged_resource('/api/test', 'test')
        mock_get.assert_called_with(
            '/api/test', {'page_size': 300, 'page_number': 2})

    def test_request_headers(self):
        zoom = ZOOM()
        self.assertEquals(zoom._headers(), {'Accept': 'application/json'})

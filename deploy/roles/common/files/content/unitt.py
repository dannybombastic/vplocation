import datetime
import unittest
from unittest.mock import Mock , patch
from nose.tools import assert_is_not_none, assert_true, assert_list_equal
import requests

from vozplus_location import  create_user, get_mac_from_this_equip, get_autho_token, sendto_api
class Tests(unittest.TestCase):




    @patch('vozplus_location.create_user')
    def test_creating_user_when_user_exist(self,mock_get):
        user_exist = [{ "username": ["A user with that username already exists."]}]
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = user_exist
        response = [create_user().json()]
        assert_list_equal(response,user_exist)


    def test_creating_user_when_is_ok(self):
        actual = create_user()
        actual = [actual.json()]
        actual_keys = actual.pop().keys()

        print(actual_keys)

        with patch('vozplus_location.create_user')as mock_get:
           create_user_keys = [{"url": "http://31.220.111.56:8000/api/laptop/176/", "mac": "32:65:54:87", "date": "2018-07-25T20:46:59.195457Z", "data": "lo que sa", "created": "2018-07-25T18:46:59.918897Z", "updated": "2018-07-25T18:46:59.918914Z"}]
           mock_get.return_value.ok = True
           mock_get.return_value.json.return_value = create_user_keys.pop().keys()
           response = [create_user().json()]
           response_keys = response.pop().keys()
           assert_list_equal(list(actual_keys), list(response_keys))

    def test_request_response(self):
        data = {
            "username": "testUser2",
            "password": "659011563"
        }


        headers = {"Content-Type": "application/json"}
        response = requests.post(url='http://153.92.209.82:8000/api/users/', json=data, headers=headers)
        print(response.ok)
        assert_true(response.ok)

    def test_sending_position_to_api(self):

        actual = [sendto_api('32:65:54:87', datetime.datetime.now(), 'lo que sa').json()]
        actual_keys = actual.pop().keys()

        with patch('vozplus_location.sendto_api')as mock_get:
            create_position_keys = [{"id": 2, "type": "Feature", "geometry": {"type": "Point", "coordinates": [-4.647989272423929, 36.64328630762586]}, "properties": {"name": "javilon"}}]
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = create_position_keys.pop().keys()
            response = [sendto_api('32:65:54:87', datetime.datetime.now(), 'lo que sa').json()]
            response_keys = response.pop().keys()

            assert_list_equal(list(actual_keys), list(response_keys))


if __name__=='__main__':
      unittest.main()
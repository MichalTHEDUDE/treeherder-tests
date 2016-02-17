# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

import pytest
import requests


@pytest.fixture(scope='session')
def capabilities(capabilities):
    capabilities.setdefault('tags', []).append('treeherder')
    return capabilities


@pytest.fixture
def persona_test_user():
    max_retries = 5
    attempt = 1
    while attempt <= max_retries:
        msg = 'There was a problem getting a personatestuser -- attempt {num}: '.format(
            num=attempt)
        try:
            response = requests.get('http://personatestuser.org/email')
            user_info = response.json()
            if user_info.get('email'):
                return user_info
        except ValueError:
            msg += 'No json was returned from personatestuser.org. \n'
            msg += 'Response status / content: {status} / {content}'.format(
                status=response.status_code,
                content=response.content)
        else:
            msg += json.dumps(user_info, indent=4, sort_keys=True)
        print msg
        attempt += 1
    raise Exception(msg)


@pytest.fixture(scope='function')
def new_user(persona_test_user):
    return {
        'email': persona_test_user['email'],
        'password': persona_test_user['pass'],
        'name': persona_test_user['email'].split('@')[0],
        'username': persona_test_user['email'].split('@')[0],
        'url': 'http://www.mozilla.org/'
    }


@pytest.fixture
def selenium(selenium):
    selenium.maximize_window()
    return selenium

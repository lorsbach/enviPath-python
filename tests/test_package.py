# Copyright 2020 enviPath UG & Co. KG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import pytest
from requests import HTTPError

from enviPath_python.enviPath import enviPath
from enviPath_python.objects import Package


class TestPackage:

    @pytest.fixture
    def eP(self):
        INSTANCE_HOST = 'http://localhost:8080/'
        return enviPath(INSTANCE_HOST)

    @pytest.fixture
    def anonymous_user(self, eP):
        for user in eP.get_users():
            if user.get_name() == 'anonymous':
                return user
        raise ValueError("No anonymoususer found!")

    @pytest.fixture
    def anonymous_default_group(self, anonymous_user):
        return anonymous_user.get_groups()[0]

    def test_create_package(self, eP, anonymous_user, anonymous_default_group):
        p = Package.create(eP, anonymous_default_group, name="Test Suite Package",
                           description="Test Suite Package Description")
        assert p.get_name() == "Test Suite Package"
        assert p.get_description() == "Test Suite Package Description"
        p.delete()

    def test_delete_package(self, eP, anonymous_default_group):
        p = Package.create(eP, anonymous_default_group, name="Test Suite Package",
                           description="Test Suite Package Description")

        package_id = p.get_id()
        p.delete()
        with pytest.raises(HTTPError):
            eP.get_package(package_id)

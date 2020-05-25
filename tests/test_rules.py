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
from enviPath_python.objects import Package, Rule, SimpleRule, SequentialCompositeRule, ParallelCompositeRule


class TestRules:

    @pytest.fixture(scope='module')
    def eP(self):
        INSTANCE_HOST = 'http://localhost:8080/'
        return enviPath(INSTANCE_HOST)

    @pytest.fixture(scope='module')
    def anonymous_user(self, eP):
        for user in eP.get_users():
            if user.get_name() == 'anonymous':
                return user
        raise ValueError("No anonymoususer found!")

    @pytest.fixture(scope='module')
    def anonymous_default_group(self, anonymous_user):
        return anonymous_user.get_groups()[0]

    @pytest.fixture(scope='module')
    def package(self, eP, anonymous_default_group):
        p = Package.create(eP, anonymous_default_group, name="Test Suite Package",
                           description="Test Suite Package Description")
        yield p
        p.delete()

    def test_create_simple_rule(self, package):
        rule_smirks = '[H][#8]-[#7:3]=[#6:4]([H])-[$([#1,*]):6]>>[$([#1,*]):6][C:4]#[N:3]'
        rule_name = 'PythonClientRule'
        rule_description = 'A SimpleRule created via Python Client'
        r = SimpleRule.create(package, smirks=rule_smirks,
                              name=rule_name, description=rule_description)
        assert r.get_smirks() == rule_smirks
        assert r.get_name() == rule_name
        assert r.get_description() == rule_description

        r.delete()

    def test_create_sequential_composite_rule(self, package):
        rule_smirks = '[H][#8]-[#7:3]=[#6:4]([H])-[$([#1,*]):6]>>[$([#1,*]):6][C:4]#[N:3]'
        rule_name = 'PythonClientRule'
        rule_description = 'A SimpleRule created via Python Client'
        r = SimpleRule.create(package, smirks=rule_smirks,
                              name=rule_name, description=rule_description)
        sr = SequentialCompositeRule.create(package, [r], name=rule_name, description=rule_description)

        assert r in sr.get_simple_rules()

        r.delete()
        sr.delete()

    def test_create_parallel_composite_rule(self, package):
        rule_smirks = '[H][#8]-[#7:3]=[#6:4]([H])-[$([#1,*]):6]>>[$([#1,*]):6][C:4]#[N:3]'
        rule_name = 'PythonClientRule'
        rule_description = 'A SimpleRule created via Python Client'
        r = SimpleRule.create(package, smirks=rule_smirks,
                              name=rule_name, description=rule_description)
        pr = ParallelCompositeRule.create(package, [r], name=rule_name, description=rule_description)

        assert r in pr.get_simple_rules()

        r.delete()
        pr.delete()

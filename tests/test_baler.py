import unittest
import os
import json
import baler


class TestBaleJSON(unittest.TestCase):
    def setUp(self):
        self.filepath = 'test_json_output.json'

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_bale_reg_json(self):
        harvest = [
            ['192.168.0.1', 'IPv4', 'inbound', 'testdata', '', '2017-03-17'],
            ['192.168.1.1', 'IPv4', 'outbound', 'testdata', 'note', '2017-03-17'],
        ]
        baler.bale_reg_json(harvest, self.filepath)
        assert os.path.exists(self.filepath)
        with open(self.filepath) as f:
            mydict = json.load(f)

        assert mydict == [
            {
                "entity": '192.168.0.1',
                "type": 'IPv4',
                "direction": 'inbound',
                "source": 'testdata',
                "notes": '',
                "date": '2017-03-17'
            },
            {
                "entity": '192.168.1.1',
                "type": 'IPv4',
                "direction": 'outbound',
                "source": 'testdata',
                "notes": 'note',
                "date": '2017-03-17'
            }
        ]

    def test_bale_enr_json(self):
        harvest = [
            ['192.168.0.1', 'IPv4', 'inbound', 'testdata', '', '2017-03-17', 1422,
             'globe', 'PH', '', ''],
            ['192.168.1.1', 'IPv4', 'outbound', 'testdata', 'note', '2017-03-17', 2131,
             'smart', 'JP', 'myhost', 'myrhost'],
        ]
        baler.bale_enr_json(harvest, self.filepath)
        assert os.path.exists(self.filepath)
        with open(self.filepath) as f:
            mydict = json.load(f)

        assert mydict == [
            {
                "entity": '192.168.0.1',
                "type": 'IPv4',
                "direction": 'inbound',
                "source": 'testdata',
                "notes": '',
                "date": '2017-03-17',
                "asnumber": 1422,
                "asname": 'globe',
                "country": 'PH',
                "host": '',
                "rhost": ''
            },
            {
                "entity": '192.168.1.1',
                "type": 'IPv4',
                "direction": 'outbound',
                "source": 'testdata',
                "notes": 'note',
                "date": '2017-03-17',
                "asnumber": 2131,
                "asname": 'smart',
                "country": 'JP',
                "host": 'myhost',
                "rhost": 'myrhost'
            }
        ]

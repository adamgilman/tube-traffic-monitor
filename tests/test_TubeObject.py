#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from tubetrafficmonitor import TTM

class TestTPMObject(unittest.TestCase):

    def setUp(self):
        self.ttm = TTM()

    def test_TTMExists(self):
        self.assertEqual( type(self.ttm), TTM )

if __name__ == '__main__':
    unittest.main()

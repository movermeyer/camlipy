# -*- encoding: utf-8 -*-
import unittest
import logging
import os

import simplejson as json

from camlipy.tests import CamliPyTestCase
from camlipy.schema import Schema, Permanode
import camlipy

logging.basicConfig(level=logging.DEBUG)


class TestSchema(CamliPyTestCase):
    def testNewBasicSchema(self):
        basic_schema = Schema(self.server)
        expected = {'camliVersion': camlipy.CAMLIVERSION}
        self.assertEqual(basic_schema.json(), json.dumps(expected))
        signed = json.loads(basic_schema.sign())
        self.assertTrue('camliSigner' in signed)
        self.assertTrue('camliSig' in signed)

    def _createBlob(self):
        test_blob_str = os.urandom(4096)
        self.server.put_blobs([test_blob_str])
        return self.compute_hash(test_blob_str)

    def testPermanode(self):
        br = self._createBlob()
        permanode = Permanode(self.server)
        permanode_br = permanode.save(br)

        permanode_res = self.server.get_blob(permanode_br)
        self.assertTrue(isinstance(permanode_res, dict))
        claims = permanode.claims()
        self.assertEqual(len(claims), 1)
        self.assertEqual(permanode.get_camli_content(), br)

        br2 = self._createBlob()
        permanode.set_camli_content(br2)
        self.assertEqual(len(permanode.claims()), 2)
        self.assertEqual(permanode.get_camli_content(), br2)


if __name__ == '__main__':
    unittest.main()
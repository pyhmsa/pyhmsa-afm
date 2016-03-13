#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import shutil
import tempfile
import os

# Third party modules.
from pyhmsa.type.numerical import convert_unit

# Local modules.
from pyhmsa_afm.fileformat.importer.asc import ImporterAFMAsc

# Globals and constants variables.

class TestImporterAFMAsc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestImporterAFMAsc, cls).setUpClass()

        testdata = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata')
        filepath = os.path.join(testdata, 'afm.asc.zip')

        cls.tmpdir = tempfile.mkdtemp()
        shutil.unpack_archive(filepath, cls.tmpdir, 'zip')

    @classmethod
    def tearDownClass(cls):
        super(TestImporterAFMAsc, cls).tearDownClass()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = os.path.join(self.tmpdir, 'afm.asc')
        self.imp = ImporterAFMAsc()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testimport_(self):
        filepath = os.path.join(self.tmpdir, 'afm.asc')
        self.imp.import_(filepath)
        datafile = self.imp.get()

        self.assertEqual(1, len(datafile.conditions))
        self.assertEqual(1, len(datafile.data))

        acq = datafile.conditions['Acq0']
        self.assertEqual(1024, acq.step_count_x)
        self.assertEqual(1024, acq.step_count_y)
        self.assertAlmostEqual(29.296875, convert_unit('nm', acq.step_size_x), 4)
        self.assertAlmostEqual(29.296875, convert_unit('nm', acq.step_size_y), 4)

        self.assertEqual(2013, datafile.header.date.year)
        self.assertEqual(5, datafile.header.date.month)
        self.assertEqual(3, datafile.header.date.day)
        self.assertEqual(8, datafile.header.time.hour)
        self.assertEqual(20, datafile.header.time.minute)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()

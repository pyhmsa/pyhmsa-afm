"""
AFM importer for ascii files (.asc)
"""

# Standard library modules.
import datetime

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.importer.importer import _Importer, _ImporterThread

from pyhmsa.datafile import DataFile
from pyhmsa.spec.header import Header
from pyhmsa.spec.condition.acquisition import AcquisitionRasterXY
from pyhmsa.spec.datum.imageraster import ImageRaster2D

# Globals and constants variables.
from pyhmsa.spec.condition.acquisition import RASTER_MODE_STAGE

class _ImporterAFMAscThread(_ImporterThread):

    def __init__(self, filepath):
        _ImporterThread.__init__(self, filepath)

    def _run(self, filepath, *args, **kwargs):
        datafile = DataFile()

        self._update_status(0.1, 'Read ASC header')
        headerdict, startline = self._read_header(filepath)

        self._update_status(0.2, 'Extract header')
        datafile.header.update(self._extract_header(headerdict))

        self._update_status(0.5, 'Extract acquisition condition')
        datafile.conditions.addall(self._extract_acquisition(headerdict))

        # Detectors and data
        self._update_status(0.7, 'Extract data')
        buffer = self._read_data(filepath, startline)

        acq = datafile.conditions['Acq0']

        datum_name = 'AFM0'
        datum = ImageRaster2D(acq.step_count_x, acq.step_count_y,
                              dtype=np.float64,
                              buffer=np.ravel(buffer),
                              conditions=datafile.conditions)
        datafile.data.add(datum_name, datum)

        return datafile

    def _read_header(self, filepath):
        headerdict = {}
        with open(filepath, "r", encoding='ascii', errors='ignore') as fp:
            for iline, line in enumerate(fp):
                if line.startswith("# Start of Data:"):
                    break
                parts = line.split("=")
                if len(parts) == 1:
                    parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    if key.startswith('#'): key = key[1:]
                    key = key.strip().lower()
                    value = parts[1].strip()
                    headerdict[key] = value

        return headerdict, iline

    def _read_data(self, filepath, startline):
        with open(filepath, "r", encoding='ascii', errors='ignore') as fp:
            return np.genfromtxt(fp, skip_header=startline + 1)

    def _extract_header(self, headerdict):
        header = Header()

        if 'date' in headerdict:
            try:
                dt = datetime.datetime.strptime(headerdict['date'],
                                                '%d.%m.%Y %H:%M')
                header.date = dt.date()
                header.time = dt.time()
            except:
                pass

        return header

    def _extract_acquisition(self, headerdict):
        step_count_x = int(headerdict['x-pixels'])
        step_count_y = int(headerdict['y-pixels'])

        step_size_x = (float(headerdict['x-length']) / step_count_x, 'nm')
        step_size_y = (float(headerdict['y-length']) / step_count_y, 'nm')

        frame_count = 1
        raster_mode = RASTER_MODE_STAGE

        c = AcquisitionRasterXY(step_count_x=step_count_x,
                                step_count_y=step_count_y,
                                step_size_x=step_size_x,
                                step_size_y=step_size_y,
                                frame_count=frame_count,
                                raster_mode=raster_mode)

        return {'Acq0': c}

class ImporterAFMAsc(_Importer):

    SUPPORTED_EXTENSIONS = ('.asc',)

    def _create_thread(self, filepath, *args, **kwargs):
        return _ImporterAFMAscThread(filepath)

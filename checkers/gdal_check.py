from checkers.check import Checker
from osgeo import gdal


class GDALChecker(Checker):

    def __init__(self, path):
        Checker.__init__(self, path)
        self.type = "GDAL {}".format(gdal.VersionInfo())

    def check(self):
        try:
            ds = gdal.Open(self.path)
            if ds == None or ds.GetProjection() == "" or ds.GetGeoTransform() == "":
                self.result = False
            else:
                self.result = True

        except:
            self.result = False

        return self.to_json()






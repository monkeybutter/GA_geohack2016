import checkers

if __name__ == "__main__":
    checker1 = checkers.GDALChecker("/Users/pablo/Desktop/LC80950732015054LGN00_B1.TIF")
    checker2 = checkers.HDF5Checker("/Users/pablo/Desktop/LC80950732015054LGN00_B1.TIF")

    print(checker1.check())
    print(checker2.check())
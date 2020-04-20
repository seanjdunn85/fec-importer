import wget, os, zipfile, datetime, sys, json
from FECDisclosureObject import FECDisclosureObject

update = '--update-current-year' in sys.argv or '-U' in  sys.argv
verbose = '--verbose' in sys.argv or '-V' in  sys.argv

years = ['04','06','08','10','12','14','16','18']

for year in years:
    fec_obj = FECDisclosureObject(year, 'ccl')
    fec_obj.get_disclosure()
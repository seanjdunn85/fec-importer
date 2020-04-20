import wget, os, zipfile, datetime, sys, json
from FECGraphClient import FECGraphClient
from termcolor import colored
from shutil import copyfile

class FECDisclosureObject(object):
    #the years that we're looking to import
    years = ['04','06','08','10','12','14','16','18']
    # filetypes need to be in done in a particular sequence, because the later dumps depend on the earlier ones. Do NOT execute imports alphabetically.
    # formerly: filetypes
    disclosure_type = ['cn','cm','ccl','oth','pas2','indiv','oppexp']
    # data = {'indiv':'itcont'}
    # formerly: filenames
    disclosure_type_aliases = {'cn':'cn','ccl':'ccl','pas2':'itpas2','indiv':'itcont','oth':'itoth','oppexp':'oppexp','cm':'cm'}

    # list of disclosure_types that have edge imports
    has_edge_import = {'ccl','indiv','oth','pas2'}

    # list of disclosure_types that have entity imports
    has_node_import = {'cm','cn','indiv'}

    #store the zips in ./zips
    compressed_directory = os.path.join(os.curdir,'zips')

    def __init__(self, election_year, disclosure_type):

        super(FECDisclosureObject, self).__init__()
        
        with open('fec.config.json') as f:
            self.config = json.load(f)
            # print self.config
            self.neoClient = FECGraphClient(self.config['neo4j']['port'],self.config['neo4j']['username'], self.config['neo4j']['password'])


        self.election_year = election_year
    
        self.disclosure_type = disclosure_type
        
        # e.g. indiv16.zip
        self.compressed_name = self.disclosure_type + self.election_year + '.zip'

        # e.g. ./zips/indiv16.zip
        self.compressed_path = os.path.join(self.compressed_directory, self.compressed_name) 

        # member name is the filename that will be reflected in 
        # the manifest of the copmpressed disclosure
        self.member_name = self.disclosure_type_aliases[self.disclosure_type] + '.txt'

        # For now the directory structure of all downloads and extraction
        # is going to be implied in this class
        self._ensure_zip_dis()
        self._ensure_extracs_dir()

    # Make sure our directosy structure has ./zips and 
    def _ensure_zip_dir(self):
        self.zip_directory = os.path.join(os.curdir,'zips')
        if not os.path.isdir(self.zip_directory):
            os.mkdir(self.zip_directory)
        return True

    # Make sure our directory structure has ./zips/{disclosure_type}/
    def _ensure_extract_dir(self):
        self.extract_dir = os.path.join(self.zip_directory , self.disclosure_type)
        if not os.path.isdir(self.extract_dir):
            os.mkdir(self.extract_dir)
        return True

    # Main entry point for the object. Download, extract, sanitize, and load the disclosure
    def get_disclosure(self, force_download = False):
        if force_download or not self._extracted_disclosure_exists():
            self._download_compressed_disclosure()
        return None
             
    # Download the compressed disclosure
    def _download_compressed_disclosure(self):
        url = self.config['url_prefix'] + '20'+self.election_year+'/'+self.compressed_name
        #Download the file into the proper directory
        wget.download(
            url,
            self.compressed_directory
            )

    # Return existence of copmressed disclosure download.
    # e.g. ./zips/
    def _compressed_disclosure_exists(self):
        return os.path.isfile(self.compressed_path)

    # Unzip the disclosure
    def _extract_disclosure(self):
        zip_ref = zipfile.ZipFile(self.compressed_path, 'r')
        zip_ref.extract(member_name, extract_dir)
        # this is not namepaced by year yet.
        # e.g. ./zips/ccl/

    # Prepend the appropriate headers, located in ./headers/ to the beginning of the file 
    def _apply_headers(self.input_path, output_path):
        headers = open(os.path.join(os.curdir,'headers', self.filenames[filetype] + '-headers.txt'),'r').readline() 
        extract_handle = open(self.output_path, 'w')
        extract_handle.write(headers)
        extract_handle.writelines(open(os.path.join(extract_dir,member_name)))
        extract_handle.close()
    
    def _extracted_disclosure_exists():
        os.isfile(self.extract_path)

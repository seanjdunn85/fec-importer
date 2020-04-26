import wget, os, zipfile, datetime, sys, json
from FECGraphClient import FECGraphClient
from termcolor import colored
from shutil import copyfile
from dotenv import load_dotenv
load_dotenv()



update = '--update-current-year' in sys.argv or '-U' in sys.argv
verbose = '--verbose' in sys.argv or '-V' in sys.argv

## TODO : remove this ungodly hack.
fix = {
    "C00622357|\"D'MAC KINGDOM\" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||": 'C00622357|\"D\'MAC KINGDOM\" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||'
}


def verboseColoredPrint(message, color):
    if verbose:
        colored(message, color)
    else:
        return None


class FECDataManager(object):
    # the years that we're looking to import
    years = ['04', '06', '08', '10', '12', '14', '16', '18']

    # Filetypes need to be in done in a particular sequence
    # The later dumps depend on the earlier ones. Do NOT execute imports alphabetically.
    filetypes = ['cn', 'cm', 'ccl', 'oth', 'pas2', 'indiv', 'oppexp']

    # filenames = {'indiv':'itcont'}
    # these is a mapping between the filetype and filename. `indiv` file types correspond to `itcont` filenames
    filenames = {'cn': 'cn', 'ccl': 'ccl', 'pas2': 'itpas2', 'indiv': 'itcont', 'oth': 'itoth', 'oppexp': 'oppexp',
                 'cm': 'cm'}

    # whether the file has edges
    has_edge_import = {'ccl', 'indiv', 'oth', 'pas2'}

    # whether the file has nodes
    has_node_import = {'cm', 'cn', 'indiv'}

    # store the zips in ./zips
    zip_directory = os.getenv("DATA_STORAGE_DIR")
    # zip_directory = os.path.join(os.curdir, 'zips')

    """docstring for FECDataManager"""

    def __init__(self, update=True):

        super(FECDataManager, self).__init__()

        # Boolean whether to update the most recent election cycle
        self.update = update

        # Current year as string, ex: '18'
        self.current_year = datetime.date.today().strftime("%Y")[2:]

        with open('fec.config.json') as f:
            self.config = json.load(f)
            # print self.config
            self.neoClient = FECGraphClient(self.config['neo4j']['port'], self.config['neo4j']['username'],
                                            self.config['neo4j']['password'])

        # Ensure that the schema has the proper constraints
        with open('schema/fec.cypher') as schemaLines:
            lines = schemaLines.readlines()
            for line in lines:
                ##result = self.neoClient.graph.evaluate(line)
                print("""hello world""")

    # boolean true update the election cycle. Can only return true if the election year
    # being processed is the most recent.
    def updateCurrentCycle(self, year):
        return (self.update == True and self.year == self.current_year)

    # boolean true if the filetype contains entities
    def hasEdgeImport(self, filetype):
        return filetype in self.has_edge_import

    # boolean true if the filetype contains entities
    def hasNodeImport(self, filetype):
        return filetype in self.has_node_import

    # Main entry point. Begins the download and entry process into RDMS and Graph DB.
    def sync(self):
        for year in self.years:
            print(year)
            for filetype in self.filetypes:
                print(filetype)
                # see if the file is
                # ./zips/indiv-16.zip
                zipname = filetype + year + '.zip'
                zip_path = os.path.join(self.zip_directory, zipname)
                # Make sure namespaced directories exist
                # dir = ./zips/{filetype}/
                #
                extract_dir = os.path.join(self.zip_directory, filetype)

                if not os.path.isdir(extract_dir):
                    os.mkdir(extract_dir)

                if os.path.isfile(zip_path) and not (self.update == True and year == self.current_year):
                    print(zip_path + ' already exists on disk')
                    extract_name = self.filenames[filetype] + '-' + year + '.txt'
                    # ./zips/indiv/itcont-16.txt
                    extract_path = os.path.join(extract_dir, extract_name)

                    zip_ref = zipfile.ZipFile(zip_path, 'r')
                # print zip_ref.namelist()
                else:
                    if os.path.isfile(zip_path):
                        os.remove(zip_path)

                    print(zip_path + ' either does not exist on disk or is set to update. Downloading...')
                    url = self.config['url_prefix'] + '20' + year + '/' + zipname

                    # Download the file into the proper directors
                    wget.download(
                        url,
                        self.zip_directory
                    )

                # itcont.txt
                member_name = self.filenames[filetype] + '.txt'
                # itcont-16.txt
                extract_name = self.filenames[filetype] + '-' + year + '.txt'
                # ./zips/indiv/itcont-16.txt
                extract_path = os.path.join(extract_dir, extract_name)

                temp_path = os.path.join(extract_dir, extract_name + '.temp')

                zip_ref = zipfile.ZipFile(zip_path, 'r')
                # print zip_ref.namelist()

                if not os.path.isfile(extract_path) and not (self.update == True and year == self.current_year):
                    zip_ref.extract(member_name, extract_dir)
                    # The zip file has been extracted. Now do any character replacement needed for parse errors/
                    headers = open(os.path.join(os.curdir, 'headers', self.filenames[filetype] + '-headers.txt'),
                                   'r').readline()
                    extract_handle = open(extract_path, 'w')
                    extract_handle.write(headers)

                    extract_handle.writelines(open(os.path.join(extract_dir, member_name)))
                    extract_handle.close()

                copyfile(extract_path, temp_path)

                temp_handle = open(temp_path)

                replace_string = 'C00622357|\\"D\'MAC KINGDOM\\" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||'

                os.remove(extract_path)

                extracted_and_fixed_handle = open(extract_path, 'w')

                with open(temp_path) as file:
                    for line in file:
                        if line[:9] == "C00622357":
                            print('replacing...')
                            extracted_and_fixed_handle.write(replace_string)
                        else:
                            extracted_and_fixed_handle.write(line)

                if self.hasNodeImport(filetype):
                    cypherFilePath = './import-cyphers/' + self.filenames[filetype] + '-import-cypher'
                    with open(cypherFilePath, 'r') as myfile:
                        cypher_query = myfile.read().replace('\n', ' ')
                        cypher_query = cypher_query % (filetype, self.filenames[filetype], year)
                        verboseColoredPrint(cypher_query, 'blue')
                        try:
                            result = self.neoClient.graph.cypher.execute(cypher_query)
                        except Exception as e:
                            print(colored(e, 'red'))
                        else:
                            pass
                        finally:
                            pass

                if self.hasNodeImport(filetype):
                    sqlFilePath = './import-sql/' + self.filenames[filetype] + '-import.sql'
                    with open(cypherFilePath, 'r') as myfile:
                        cypher_query = myfile.read().replace('\n', ' ')
                        cypher_query = cypher_query % (filetype, self.filenames[filetype], year)
                        verboseColoredPrint(cypher_query, 'blue')
                        try:
                            result = self.neoClient.graph.cypher.execute(cypher_query)
                        except Exception as e:
                            print(colored(e, 'red'))
                        else:
                            pass
                        finally:
                            pass

                if self.hasEdgeImport(filetype):
                    cypherFilePath = './import-cyphers/' + self.filenames[filetype] + '-edge-import-cypher'
                    with open(cypherFilePath, 'r') as myfile:
                        cypher_query = myfile.read().replace('\n', ' ')
                        cypher_query = cypher_query % (filetype, self.filenames[filetype], year)
                        verboseColoredPrint(cypher_query, 'blue')
                        try:
                            result = self.neoClient.graph.cypher.execute(cypher_query)
                        except Exception as e:
                            print(colored(e, 'red'))
                        else:
                            pass
                        finally:
                            pass

    def interpolateCypher(cypher, params):
        return cypher % params


dataManager = FECDataManager(update)
dataManager.sync()

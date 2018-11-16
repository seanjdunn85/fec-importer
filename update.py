import wget, os, zipfile, datetime, sys, json
from FECGraphClient import FECGraphClient
from termcolor import colored
from shutil import copyfile

update = '--update-current-year' in sys.argv or '-U ' in  sys.argv

# Get the current year so we can update the current election cycle
current_year = datetime.date.today().strftime("%Y")[2:]

fix ={
	"C00622357|\"D'MAC KINGDOM\" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||":'C00622357|\"D\'MAC KINGDOM\" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||'
}




class FECDataManager(object):

	#the years that we're looking to import
	years = ['04','06','08','10','12','14','16','18']

	#filetypes need to be in done in a particular sequence, because the later dumps depend on the earlier ones. Do NOT execute imports alphabetically.
	filetypes = ['cn','cm','ccl','oth','pas2','indiv','oppexp']
	
	# filenames = {'indiv':'itcont'}
	filenames = {'cn':'cn','ccl':'ccl','pas2':'itpas2','indiv':'itcont','oth':'itoth','oppexp':'oppexp','cm':'cm'}
	
	# whether the file has edges
	has_edge_import = {'ccl','indiv','oth','pas2'}
	
	# whether the file has nodes
	has_node_import = {'cm','cn','indiv'}
	
#	store the zips in ./zips
	zip_directory = os.path.join(os.curdir,'zips')

	"""docstring for FECDataManager"""
	def __init__(self, update = True):
		super(FECDataManager, self).__init__()
		self.update = update
		self.current_year  =  datetime.date.today().strftime("%Y")[2:]

		with open('fec.config.json') as f:
			self.config = json.load(f)
			print self.config
			self.neoClient = FECGraphClient(self.config['neo4j']['port'],self.config['neo4j']['username'], self.config['neo4j']['password'])
		# ensure that the schema has the proper constraints
		with open('schema/fec.cypher') as schemaLines:
			lines =  schemaLines.readlines()
			for line in lines:
				result = self.neoClient.graph.cypher.execute(line)
				print result

	 

	def updateCurrentCycle(self, year):
		return (self.update == True and self.year == self.current_year)


	def hasEdgeImport(self, filetype):
		return filetype in self.has_edge_import

	def hasNodeImport(self, filetype):
		return filetype in self.has_node_import

	def sync(self):
		for year in self.years:
			print year
			for filetype in self.filetypes:
				print filetype				
				# see if the file is 
				#./zips/indiv-16.zip
				zipname = filetype+year+'.zip'
				zip_path = os.path.join(self.zip_directory,zipname)
				# Make sure namespaced directories exist
				# dir = ./zips/{filetype}/
				# 
				extract_dir = os.path.join(self.zip_directory , filetype)

				if not os.path.isdir(extract_dir):
					os.mkdir(extract_dir)

				if os.path.isfile(zip_path) and not (self.update == True and year == current_year):
					print zip_path + ' already exists on disk'
					extract_name = self.filenames[filetype] + '-' + year + '.txt' 
					#./zips/indiv/itcont-16.txt
					extract_path = os.path.join(extract_dir, extract_name)


					zip_ref = zipfile.ZipFile(zip_path, 'r')
					# print zip_ref.namelist()
				else:
					if os.path.isfile(zip_path):
						os.remove(zip_path)

					print zip_path + ' either does not exist on disk or is set to update. Downloading...'
					url = url_prefix + '20'+year+'/'+zipname

					wget.download(
						url,
						self.zip_directory
						)


				#itcont.txt
				member_name =  self.filenames[filetype] + '.txt'
				# itcont-16.txt
				extract_name = self.filenames[filetype] + '-' + year + '.txt' 
				#./zips/indiv/itcont-16.txt
				extract_path = os.path.join(extract_dir, extract_name)

				temp_path = os.path.join(extract_dir, extract_name + '.temp')


				zip_ref = zipfile.ZipFile(zip_path, 'r')
				# print zip_ref.namelist()
				
				if not os.path.isfile(extract_path) and not (self.update == True and year == current_year):
					zip_ref.extract(member_name, extract_dir)
					#The zip file has been extracted. Now do any character replacement needed for parse errors/
					headers = open(os.path.join(os.curdir,'headers', self.filenames[filetype] + '-headers.txt'),'r').readline() 
					extract_handle = open(extract_path, 'w')
					extract_handle.write(headers)

					extract_handle.writelines(open(os.path.join(extract_dir,member_name)))
					extract_handle.close()
				
				copyfile(extract_path, temp_path)
				
				temp_handle = open(temp_path)

				replace_string = 'C00622357|\\"D\'MAC KINGDOM\\" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||'

				os.remove(extract_path)

				extracted_and_fixed_handle = open(extract_path,'w')

				with open(temp_path) as file:
					for line in file:
						# print line
						if line[:9] == "C00622357":
							# print line
							# print bad_string
							# basl = (line == bad_string)
							# print basl
							# print type(basl)
							# print type(bad_string)
							# print type(line)
							# print colored(bad_string,'red')
							print 'replacing...'
							extracted_and_fixed_handle.write(replace_string)
						else:
							extracted_and_fixed_handle.write(line)
							

						if line in fix:
							print colored(
								'C00622357|"D\'MAC KINGDOM" THE GOOD NEWS OF HEALING & UNIFYING OUR GREAT NATION|KAREN D MACK|7211 CRANE AVE APT# 114||JACKSONVILLE|FL|32216|P|P||Q|||','red')
							print colored(line,'red')
							print line
							print fix[line]

				if self.hasNodeImport(filetype):
					cypherFilePath = './import-cyphers/'+ self.filenames[filetype] + '-import-cypher'
					with open(cypherFilePath, 'r') as myfile:
						cypher_query = myfile.read().replace('\n', ' ')
						cypher_query = cypher_query % (filetype,self.filenames[filetype], year)
						print cypher_query
						try:
							result = self.neoClient.graph.cypher.execute(cypher_query)
						except Exception as e:
							print colored(e, 'red')
						else:
							pass
						finally:
							pass

				if self.hasNodeImport(filetype):
					sqlFilePath = './import-sql/'+ self.filenames[filetype] + '-import.sql'
					with open(cypherFilePath, 'r') as myfile:
						cypher_query = myfile.read().replace('\n', ' ')
						cypher_query = cypher_query % (filetype,self.filenames[filetype], year)
						print cypher_query
						try:
							result = self.neoClient.graph.cypher.execute(cypher_query)
						except Exception as e:
							print colored(e, 'red')
						else:
							pass
						finally:
							pass


				if self.hasEdgeImport(filetype):
					cypherFilePath = './import-cyphers/'+ self.filenames[filetype] + '-edge-import-cypher'
					with open(cypherFilePath, 'r') as myfile:
						cypher_query = myfile.read().replace('\n', ' ')
						cypher_query = cypher_query % (filetype,self.filenames[filetype], year)
						print cypher_query
						try:
							result = self.neoClient.graph.cypher.execute(cypher_query)
						except Exception as e:
							print colored(e, 'red')
						else:
							pass
						finally:
							pass

	def interpolateCypher(cypher, params):
		return cypher % params

dataManager = FECDataManager(update)
dataManager.sync()
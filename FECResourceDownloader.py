import wget, os, zipfile, datetime, sys

class FECResourceDownloader(object):
	years = ['04','06','08','10','12','14','16','18']

	filetypes = {'cn','ccl','oth','pas2','indiv','oppexp'}

	filenames = {'cn':'cn','ccl':'ccl','pas2':'itpas2','indiv':'itcont','oth':'itoth','oppexp':'oppexp'}

	zip_directory = os.path.join(os.curdir,'zips')
	
	# Get the current year so we can update the current election cycle
	current_year = datetime.date.today().strftime("%Y")[2:]

	#Whether or not to update the current year
	update = False

	"""FECResourceDownloader"""
	def __init__(self):
		super(FECResourceDownloader, self).__init__()
		# self.arg = arg


	def getAll(self, update, dontUpdate = None):
		
		print '**locals()'
		
		print locals()

		for year in years:
			print year
			for filetype in filetypes:
				zipname = filetype+year+'.zip'
				zip_path = os.path.join(zip_directory,zipname)
				if os.path.isfile(zip_path) and not (update == True and year == current_year):
					print 'file exists'
				else:
					url = 'https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/20'+year+'/'+zipname

					wget.download(
						url,
						zip_directory
						)
				
				extract_dir = os.path.join(zip_directory , filetype)

				if not os.path.isdir(extract_dir):
					os.mkdir(extract_dir)

				zip_ref = zipfile.ZipFile(zip_path, 'r')

				print zip_ref.namelist()

				member_name =  filenames[filetype] + '.txt'
				
				extract_name = filenames[filetype] + '-' + year + '.txt' 

				extract_path = os.path.join(extract_dir, extract_name)

				zip_ref.extract(member_name, extract_dir)

				headers = open(os.path.join(os.curdir,'headers', filenames[filetype] + '-headers.txt'),'r').readline() 

				print headers 
				extract_handle = open(extract_path, 'w')
				extract_handle.write(headers)
				extract_handle.writelines(open(os.path.join(extract_dir,member_name)))


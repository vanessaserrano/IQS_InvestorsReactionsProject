import os
import datetime
import sys 
import json
import excelExport
from shutil import copyfile

print('/nDo you want to update Maestro?\n')
print('1: Yes\n')
print('2: No\n')

sel = input('Choose (1 or 2): ')

#PATH Definition
JPATH = os.path.join(os.path.dirname(sys.path[0]),'Json')
MPATH = os.path.join(os.path.dirname(sys.path[0]),'Json', 'Maestro.json')

if '1' in sel:
	
	#If Maestro is no Found then It would be Created
	try: 
		copyfile(MPATH, os.path.join(os.path.dirname(sys.path[0]),'Backup', 'Maestro - ' + datetime.datetime.now().strftime("%Y-%m-%d") + ' .json'))
		print('\nBackup done\n')
		with open(MPATH, 'r') as f:
			datM = json.load(f)
	except: 
	
		outfile = open(MPATH, 'w')
		update = [[],[]]
		json.dump(update, outfile)
		outfile.close()
		with open(MPATH, 'r') as f:
			datM = json.load(f)
		print('\nMaestro was not Found\n')
		print('A new Maestro was Created\n')
		print('Check possibles Errors.Restablish Backup if It would be necessary\n')

	maestro = datM[0]
	load = datM[1]
	
	#Mestro will only update those references that are not yet in Maestro
	for dirJson in os.listdir(JPATH): 
		
		ref = dirJson[0:16]
	
		if 'Maestro' not in dirJson:
			if ref not in load:
				file = open(os.path.join(os.path.dirname(sys.path[0]),'Json', dirJson), 'r')
				data = json.load(file)
				maestro.extend(data)
				load.append(ref)
				print(ref + ' Updated\n')
			
	outfile = open(MPATH, 'w')	
	update = [maestro, load]
	json.dump(update, outfile)
	outfile.close()
	
	print('\nMaestro Updated\n')
	
else:
	print('\nMaestro was not updated\n')


print('Do you want to update an Excel?\n')
print('1: Yes\n')
print('2: No\n')

#Update a Companie Excel
sel = input('Choose (1 or 2): ')

if '1' in sel: 
	print('\nWhich Excel do you want to update?\n')
	ID = input('Company ID: ')
	with open(MPATH, 'r') as f: 
		file = json.load(f)
	exc = excelExport.JsonToExcel(file, ID)
	exc.export()
	print('\nExcel Correctly Updated\n')
else:
	print('\nYou did not updated any Excel\n')
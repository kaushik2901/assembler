import sys
import re

addressSymbols = []

variables = []

output = []

mriDirect = {
	'AND': 0x1,
	'ADD': 0x2,
	'LDA': 0x3,
	'STA': 0x4,
	'BUN': 0x5,
	'BSA': 0x6,
	'ISZ': 0x7,
}

mriInDirect = {
	'AND': 0x8,
	'ADD': 0x9,
	'LDA': 0xA,
	'STA': 0xB,
	'BUN': 0xC,
	'BSA': 0xD,
	'ISZ': 0xE,
}

registerRef = {
	'CLA': 0x7800,
	'CLE': 0x7400,
	'CMA': 0x7200,
	'CME': 0x7100,
	'CIR': 0x7080,
	'CIL': 0x7040,
	'INC': 0x7020,
	'SPA': 0x7010,
	'SNA': 0x7008,
	'SZA': 0x7004,
	'SZE': 0x7002,
	'HLT': 0x7001,
}

ioRef = {
	'INP': 0xF800,
	'OUT': 0xF400,
	'SKI': 0xF200,
	'SKO': 0xF100,
	'ION': 0xF080,
	'IOF': 0xF040,
}

def findMri(value):
	for i in addressSymbols:
		if value == i[0]:
			return i[1]
	return None

def FirstPass(File):
	lineNO = 1
	lc = 0
	for line in File:
		line = line[:-1]
		if 'ORG' in line:
			if ',' in line:
				print("ERROR on line "+ str(lineNO))
				exit(1)
			try:
				temp, ads = line.split(" ")
				a = re.findall('[^0-9]', ads[:-1])
				if len(a) > 0:
					print("Invalid Origin : line no. "+ str(lineNO))
					exit(1)
				lc = int(ads)
			except ValueError:
				lc = 0
			except Exception as e:
				print("ERROR on line "+ str(lineNO) + "\n" + str(e))
				exit(1)
		elif 'END' in line:
			if ',' in line:
				print("ERROR on line "+ str(lineNO))
				exit(1)
		elif ',' in line:
			try:
				temp, inst = line.split(",")
			except Exception as e:
				print("ERROR on line "+ str(lineNO))
				print(str(e))
				exit(1)
			if len(temp) > 3:
				print("Label must be of 3 letters : line no. "+ str(lineNO))
				exit(1)

			a = re.findall('[^A-Z]', temp[0])
			if len(a) > 0:
				print("Invalid Label : line no. "+ str(lineNO))
				exit(1)
			a = re.findall('[^A-Z0-9]', temp[1:])
			if len(a) > 0:
				print("Invalid Label : line no. "+ str(lineNO))
				exit(1)

			label = temp
			addressSymbols.append([label, lc])
			lc += 1
		lineNO += 1
	return

def SecondPass(File):
	lineNO = 0
	lc = 0

	for line in File:
		if "ORG" in line:
			try:
				temp, ads = line.split(" ")
				a = re.findall('[^0-9]', ads[:-1])
				if len(a) > 0:
					print("Invalid Origin : line no. "+ str(lineNO))
					exit(1)
				lc = int(ads)
			except ValueError:
				lc = 0
			except Exception as e:
				print("ERROR on line "+ str(lineNO) + "\n" + str(e))
				exit(1)
		elif 'END' in line:
			pass
		elif 'DEC' in line:
			try:
				temp, ads = line.split(" ")
				a = re.findall('[^0-9]', ads[:-1])
				if len(a) > 0:
					print("Invalid Address : line no. "+ str(lineNO))
					exit(1)
				val = int(ads)
				val = bin(val)
				val = val[2:]
				val = val.zfill(16)
				variables.append([val, lc])
			except ValueError:
				lc = 0
			except Exception as e:
				print("ERROR on line "+ str(lineNO) + "\n" + str(e))
				exit(1)
			lc += 1
		elif 'HEX' in line:
			try:
				temp, ads = line.split(" ")
				a = re.findall('[^0-9A-Z]', ads[:-1])
				if len(a) > 0:
					print("Invalid Address : line no. "+ str(lineNO))
					exit(1)
				val = int(ads, 16)
				val = bin(val)
				val = val[2:]
				val = val.zfill(16)
				variables.append([val, lc])
			except ValueError:
				lc = 0
			except Exception as e:
				print("ERROR on line "+ str(lineNO) + "\n" + str(e))
				exit(1)
			lc += 1
		elif ',' in line:
			try:
				temp, inst = line.split(",")
			except Exception as e:
				print("ERROR on line "+ str(lineNO))
				print(str(e))
				exit(1)

			if 'DEC' in inst:
				try:
					temp, ads = line.split(" ")
					a = re.findall('[^0-9]', ads[:-1])
					if len(a) > 0:
						print("Invalid Address : line no. "+ str(lineNO))
						exit(1)
					val = int(ads)
					val = bin(val)
					val = val[2:]
					val = val.zfill(16)
					variables.append([val, lc])
				except ValueError:
					lc = 0
					print(lc)
				except Exception as e:
					print("ERROR on line "+ str(lineNO) + "\n" + str(e))
					exit(1)
				lc += 1
			elif 'HEX' in inst:
				try:
					temp, ads = line.split(" ")
					a = re.findall('[^0-9A-Z]', ads[:-1])
					if len(a) > 0:
						print("Invalid Address : line no. "+ str(lineNO))
						exit(1)
					val = int(ads, 16)
					val = bin(val)
					val = val[2:]
					val = val.zfill(16)
					variables.append([val, lc])
				except ValueError:
					lc = 0
					print(lc)
				except Exception as e:
					print("ERROR on line "+ str(lineNO) + "\n" + str(e))
					exit(1)
				lc += 1
			else:
				line = inst
				values = line.split(" ")
				if str(values[0]) in list(mriDirect.keys()):
					#Memory ref
					if len(values) > 3:
						print("Error : line no. "+ str(lineNO))
						exit(1)
					if len(values) == 3 and values[2] == 'I':
						if str(values[0]) in list(mriInDirect.keys()):
							try:
								ins = mriInDirect[values[0]]
								binValue = bin(ins)[2:]
								binValue = binValue.zfill(4)
							except Exception as e:
								print("Error : line no. "+ str(lineNO) + " " + e)
								exit(1)
						add = values[1]
						loc = findMri(add)
						binLoc = bin(loc)[2:]
						binLoc = binLoc.zfill(12)
						output.append(binValue + binLoc)
					if len(values) == 2:
						if str(values[0]) in list(mriDirect.keys()):
							try:
								ins = mriDirect[values[0]]
								binValue = bin(ins)[2:]
								binValue = binValue.zfill(4)
							except Exception as e:
								print("Error : line no. "+ str(lineNO) + " " + e)
								exit(1)

						add = values[1][:-1]
						loc = findMri(add)
						binLoc = bin(loc)[2:]
						binLoc = binLoc.zfill(12)
						output.append(binValue + binLoc)

					lc += 1

				elif str(values[0]) in list(registerRef.keys()):
					#Reg ref
					if len(values) > 1:
						print("Error : line no. "+ str(lineNO))
						exit(1)

					try:
						instruction = registerRef[values[0]]
						binValue = bin(instruction)[2:]
						binValue = binValue.zfill(16)
						output.append(binValue)
					except Exception as e:
						print("Error : line no. "+ str(lineNO) + " " + e)
						exit(1)

					lc += 1

				elif str(values[0]) in list(ioRef.keys()):
					#io ref
					if len(values) > 1:
						print("Error : line no. "+ str(lineNO))
						exit(1)
					try:
						instruction = ioRef[values[0]]
						binValue = bin(instruction)[2:]
						binValue = binValue.zfill(16)
						output.append(binValue)
					except Exception as e:
						print("Error : line no. "+ str(lineNO) + " " + e)
						exit(1)
					lc += 1
		else:
			values = line[:-1].split(" ")
			if str(values[0]) in list(mriDirect.keys()):
				#Memory ref
				if len(values) > 3:
					print("Error : line no. "+ str(lineNO))
					exit(1)
				if len(values) == 3 and values[2] == 'I':
					if str(values[0]) in list(mriInDirect.keys()):
						try:
							ins = mriInDirect[values[0]]
							binValue = bin(ins)[2:]
							binValue = binValue.zfill(4)
						except Exception as e:
							print("Error : line no. "+ str(lineNO) + " " + e)
							exit(1)
					add = values[1]
					loc = findMri(add)
					binLoc = bin(loc)[2:]
					binLoc = binLoc.zfill(12)
					output.append(binValue + binLoc)
				if len(values) == 2:
					if str(values[0]) in list(mriDirect.keys()):
						try:
							ins = mriDirect[values[0]]
							binValue = bin(ins)[2:]
							binValue = binValue.zfill(4)
						except Exception as e:
							print("Error : line no. "+ str(lineNO) + " " + e)
							exit(1)
					add = values[1]
					loc = findMri(add)
					binLoc = bin(loc)[2:]
					binLoc = binLoc.zfill(12)
					output.append(binValue + binLoc)
				lc += 1

			elif str(values[0]) in list(registerRef.keys()):
				#Reg ref
				if len(values) > 1:
					print("Error : line no. "+ str(lineNO))
					exit(1)

				try:
					instruction = registerRef[values[0]]
					binValue = bin(instruction)[2:]
					binValue = binValue.zfill(16)
					output.append(binValue)
				except Exception as e:
					print("Error : line no. "+ str(lineNO) + " " + e)
					exit(1)

				lc += 1

			elif str(values[0]) in list(ioRef.keys()):
				#io ref
				if len(values) > 1:
					print("Error : line no. "+ str(lineNO))
					exit(1)

				try:
					instruction = ioRef[values[0]]
					binValue = bin(instruction)[2:]
					binValue = binValue.zfill(16)
					output.append(binValue)
				except Exception as e:
					print("Error : line no. "+ str(lineNO) + " " + e)
					exit(1)

				lc += 1
	return


if __name__ == "__main__":

	if len(sys.argv) != 3:
		print("Required exact 2 arguments")
		print("python "+str(sys.argv[0])+" <--source file--> <--output file-->")
		exit(0)

	fileName = str(sys.argv[1])
	outputName = str(sys.argv[2])

	if outputName[len(outputName)-2:] != '.o':
		outputName = outputName + ".o"

	try:
		File = open(fileName, "r")
	except:
		print("No file found")
		exit(404)
	FirstPass(File)

	try:
		File = open(fileName, "r")
	except:
		print("No file found")
		exit(404)

	SecondPass(File)

	try:
		outFile = open(outputName, "w")
	except Exception as e:
		print("Error : " + str(e))
		exit(404)

	for line in output:
		outFile.write(line + "\n")

	outFile.write("\n")

	for line in variables:
		outFile.write(line[0] + "\n")

	outFile.close()
	File.close()

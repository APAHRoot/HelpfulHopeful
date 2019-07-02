
import os
import sys
import csv
import time
import operator

#Author: Nathaniel Root
#Purpose: for splitting up large UNSORTED CSV files based on a category.
#		For instance, if working with a file containing data on an entire state
#		you can run the data through this program and split it up based on county,
#		assuming you know which column that information is stored.
#
#Python version: 3.6
#
#How to run: if you have python 3 installed, you should be able to simply double click
#the file and the program prompts should initiate.
#
#Run time: When run on 4.5 GB CSV, splitting into about 20 or so files, program execution took around 15-20 minutes.
#
#Date modified: July 2, 2019

def main():
	#Main provides the user interaction portion of the program and hands off data to the splitter function
	print(" ")
	print("Hello! I am going to sort your large CSV file into smaller individual CSV files. What is the file path?")
	print("[type \"exit\" to exit]")
	filepath = input("Filepath: ")
	if filepath == "exit":
		print("Exiting")
		time.sleep(.5)
		exit()
	print("Looking for your file now")
	
	#this section checks whether or not the user provided an actual file path
	inputType = whatismypath(filepath)
	if inputType == "dir":
		print("You entered a directory path, not a filepath.")
		time.sleep(2)
		main()
	elif inputType == "file":
		fNcomponents = str(filepath).split(".")
		if fNcomponents[len(fNcomponents)-1] !="csv":
			print("I cannot operate on a non-csv file. Please either double check the file path, convert the file to csv, OR modify this program to cope with non-csv file formats")
			print("You gave me a "+str(fNcomponents[len(fNcomponents)-1]))
			main()
		
		curDir =str(filepath[0:filepath.rfind("\\")])
		os.chdir(curDir)
		try:
			#creates a temporary directory to store split files
			os.mkdir("tempForSort")
		except:
			print("Tried to create a temporary directory and failed. A directory named tempForSort already exists in the same directory as the file you chose. Please delete or rename that directory and try again.")
			exit()
		
		#request user provide the column that will determine what to split the csv files up by
		sortColumn = input("\nFile Located! \nWhat Column would you like the data split up by? Enter any whole number 1 through the number of columns in the file to indicate the column. \nColumn Number: ")
		
		if sortColumn == "exit":
			#allow for user to exit using exit
			print("Exiting")
			time.sleep(.5)
			exit()
		else:
			#check that user provided an integer, then round and make sure that integer is positive
			try:
				sortColumn = abs(round(int(sortColumn)))-1
			except:
				print("User did not supply a valid input for the column number. System will now exit. Reload and try again.")
				time.sleep(4)
				exit()
		
		#call the splitter function
		filelist = splitter(filepath, str(curDir + "\\tempForSort"), ',',True, sortColumn)
		print("\n\nSplitting complete, the following files have been generated:")
		filelist = sorted(filelist)
		for fil in filelist:
			print(str(fil))
		t = input("\nHit enter to end program")
		
	elif inputType == "err":
		print("File Not Found")
		print("User wrote: " + str(filepath))
		time.sleep(2)
		main()


def splitter(filepath, output_path, delim=',', useHeaders = True, splitbycol = 0):
	#take a filepath, optional delimiter, output path,
	#whether to retain headers, and which column to split by (defaults to first)
	#Split it into different files based on the column identified.


	with open(filepath, 'r') as source:
		reader = csv.reader(source, delimiter=delim)
		header_row = next(reader)
		#creates the first file based on the first category in the column (e.g.
		#by county or by icecream flavor)
		current_category = "Unnamed"
		#checkExisting is used to keep track of which files have been created
		checkExisting=[]
		#start is used to check if the program is creating its first file
		start = 1	
		for i, row in enumerate(reader):
			
			current_category = str(row[splitbycol])
			
			if start ==1:
				currentOutPath = output_path + "\\" + str(current_category) + ".csv"
				currentOutWrite = csv.writer(open(currentOutPath,'w',newline=''), delimiter = delim)
				start = 0
				checkExisting.append(current_category)
				if useHeaders:
					currentOutWrite.writerow(header_row)
					print("")
					print("")
					print("Creating: " + str(current_category) +".csv")
						
			elif current_category != prev_category:
				if current_category in checkExisting:
					#if the category is included in checkExisting, that means the file for this category already exists.
					#open the file in append mode and notify CMD what is being worked on
					currentOutPath = output_path + "\\" + str(current_category) + ".csv"
					currentOutWrite = csv.writer(open(currentOutPath,'a',newline=''), delimiter = delim)
					print("")
					print("")
					print("Now working on: " + str(current_category) +".csv")
				else:
					#if the category is no in checkExisting, then a new file needs to be opened in write mode
					#Determine if headers should be included
					#add the category to checkExisting
					currentOutPath = output_path + "\\" + str(current_category) + ".csv"
					currentOutWrite = csv.writer(open(currentOutPath,'w',newline=''), delimiter = delim)
					checkExisting.append(current_category)
					if useHeaders:
						currentOutWrite.writerow(header_row)
						print("")
						print("")
						print("Creating: " + str(current_category) +".csv")
			
			currentOutWrite.writerow(row)
			#status indicator, simply prints periods to the prompt screen to show that the program is working
			if i%800 == 0:
				print("    ",end ="\r", flush = True)
				print("    ",end ="\r", flush = True)
			elif i%200 == 0:
				print(".", end ="", flush = True)
			
			i += 1
			prev_category = current_category
			
			
	source.close()
	return checkExisting

def whatismypath(dirfilepath):
	# given a string representing a path, function returns
	# a str "dir" if directory
	# a str "file" if a file
	# and a str "err" if neither
	
	if os.path.isdir(dirfilepath) == True:
		return "dir"
	elif os.path.isfile(dirfilepath) == True:
		return "file"
	else:
		return "err"

	
	

#what to do when the program is initiated
main()
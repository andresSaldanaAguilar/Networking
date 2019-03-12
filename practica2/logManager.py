import os
def log(toWrite):

	try:  
		os.mkfile("log.txt")
	except OSError:  
		print ("Creation of the directory %s failed / Already Exists" % k)
	else:  
		print ("Successfully created the directory %s " % k)
	f= open("log.txt","w+")

	file.write("Hello World") 
	file.write("This is our new text file") 
	file.write("and this is another line.") 
	file.write("Why? Because we can") 
	 
	file.close() 

def main():
	log()
	
	
    	

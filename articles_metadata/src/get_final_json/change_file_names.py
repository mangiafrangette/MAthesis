# importing os module 
import os 

path = "../data/xml_files/dhq_xml"
# Function to rename multiple files 
for file_name in os.listdir(path): 
	os.rename(os.path.join(path, file_name), os.path.join(path, f'dqh_{file_name}')) 
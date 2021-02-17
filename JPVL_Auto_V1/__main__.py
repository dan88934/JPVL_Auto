from f_input import collect_user_input, input_type
from file_processing import process_file 
from doc_create import create_vocab_list
from PIL import UnidentifiedImageError
from zipfile import BadZipFile
import sys



#1. ===Collect user input (title, images)===
try:
    collect_user_input()
except AttributeError:
    print('Program was closed before input was selected')
    sys.exit(1)

#2. ===Process images or docs===
try:
    process_file()
except UnidentifiedImageError:
    print('Error - File does not match selected file type (not a recognized image)') 
    sys.exit(1)
except BadZipFile:
    print('Error - File does not match selected file type (not a document)') 
    sys.exit(1)

#3. ===Create document based on images===
create_vocab_list()






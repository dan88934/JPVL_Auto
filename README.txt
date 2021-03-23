README

============
Description:
============

JPVL_Auto is an application which generates vocabulary lists for Japanese language texts. 
It takes image(s) (.jpg or .png) or documents(s) (.docx) as input and will scan these files for Japanese words. 
The application will then generate a word document with a table containing the reading (hiragana or katakana) and the english definition(s) of all the words in the input file. See 'Output Examples' folder for an example of what this looks like.

There are some images and documents you can use to test the program in the 'Sample Images' and 'Sample Documents' folder.

The program contains a customised version of the Jamdict package (Japanese-to-English dictionary for Python). However, the regular set up process for this package will also need to be followed, see details below.

============
Installation:
============

1. Install tesseract and ensure that the tesseract executable is in '/usr/local/Cellar/tesseract/'

2. Create a virtual environemnt and then install this projects dependencies (in the requirements.txt) in it.

3. Follow the installation guidance for Sudachipy on https://pypi.org/project/SudachiPy/ (the x files can be found in the x folder in this repository)

4. Follow the install instructions for Jamdict on https://pypi.org/project/jamdict/ (the x files can be found in the x folder in this repository)


============
Usage:
============


The program should be ran as a package (or from the __main__.py file). 

The Program has a GUI which will open when the program runs.

Output documents will be placed in this folder (JPVL_Auto).

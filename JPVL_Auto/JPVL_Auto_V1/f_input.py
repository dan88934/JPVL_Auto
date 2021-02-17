import time
import PySimpleGUI as sg

title = []
input_files = []
input_type = []
def collect_user_input():
    sg.theme('Dark Blue 3')  
    layout = [
            [sg.Text('Title', size=(15, 1)), sg.InputText(), sg.Text('1. Enter a title for your vocabulary list.')],
            [sg.Text('Input type', size=(15, 1)), sg.Combo(['Document', 'Image']),sg.Text('2. Select type of file')],
            [sg.Text('Select Files', size=(15, 1)), sg.Input(key='_FILES_',), sg.FilesBrowse(
                file_types=("*.jpg", "*.png", '*.docx')), sg.Text('3. Select file(s) (must be same filetype).')],  # file_types=("*.jpg", "*.png"), takes multiple images
            [sg.OK()]]

    window = sg.Window('JPVL Auto', layout)
    event, values = window.read() #'event' is required here, contrary to what linting might say 
    title.append(values[0])
    files = values['_FILES_'].split(';') #files this var + if input type img lauch img_processing on file or if doc launch doctprocessing
    for item in files:
        input_files.append(item)
    window.close()
    print(files)
    input_type.append(values[1])
    print(input_type)


  
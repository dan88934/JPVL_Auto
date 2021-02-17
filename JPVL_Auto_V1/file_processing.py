import pytesseract
import pykakasi
from sudachipy import tokenizer
from sudachipy import dictionary 
from JPVL_jamdict import Jamdict #Must import from the customised version of Jamdict included in this package, not regular version
from f_input import input_files, input_type
import docx2txt
import re
import sys
from decorators import measure
try:
    from PIL import Image
except ImportError:
    import Image
tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1'
tokenizer_obj = dictionary.Dictionary().create()
kks = pykakasi.kakasi()
conv = kks.getConverter()
jmd = Jamdict()

original_words = [] #Words for side 1 will be put in here  
kana_and_eng_def = [] #Words for side 2 will be put in here

combined = [] #the loop will place all the words from each of the images passed in in here when it concatinates the list of words for each image together


#1. ===Define functions===
def get_japanese_only(context): #Here we remove all non-Japanese (excluding Chinese) characters from the string
    filtrate = re.compile(u'[^\u4E00-\u9FA5\u3040-\u309f\u30A0-\u30FF]')  #These are the unicode ranges for CJK, Hiragana and Katanaka (all characters that do not fall into these groups are excluded)
    context = filtrate.sub(r'', context)
    return context


def tokenize_into_words(string): #Takes a string of Japanese-only text and turns it into a list of words (and some irrelevant hiragana and karakana we will remove later)
    mode = tokenizer.Tokenizer.SplitMode.A
    tokenized_list = [m.dictionary_form() for m in tokenizer_obj.tokenize(string, mode)]
    # print(f'Tokenized list of words - {tokenized_list}')
    return tokenized_list

def list_concat(master_list): # This turns our multiple lists (one for each image) into a single list which can then be iterated over
    for item in master_list:
        combined.append(item)
    return combined

def remove_duplicate_items(input_list): #This removes duplicate items from our list by turning it into a dictionary and then converting it back again
    duplicates_removed_list = list(
            dict.fromkeys(input_list))
    return duplicates_removed_list
        # filtered_words = duplicates_removed_list

def remove_irrelevant_characters(input_list): #This removes some verb components and any random kanji which tend to occur and have no meaning on their own (e.g. ます)
    unwanted_particles_etc = {'ます','引', 'って'}  #引 appears in the list sometimes when it is not actually in the image
    unwanted_particles_removed_list = [item for item in input_list if item not in unwanted_particles_etc] #We use a list comprehension to remove them
    return unwanted_particles_removed_list

def remove_single_katakana(input_list):
    single_katakana = {'ア','イ','ウ','エ','オ','カ','キ','く','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ',
    'ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ヲ'} #All commonly used katakana
    single_katanaka_removed_list = [item for item in input_list if item not in single_katakana] 
    return single_katanaka_removed_list

def remove_single_hiragana(input_list):
    single_hiragana = {'あ','い','う','え','お','か','き','く','け','こ','が','ぎ','ぐ','げ','ご','さ','し','す','せ','そ','ざ','じ',
    'ず','ぜ','ぞ','た','ち','つ','て','と','だ','ぢ','づ','で','ど','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ば','び','ぶ',
    'べ','ぼ','ぱ','ぴ','ぷ','ぺ','ぽ','ま','み','む','め','も','や','ゆ','よ','ら','り','る','れ','ろ','わ','を','ん'}# All commonly used Hiragana
    single_hiragana_removed_list = [item for item in input_list if item not in single_hiragana]
    return single_hiragana_removed_list

def add_items_to_original_word_list(input_list): #Appends words to the original ('side 1') words list in the global scope
    if not input_list: #Error handling for the event that input_list is empty (this would occur in the event that there were not Japanese characters in the image or document)
        print('Error - No Japanese words in images')
        sys.exit(1)
    for item in input_list:
        original_words.append(item)
    return original_words
@measure
def get_reading_and_eng(input_list): #This uses Jamdict to return a list of strings, each string contains the hiragana and english definitions for each of the words in our original words list (above function)
    for item in input_list:   #CHANGE SO IT USES A GENERATOR
        result = jmd.lookup(item)
        kana_and_eng_def.append(str(result))
    return kana_and_eng_def



#2. ===Execute functions in process_file() which is imported into, and ran from, __main__.py===
def process_file():
    print('Running process_file()')
    tokenized_list = []
    combined_japanese_chars_list = []
    file_type = input_type[0] #This checks the file type entered on the GUI dropdown box (doc or img) and sends the files to the correct processing condition
    if file_type == '':
        print('Error - Please select a file type') #Error handling for the event that no file-type is selected 
        sys.exit(1)
    for item in input_files: 
        if file_type == 'Document':
            print('Entered doc processing loop')
            try:
                raw_text = docx2txt.process(item) #Get a string of all the text in the doc
                print(raw_text)
            except FileNotFoundError:
                print('Error - Document does not exist')
                sys.exit(1)
            japanese_only = get_japanese_only(raw_text) #Remove non-Japanese text from the string 
            print('Japanese only', japanese_only)
            tokenized_list = tokenize_into_words(japanese_only) #Tokenize string into a list of words 
            print('Tokenized list', tokenized_list)
            combined_japanese_chars_list = list_concat(tokenized_list) #join the lists created for each file passed in together
            print('Joined lists', combined_japanese_chars_list)
        elif file_type == 'Image':
            print('Entered image processing loop')
            try:
                raw_text = pytesseract.image_to_string( #Get a string of all the text in the image via OCR
                    Image.open(item), lang='jpn')
            except FileNotFoundError:
                print('Error - Image does not exist')
                sys.exit(1)
            japanese_only = get_japanese_only(raw_text) #Remove non-Japanese text from the string 
            print('Japanese only', japanese_only)
            tokenized_list = tokenize_into_words(japanese_only) #Tokenize string into a list of words 
            print('Tokenized list', tokenized_list) 
            combined_japanese_chars_list = list_concat(tokenized_list) #join the lists created for each file passed in together
            print('Joined lists', combined_japanese_chars_list)

    #Exit loop and back to process_file() scope
    irrelevant_items_removed_list = remove_irrelevant_characters(combined_japanese_chars_list) #Remove items that have no meaning (see function for more details)
    print('Irrelevant stuff removed', irrelevant_items_removed_list)
    single_katakana_removed_list = remove_single_katakana(irrelevant_items_removed_list) #Remove single katanaka characters (which are meaningless on their own)
    print('Single katanaka removed', single_katakana_removed_list)
    single_hiragana_removed_list = remove_single_hiragana(single_katakana_removed_list) #Removes single hiragana characters (which are meaningless on their own)
    print('Single hiragana removed', single_hiragana_removed_list)
    duplicate_items_removed_list = remove_duplicate_items(single_hiragana_removed_list) #Removes any duplicate words and characters in our word list
    print('Duplicate items removed', duplicate_items_removed_list)
    add_items_to_original_word_list(duplicate_items_removed_list) #Add original words to list in global scope 
    get_reading_and_eng(duplicate_items_removed_list) #Add reading and eng definition to list in global scope
    print('Readings and eng', kana_and_eng_def)
    














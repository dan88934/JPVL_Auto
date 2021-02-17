import unittest
from file_processing import get_japanese_only, tokenize_into_words, list_concat, remove_duplicate_items, remove_irrelevant_characters, remove_single_katakana, remove_single_hiragana, add_items_to_original_word_list, get_reading_and_eng


#The methods in the below class test the functions in file_processing.py
class TestFileProcessing(unittest.TestCase): 
    def test_get_japanese_only(self): #get_japanese_only function
        #Test that it removes eng and symbols from the string
        string = 'Hello今日、!!日本語を勉強した。^]'
        result = get_japanese_only(string)
        self.assertEqual(result, '今日日本語を勉強した')

    def test_tokenize_into_words(self):
        #Test that it takes each word from the sentence and creates a list of these words (in the mannar desired)
        string = '今日日本語を勉強した'
        result = tokenize_into_words(string)
        self.assertEqual(result, ['今日','日本','語','を','勉強','する', 'た']) #We can see that due to the settings, the past verb is changed to the root dict form

    # def test_list_concat(self):
    #     #This joins two list together - unsure of how to test it 
    #     master_list = [['今日','日本','語','を','勉強','する', 'た'], ['カタカナ','必死','避難']]
    #     result = list_concat(master_list)
    #     self.assertEqual(result, ['今日','日本','語','を','勉強','する', 'た','カタカナ','必死','避難'])
    
    def test_remove_duplicate_items(self):
        test_list = ['今日','日本','語','語','勉強','を','勉強','する', 'た']
        result = remove_duplicate_items(test_list)
        self.assertEqual(result, ['今日','日本','語','勉強','を','する', 'た']) #Removes all but the first instance of the word

    def test_remove_irrelevant_characters(self):
        test_list = ['今日','日本','語','ます','勉強','を','する','って']
        result = remove_irrelevant_characters(test_list)
        self.assertEqual(result, ['今日','日本','語','勉強','を','する'])
    
    def test_remove_single_katakana(self):
        test_list = ['今日','日本','語','勉強','く','を','する', 'コ']
        result = remove_single_katakana(test_list)
        self.assertEqual(result, ['今日','日本','語','勉強','を','する'])

    def test_remove_single_hiragana(self):
        test_list = ['今日','日本','語','は','勉強','を','する', 'め']
        result = remove_single_hiragana(test_list)
        self.assertEqual(result, ['今日','日本','語','勉強','する'])

    def test_add_items_to_original_word_list(self):
        test_list = ['今日','日本','語','勉強','する']
        result = add_items_to_original_word_list(test_list)
        self.assertEqual(result, ['今日','日本','語','勉強','する'])

    # def test_get_reading_and_eng(self):
           #This checks that the output contains an english definition matching to one of the JP words in list - unsure of how to carry this out
    #     test_list = ['今日','日本','語','勉強','する']
    #     # test_string = 'Today'
    #     result = get_reading_and_eng(test_list)
    #     self.assertIn('language', result) #'語' means 'language' (usually when added on to the name of a country i.e. イタリア語)

        



if __name__ == '__main__':
    unittest.main()
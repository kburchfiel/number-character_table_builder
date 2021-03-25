# Number-Character Table Builder
#
# Kenneth Burchfiel, MIT License
#
# First uploaded to GitHub on 2021-3-25
#
# Python's chr() function converts a number into its corresponding Unicode
# value. This program creates a table of i, chr(i) pairs for all instances of
# chr(i) that could be successfully encoded. 
#
# It's fun to look through the output (which I needed to open in Libre Calc, as
# most characters did not render correctly in Excel using its default settings)
# and see all the different types of characters that exist in Unicode, from the
# Latin alphabet to Chinese characters and beyond. For example, the table shows
# that chr(127952) returns a volleyball, one of many emoji now present in
# Unicode. (It appears that most of the emoji begin at position 127,744 in the
# list, or 1f300 in hexadecimal form, and stop before position 131,072, or 20000
# in hexadecimal form.) I hope you'll enjoy looking through the table as well! 
#

import pandas as pd

def create_number_character_table(start_num=0, end_num=1024):
    '''For each number looped through, the function determines the Unicode
    character that corresponds to that number (unless that character cannot be
    printed--see comments below); appends both the number and its corresponding
    character to a tuple; and stores that tuple in a list. The function then
    returns a list of these tuples.'''
    number_character_table = []
    for i in range (start_num, end_num+1, 1): 
        # end_num+1 ensures that the function includes the final number
        # specified in the range print(i) # useful for debugging
        encode_result = chr(i).encode(encoding="utf-8",errors="ignore") 
        # For Python documentation on chr(), see
        # https://docs.python.org/3/library/functions.html#chr
        #
        # I initially encountered errors when trying to print certain outputs of
        # chr(i) and/or export them to a CSV file. The error messages were in
        # the following format: 
        #
        # "'utf-8' codec can't encode character '\ud800' in position 0:
        # surrogates not allowed." 
        #
        # (\ud800 was just one example of a character that could not be encoded.
        # It corresponded to an i of 55296.) 
        #
        # The above line of code and the following two lines are designed to
        # prevent values from being stored in number_character_table that would
        # cause errors later on.
        #
        # The above line creates an encoded version of chr(i) (see
        # https://docs.python.org/3/library/stdtypes.html#str.encode). It
        # ignores errors that occur in the encoding process so as not to
        # terminate the program. 
        #
        # After some testing, I found that, for instances of chr(i) that
        # resulted in encoding errors, the output of encode_result (i.e. the
        # output of chr(i).encode(encoding="utf-8",errors=ignore") had a length
        # of 0 as determined by the len() function. Meanwhile, the length of
        # encode_result was 1 or greater for instances of chr(i) that could be
        # printed or saved into a csv successfully.
        #
        # This provided a solution to the encoding issues: I could check the
        # length of encode_result and then skip to the next instance of i if the
        # length was 0. If the length was not 0, I could then append chr(i) to
        # number_character_table knowing that it would not cause any errors
        # later on. 
        if len(encode_result) == 0:
            continue
        number_character_table.append((i, hex(i), chr(i))) 
        # Storing i, a hexadecimal representation of i, and chr(i) (not
        # encode_result, whose purpose is simply to prevent instances of chr(i)
        # that would cause errors from being appended into this table)
    return(number_character_table)

number_character_table = create_number_character_table(0, 1112064) 
# There are 1,112,064 possible Unicode values, hence the choice of parameters
# print(number_character_table) # for debugging
df_nc = pd.DataFrame(number_character_table,columns=["dec", "hex", "char"])
df_nc.set_index('dec',inplace=True)
print(df_nc)
df_nc.to_csv('number_character_table.csv',encoding='utf-8')
# Note: opening this .csv file in Excel will cause many characters to display
# incorrectly, as Excel does not default to UTF-8 encoding. Therefore, I
# recommend opening it in Libre Calc, an open-source spreadsheet program.
# However, there's probably a way to force Excel to open the file in UTF-8 if
# you prefer not to use/install Libre Calc. (Notepad displayed more characters
# than a default Excel setup, but some characters were still missing that were
# visible in Libre Calc, such as #129-159.) recommend using Notepad (or Libre
# Calc or Google Sheets, as someone suggested on the internet) to view this
# document.
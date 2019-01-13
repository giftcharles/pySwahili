##############################################################
################### FEATURE LOG ##############################
##############################################################
    #
    # Author: Gift Charles Nakembetwa
    #
    # Email: Giftnakembetwa@gmail.com
    #
    # Link: Pending...
    #
    # Version: 0.1
    #
    # Title: Neno Processor
    # 
    # Description: The Classes in this script can be used to
    #              process the swahili language depending on
    #              the needs of the user.(Check the feature
    #              list below).
    #
    # License: Pending...
    #
    # Date: Sunday, 13 January 2019
    #
    #
    # BACKLOG:
    #    >> English to swahili and viceversa translation
    #    >> Plural to singular and viceversa conversition
    #    >> String number operations
    #    >> Word usage frequency statistics into database
    #    >> Name initials sensitivity
    #    >> Ignorable symbols acknowledge
    #    
    # FEATURES:
    #    >> Break words into "sarufi"
    #    >> Convert digits into text representations
    #
    #
    #
##############################################################
####################### END ##################################
################### FEATURE LOG ##############################
##############################################################

import re
import codecs



class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
        expression -- points out the value with the problem
    """

    def __init__(self, message, expression):
        self.message = message
        self.expression = expression
        
##############################################################
####################### END ##################################
################## ERROR HANDLERS ############################
##############################################################
        
class Neno():
    
    """
        # Neno() class.
        #
        # This class can help process the swahili language depending on the needs.
        
    """
    
    def break_word(self, str=""):
        """
            break apart a string into blocks of
            consonants, stop and comma and such
            symbols
           
        """
        
        conso = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "m", "n",
              "p", "r", "s", "t", "v", "w", "y", "z"]

        vowels = ["a", "e", "i", "o", "u"]

        # variables
        n_str = ""
        conc_list = list()

        # kill the function if the string
        # provided is empty.
        if str == "" or str == " ":return None

        # for every character in the string
        # check if is consonant, vowel or symbol.
        for c in str:

            # if is consonant
            if c in conso and c != "" or c == "'":
                n_str+=c
                str = str[1:]

            # if is vowel
            if c in vowels and c != "":
                
                # if is after or before a consonant
                # the add it after or before that consonant 
                # {revisit this in the future}            
                n_str+=c
                str = str[1:]
                conc_list.append(n_str)
                n_str = ""

            # if it is a .,;:?! or any other stopper
            # symbol
            sym_regex = re.match("[.,;:?!]", c)
            if sym_regex != None and n_str == "":
                conc_list.append(c)
                str = str[1:]

        return conc_list

    def break_sentence(self, str=""):
        """
            break up a sentence into blocks of words and symbols
            in them and them feed them to the 
        """
        
        phonemes = list()
           
        # if their are brackets of any kind right after a word
        # remove the brackets and add spaces between the words.
        bracketsWregex = "(\w+?)([()[\]{}])(\w+)([]()[{}])"
        brackets = re.match(bracketsWregex , str.lower())
        if brackets != None:
            if brackets.group(1) != None:
                str = re.sub(bracketsWregex, brackets.group(1) + " " + brackets.group(3), str)
            else:
                str = re.sub(bracketsWregex, " " + brackets.group(3), str)
                
        # if their is a bracketed string of words with no words immidiately
        # before or after the word then replace the brackets with spaces
        bracketsWregex = "([()'\"[\]{}])(\w+)([]()'\"[{}])"
        brackets = re.match(bracketsWregex , str.lower())
        if brackets != None:
            str = re.sub(bracketsWregex, brackets.group(2), str)


        # get the words into blocks
        # pass the words into the function to split them into
        # blocks of phonemes & store them in 
        for word in str.split():
            w_regex = re.match("^[a-z]+", word)
            d_regex = re.match("^\d+", word)
            dot_dot_nums = re.match("^\d+\.\d+\.\d+", word.lower())
            
            if re.match('[aeiou0-9,.!?:;"\']', word.lower()[-1:]) == None:
                raise InputError("Kiswahili lazima kiishie na aidha a, e, i, o, u au iwe namba 0-9 au alama ,.!?:\"';", word.lower())
                
            
            # if their is no space between word symbol word combinations then raise Error
            if re.match("\w+([.,;:?!]+)\w+", word.lower()) != None:
                raise InputError("Lazima kuwe na nafasi kabla ya neno na baada ya alama.", word.lower())
            
            # if the string has digits and letters in it then kill the function
            if re.match("^\d+[a-z]+", word.lower()) != None or re.match("^[a-z]+\d+", word.lower()):
                raise InputError("Maneno na namba haziwezi unganishwa kutengeneza neno kwenye kiswahili", word.lower())
            
            # if its digits followed by a full stop, then one or more full digits
            # then another full stop, this should be read as consecative decimal points
            # deal with them separately, fill the phonemes list and return out of function
            #
            # muhumu kwa kusoma version za software
            if dot_dot_nums != None:
                #print("sowy")
                # if it ends with a symbols then delete it first
                # from the string and continue with the operation
                last_char = word[-1:]
                if re.match("^[.,;:?!]", last_char) != None:
                    word = word[:-1]
                
                counter = 0
                for number in word.split("."):
                    if counter >= 1 and number != "":
                        for d in number:
                            phonemes.append(self.digits_into_words(d))
                            if counter+1 < len(word.split(".")):phonemes.append("nukta")
                        counter+=1
                    if counter == 0 and number != "":
                        for w in self.digits_into_words(number).split():
                            phonemes.append(w)
                        phonemes.append("nukta")
                        counter+=1
                        
                if re.match("^[.,;:?!]", last_char) != None:phonemes.append(last_char)
                
            # if is word then break into phonemes
            if w_regex != None: 
                for w in self.break_word(word.lower()):
                    phonemes.append(w)
                    
            # if is digits then turn them into words
            # but should not match the dot num dot expression
            # those are handled by another part of the function
            if d_regex != None and dot_dot_nums == None:
                
                # if their is a comma at the end of the digits
                comma_regex = re.match("[.,;:?!]", word[-1])
                
                if comma_regex != None:
                    stop_mark = word[-1]
                    d_words = self.digits_into_words(word[:-1])
                    for d_word in d_words.split():            
                        phonemes.append(d_word)
                    phonemes.append(stop_mark)
                else:
                    d_words = self.digits_into_words(word)
                    for d_word in d_words.split():
                        phonemes.append(d_word)
                    
        return phonemes

    def digits_into_words(self, str=""):
        """
            Take a string, check if its made of digits
            After that turn that string into word representation of digits
            break the words into consonant chunks and return them.
            
            This can be helpful when dealing with huge amounts of text from a book
            a text file or anything of the sort.
        """
        #print(str)
        # variables
        
        flipped = False
        digit_string = list()
        numbers = {
            "1":"moja",
            "2":"mbili",
            "3":"tatu",
            "4":"nne",
            "5":"tano",
            "6":"sita",
            "7":"saba",
            "8":"nane",
            "9":"tisa",
            }
        
        def makumi(str):
            """
                convert the string digit into a text of the tens position in swahili
            """
            if str == "1":
                return "Kumi"
            if str == "2":
                return "Ishirini"
            if str == "3":
                return "Therasini"
            if str == "4":
                return "Arobaini"
            if str == "5":
                return "Hamsini"
            if str == "6":
                return "Sitini"
            if str == "7":
                return "Sabini"
            if str == "8":
                return "Themanini"
            if str == "9":
                return "Tisini"
            
            return "failed!"
        

        d_regex = re.match("^\d+", str)
        if d_regex != None:
            
            # remove the commas
            str = str.replace(",", "")
            
            # break the string at the period
            str_list = str.split(".")
            
            if len(str_list[0])>1:
                # reverse the digits before the period
                str_list[0] = str_list[0][::-1]
                
                flipped = True
            
            # for each character in string
            # replace with its positional name
            position = 0
            for d in str_list[0]:
                # any zeros
                #if d == "0" and position != 0:
                    #digit_string.append("na")
                if d == "0" and len(str_list[0])==1:
                    digit_string.append("sifuri")
                    
                for k,v in numbers.items():
                    if d == k:
                        # based on position what is added at the beggining changes
                        
                        # variables
                        na = mil = bil = tril = kwan = ""
                        
                        # mamoja
                        if position == 0:
                            digit_string.append(v)
                        
                        # makumi
                        if position == 1:
                            if str_list[0][position - 1] != "0":na=" na"
                            digit_string.append(makumi(k) + na)
                        
                        # mamia
                        if position == 2:
                            digit_string.append("Mia " + v)
                            
                        # maelfu
                        if position == 3 and len(str_list[0])==4:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Elfu " + v + na)
                        elif position == 3 and len(str_list[0])>4:
                            digit_string.append(v)
                        if position == 4:
                            if str_list[0][position - 1] != "0":na=" na"
                            digit_string.append("Elfu " + makumi(k) + na)
                            
                        # malaki
                        if position == 5:
                            digit_string.append("Laki " + v)
                            
                        # mamilioni
                        if position == 6 and len(str_list[0])==7:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Milioni " + v + na)
                        elif position == 6 and len(str_list[0])>7:
                            digit_string.append(v)
                        if position == 7:
                            if str_list[0][position - 1] != "0":na=" na"
                            if len(str_list[0])==8:mil="Milioni "
                            digit_string.append(mil + makumi(k) + na)
                        if position == 8:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Milioni mia " + v + na)
                            
                        # mabilioni
                        if position == 9 and len(str_list[0])==10:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Bilioni " + v + na)
                        elif position == 9 and len(str_list[0])>10:
                            digit_string.append(v)
                        if position == 10:
                            if len(str_list[0])==11:bil="Bilioni "
                            if str_list[0][position - 1] != "0":na=" na"
                            digit_string.append(bil + makumi(k) + na)
                        if position == 11:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Bilioni mia " + v + na)
                            
                        # trilioni
                        if position == 12 and len(str_list[0])==13:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Trilioni " + v + na)
                        elif position == 12 and len(str_list[0])>13:
                            digit_string.append(v)
                        if position == 13:
                            if len(str_list[0])==14:tril="Trilioni "
                            if str_list[0][position - 1] != "0":na=" na"
                            digit_string.append(tril + makumi(k) + na)
                        if position == 14:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Trilioni mia " + v + na)
                            
                        # kwantilioni
                        if position == 15 and len(str_list[0])==16:
                            digit_string.append("Kwantilioni " + v)
                        elif position == 15 and len(str_list[0])>16:
                            digit_string.append(v)
                        if position == 16:
                            if len(str_list[0])==17:kwan="Kwantilioni "
                            if str_list[0][position - 1] != "0":na=" na"
                            digit_string.append(kwan + makumi(k) + na)
                        if position == 17:
                            if str_list[0][position - 1] == "0":na=" na"
                            digit_string.append("Kwantilioni mia " + v + na)
                position+=1
            
            if flipped == True:
                digit_string = digit_string[::-1]
            
            # turn the decimals in to text and add them to [digit_string]
            if len(str_list) == 2:
                digit_string.append("nukta")
                for d in str_list[1]:
                    if d == "0":
                        digit_string.append("sifuri")
                    for k,v in numbers.items():
                        if d == k:
                            digit_string.append(v)
            
            sentence = ' '.join(digit_string) 
            return sentence

with codecs.open("test2.txt", "r", "utf-8") as f:
    s = f.read()

#s = "manono 892345654343"
print(len(s))
p = Neno()

concats = p.break_sentence(s)



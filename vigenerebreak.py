import urllib2, random, string, numpy, itertools, time

# Global variable to set the algorithm's tolerance to deviate from 0.065 freq
TOLERANCE = 0.019

# ##load dict of all words
# filename = "dictionary.txt"
# reader = file(filename,"r")
# all_eng_words = reader.read().split()

## load dict of top 1000 words
filename = "1000_most_common_words.txt"
reader = file(filename,"r")
top_words = reader.read().split()

## load dict of top 1000 quadgrams
filename = "eng_top1000_quadgrams.txt"
reader = file(filename,"r")
top_quads = reader.read().split()

# INPUT : block of text /w no spaces
# OUTPUT : fitness score
# If score is under 100(?), not english. If over 100(?) its english.
def isEnglishFast(text):
    score = 0

    for word in top_words:
        t_count = text.count(word)
        if t_count > 0 and len(word) > 3: #if an english word is found in the text AND its longer than 4 char
            weight = t_count * len(word) * 1000
            score = score + weight
    
    for quad in top_quads:
        count = text.count(quad)
        if count > 0:
            weight = count * 1000
            score = score + weight
        
    # barbaric attempt to normalize score based on length
    score = score / len(text)
    
    return score

# # INPUT : block of text /w no spaces
# # OUTPUT : fitness score
# # If score is under 500(?), not english. If over 500(?) its english.
# def isEnglish(text):
#     score = 0
#     #words_found = 0
    
#     for word in all_eng_words: 
#         t_count = text.count(word)
#         if t_count > 0 and len(word) > 3: #if an english word is found in the text AND its longer than 2 char
#             #words_found = words_found + t_count
#             weight = t_count * len(word) * 1000
#             score = score + weight
#     # barbaric attempt to normalize score based on length
#     score = score / len(text)
    
#     return score

# shift a single character c by n
def shiftBy(c, n):
    return chr(((ord(c) - ord('a') + n) % 26) + ord('a'))

# take input text and ouput the frequency of each letter in an array indexed by letter
def findCharFreqs(text):
    frequency = {}
    for ascii in range(ord('a'), ord('a')+26):
        frequency[chr(ascii)] = float(text.count(chr(ascii)))/len(text)
    return frequency

# takes an array of letter frequencies indexed by letter and returns the sum of the frquencies squared
def sumFreqsSquared(frequency):
    sum_freqs_squared = 0.0
    for ltr in frequency:
        sum_freqs_squared += frequency[ltr]*frequency[ltr]
    return sum_freqs_squared
    
# takes a block of text encrypted with the Caesar Cipher as well as an array of it's letter frequencies.
# outputs array of possible caesar shift keys
def caesarBreak(encrypted_text, et_frequency):
    normal_freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
    possible_keys = []
    for possible_key in range(0, 25):
        sum_f_sqr = 0.0
        for ltr in normal_freqs:
            caesar_guess = shiftBy(ltr, possible_key)
            sum_f_sqr += normal_freqs[ltr]*et_frequency[caesar_guess]
        if abs(sum_f_sqr - .065) < TOLERANCE:
            #print ">> Close Caesar Key: ", possible_key, " f_sqr is ",sum_f_sqr
            possible_keys.append(possible_key)
    return possible_keys

# Input text encrypted with Vigenere cipher
# Output an array of possible key lengths with the sum of the Freqs squared for each
def findKeyLength(encrypted_text):
    ans = []
    for x in range(10,20): # CHANGE BACK TO 10,20 FOR BHC
        sum_f_sqr = sumFreqsSquared(findCharFreqs(encrypted_text[0::x]))
        if abs(sum_f_sqr - .065) < .05: # just check all keys
            print "Vigenere Key length could be: ", x, " f_sqr is ",sum_f_sqr
            ans.append(x)
    return ans

# master function to break vigenere cipher with UNKNOWN key length
def unkVigenereBreak(encrypted_text):
    ans = []
    key = []
    key_length_arr = findKeyLength(encrypted_text)
    for y in range(0, len(key_length_arr)):
        key_length = key_length_arr[y]
        print "-------"
        print "Vigenere Breaking for Possible Key Length: ",key_length
        possible_vin_keys = []
        for x in range(0, key_length):
            print "> Caeser Breaking index: " + str(x)
            possible_caeser_shifts = caesarBreak(encrypted_text, findCharFreqs(encrypted_text[x::key_length]))
            if possible_caeser_shifts == []:
                print "> Caeser Break FAILED for index: ",  x, " | defaulting to all"
                possible_vin_keys.append(range(0,26))
            else:
                print "> Caeser Break Succeeded for index: ", x, "| Possible Keys are: ", possible_caeser_shifts
                possible_vin_keys.append(possible_caeser_shifts)
                
        if possible_vin_keys != []:
            print "Possible Vigenere Keys for Key Length: ", key_length, possible_vin_keys
            all_keys = allPossibleKeyCombinations(possible_vin_keys)
            
            # Check keys against the cipher to see if it solves it
            print "Decoding with all possible Vigenere Keys and checking if result is English..."
            timer = time.clock()
            
            for k in all_keys:
                decrypted = vinDecoderNumKey(encrypted_text, k).lower()
                f_score = isEnglishFast(decrypted)
                
                #print "Key: ",k, "Decrypts to fitness score of", f_score
                #print decrypted,"\n"
                
                if (f_score > 300): # CHANGE BACK TO 100 for BHC
                    print "\nSOLVED?? This is close to English: "
                    print k, f_score, decrypted
                    ans.append([k,decrypted])
                elif ((time.clock() - timer) > 10):
                    timer = time.clock()
                    #print(".")
                   
    print "~~~~ POSSIBLE ANSWERS ~~~~\n", ans
    return ans

# shifts letter 1 by an amount equal to letter 2
def letter_from_difference(letter1, letter2):
    diff = (ord(letter1) - ord(letter2))
    if diff < 0:
        diff = 26 + diff
    elif diff + 65 > 90:
        diff -= 65
    return chr(65 + diff)

# INPUT: vigenere encrypted ciphertext text and numeric key
# Output: decrypted ciphertext
def vinDecoderNumKey(ciphertext, key):
    res = []
    key_index = 0
    key = key2letters(key)
    for letter in ciphertext:
        res.append(letter_from_difference(letter, key[key_index]))
        key_index += 1
        if key_index > len(key) - 1:
            key_index = 0
    res = list_to_string(res)
    return res
    

# takes an array key of numbers 0-25 and translates it to the cooresponding alphabet character
def key2letters(key):
    ans = []
    alph = list(string.ascii_lowercase)
    for x in range(0,len(key)):
        ans.append(alph[key[x]])
    return ans


def list_to_string(l):
    res = ""
    for elem in l:
        res += elem
    return res
    
# Input: string filename of the file to load
# Output: unformatted text
def loadText(filename):
    file = open(filename,'r')
    text = file.read()
    onlyletters = filter(lambda x: x.isalpha(), text)
    onlylower = onlyletters.lower()
    return onlylower

# Input a 2 dimensional array and output an array of every possible comination
def allPossibleKeyCombinations(arr):
    print "Finding All Possible Key Combinations..."
    ans = []
    timer = time.clock()
    for t in itertools.product(*arr):
        ans.append(t)
        if (time.clock() - timer) > 10:
            print "."
            timer = time.clock()
    print "Number of Possible Keys are:", len(ans)
    return ans

# # Loop through blackhat challenges 2 and 4 and run the Vigenere Analysis on them
# print "--------"
# encrypted = loadText('secret2')
# print "ANALYZING secret2"
# #print "Encrypted Message: ",encrypted
# unkVigenereBreak(encrypted)

# print "--------"
# encrypted = loadText('secret4')
# print "ANALYZING secret4"
# #print "Encrypted Message: ",encrypted
# unkVigenereBreak(encrypted)


# ## Testing Vin Breaker with known Vin
# print "--------"
# encrypted = loadText('test_vig2.txt')
# print "ANALYZING test vig2"
# print "Encrypted Message: ",encrypted
# unkVigenereBreak(encrypted)

# ## Testing Vin Decoder
# encrypted = loadText('test_vig.txt').lower()
# decrypted = vinDecoderAlphaKey(encrypted, 'encrypt').lower()
# print decrypted
# print isEnglish(decrypted)
# print isEnglish(encrypted)

## Testing Vin Decoder
encrypted = loadText('secret2').lower()
decrypted = vinDecoderNumKey(encrypted, [17, 9, 8, 17, 15, 6, 3, 7, 2, 24, 23, 17, 15]).lower()
print decrypted
print isEnglishFast(decrypted)
print isEnglishFast(encrypted)

## Testing isEnglishFast()
# import random, string
# count = 0
# while count < 10:
#     arr = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(1000))
#     #print arr
#     print "Score of random", isEnglishFast(arr)
#     count=count+1

# text = loadText('some_eng')
# print "Score of Eng: ",isEnglishFast(text)

# ## Testing allPossibleCombinations()
# arr = [[16, 20], [14], [12, 24, 25], [7, 12], [15], [4, 8, 15, 19, 23], [2, 3, 12], [3, 7, 22], [6, 7, 21], [3]]
# allPossibleKeyCombinations(arr)
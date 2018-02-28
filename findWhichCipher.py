import urllib2, random, string, numpy

normal_freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}

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

# Input: string filename of the file to load
# Output: unformatted text
def loadText(filename):
    file = open(filename,'r')
    text = file.read()
    onlyletters = filter(lambda x: x.isalpha(), text)
    onlylower = onlyletters.lower()
    return onlylower

def diffFromNormFreq(text):
    given_freq_arr = findCharFreqs(text)
    total_diff = 0
    for char in given_freq_arr:
        total_diff = total_diff + abs(given_freq_arr[char] - normal_freqs[char])
    return total_diff
    
# Input text encrypted with Vigenere cipher
# Output an array of possible key lengths with the sum of the Freqs squared for each
def findKeyLength(encrypted_text):
    ans = []
    for x in range(10,20):
        sum_f_sqr = sumFreqsSquared(findCharFreqs(encrypted_text[0::x]))
        if abs(sum_f_sqr - .065) < .5:
            print "Vigenere Key length could be: ", x, " f_sqr is ",sum_f_sqr
            ans.append(x)
    return ans


# Loop through all blackhat challenges and run the cipher analysis on them
count=1
while (count < 6):
    filename = "secret" + str(count)
    print"-----"
    print "Analyzing: ", filename
    text = loadText(filename)
    print "Diff from Norm Freq: ", diffFromNormFreq(text)
    print "Sum Freq Squared: ", sumFreqsSquared(findCharFreqs(text))
    print "Number of J's: ", text.count('j')
    findKeyLength(text)
    count=count+1

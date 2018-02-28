import urllib2

# INPUT : block of text /w no spaces
# OUTPUT : fitness score
# If score is under 500(?), not english. If over 500(?) its english.
def isEnglish(text):
    #load dict of all words
    filename = "dictionary.txt"
    reader = file(filename,"r")
    all_eng_words = reader.read().split()

    score = 0
    #words_found = 0
    
    for word in all_eng_words:
        
        t_count = text.count(word)
        if t_count > 0 and len(word) > 3: #if an english word is found in the text AND its longer than 2 char
            
            #words_found = words_found + t_count
            weight = t_count * len(word) * 1000
            score = score + weight
            
    # barbaric attempt to normalize score based on length
    score = score / len(text)
    
    return score
    
def isEnglishFaster(text):
    #load dict of all words
    filename = "1000_most_common_words.txt"
    reader = file(filename,"r")
    all_eng_words = reader.read().split()

    score = 0
    #words_found = 0
    
    for word in all_eng_words:
        
        t_count = text.count(word)
        if t_count > 0 and len(word) > 3: #if an english word is found in the text AND its longer than 2 char
            
            #words_found = words_found + t_count
            weight = t_count * len(word) * 1000
            score = score + weight
            
    # barbaric attempt to normalize score based on length
    score = score / len(text)
    
    return score
    
# # TESTING
    
res=file('secret4','r')
mobytext = res.read()
print "Score of english: ", isEnglish(mobytext)


import random, string
count = 0
while count < 10:
    arr = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10000))
    #print arr
    print "Score of random", isEnglish(arr)
    count=count+1

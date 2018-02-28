from caesarcipher import CaesarCipher

filename = 'secret5'

f=file(filename, 'r')
secret = [word.strip() for word in f]
print "Processing ", filename, ": ", secret[0], "\n"
f.close()

def caesar_letter_shift(string,o):
    cipher = CaesarCipher(string, offset=o)
    return cipher.decoded



count = 0
while count < 27:
    print "Offset: ", count, "\n", caesar_letter_shift("sahyk iapkp daben opzwu kbpda naopk bukqn hebau",count), "\n"
    count=count+1

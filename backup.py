import sys
import codecs


# including vowel/cons characters
CONSONANTS = {u'\u0623':'?a', u'\u0625':'?I', u'\u0628':'b', u'\u062A':'t', u'\u062B':'T', u'\u062C':'dZ', u'\u062D':'X\\', u'\u062E':'x',
            u'\u062F':'d', u'\u0630':'D', u'\u0631':'4', u'\u0632':'z', u'\u0633':'s', u'\u0634':'S', u'\u0635':'s_?\\', u'\u0636':'d_?\\',
            u'\u0637':'t_?\\', u'\u0638':'T_?\\', u'\u0639':'?\\', u'\u063A':'G', u'\u0641':'f', u'\u0642':'q', u'\u0643':'k', u'\u0644':'l',
            u'\u0645':'m', u'\u0646':'n', u'\u0647':'h', u'\u0648':'w', u'\u064a':'y', u'\u0629':'a', u'\u0649':'a', u'\u064b':'?'}


SHORT_VOWELS = {u'\u064e':'a', u'\u064f':'u', u'\u0650':'I', u'\u0651':':'}

AL = [u'\u0627', u'\u0644']

SUN_LETTERS = [u'\u062A', u'\u062B', u'\u062F', u'\u0630', u'\u0631',u'\u0632', u'\u0633', u'\u0634', u'\u0635', u'\u0636', u'\u0637', \
               u'\u0638', u'\u0644', u'\u0646']


LONG_VOWELS = {u'\u0627':'A:', u'\u064a':'i:', u'\u0648':'u'}

LONG_TO_SHORT = {'A:':'?a', 'u:':'w', 'i:':'y'}




def main():
    source_file = codecs.open(sys.argv[1], 'r', encoding='utf-8')
    out_file = codecs.open('transcriptions.txt', 'w', encoding='utf-8')
    for line in source_file:
        line = line.strip()
        line = line.replace(u'\ufeff', '')
        characters = list(line)
        print str(characters)
        print line
        transcrip = [''] * len(characters)

        if characters[0] == AL[0] and characters[1] == AL[1] and len(characters) > 2:
            contains_al = True
        else:
            contains_al = False

        characters, transcrip = initial_replacement(characters, transcrip)
        if contains_al:
            characters, transcrip = process_al(characters, transcrip)
        characters, transcrip = process_vowels(characters, transcrip, contains_al)

        print transcrip



def initial_replacement(characters, transcrip):

    for i in range (0, len(characters)):
        if characters[i] in CONSONANTS:
            transcrip[i] = CONSONANTS[characters[i]]
        if characters[i] in SHORT_VOWELS:
            transcrip[i] = SHORT_VOWELS[characters[i]]
        if characters[i] in LONG_VOWELS:
            transcrip[i] = LONG_VOWELS[characters[i]]

    return characters, transcrip

def process_vowels(characters, transcrip, contains_al):

    if contains_al:
        start = 2
    else:
        start = 0

    if characters[start] in LONG_VOWELS:
        transcrip[start] = LONG_TO_SHORT[transcrip[0]]

    for i in range (start + 1, len(characters) - 1):
        if characters[i] in LONG_VOWELS:
            if characters[i + 1] in LONG_VOWELS:
                transcrip[i] = LONG_TO_SHORT[transcrip[i]]


    return characters, transcrip

def process_al(characters, transcrip):

    if len(characters) > 2:
        if characters[0] == AL[0] and characters[1] == AL[1]:
            transcrip[0] = '?a'
            if characters[2] in SUN_LETTERS:
                transcrip[1] = transcrip[2]
                transcrip[2] = ":"

    return characters, transcrip


if __name__ == "__main__":
    main()








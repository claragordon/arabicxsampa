import sys
import codecs


# dictionaries and sound groupings

# maps Arabic consonants to the corresponding X-SAMPA transcription
CONSONANTS = {u'\u0628':'b', u'\u062A':'t', u'\u062B':'T', u'\u062C':'dZ', u'\u062D':'X\\', u'\u062E':'x',
            u'\u062F':'d', u'\u0630':'D', u'\u0631':'4', u'\u0632':'z', u'\u0633':'s', u'\u0634':'S',
            u'\u0635':'s_?\\', u'\u0636':'d_?\\', u'\u0637':'t_?\\', u'\u0638':'T_?\\', u'\u0639':'?\\',
            u'\u063A':'G', u'\u0641':'f', u'\u0642':'q', u'\u0643':'k', u'\u0644':'l', u'\u0645':'m',
            u'\u0646':'n', u'\u0647':'h', u'\u064a':'y', u'\u0648':'w', u'\u0629':'a'}

# isolate vowel diacritical marks: fatha, domma, kasra
SHORT_VOWELS = {u'\u064e':'a', u'\u064f':'u', u'\u0650':'I'}

# long vowel characters
LONG_VOWELS = {u'\u0627':'A:', u'\u064a':'i:', u'\u0648':'u:', u'\u0649':'A:'}

# combinted characters consisting of a character and hamza
COMBINED_HAMZA = {u'\u0623':'?a', u'\u0624':'?u', u'\u0625':'?I'}

# separate non-vowel diacritical marks: shadda and sukun
DIACRITICS ={u'\u0651':':', u'\u0652':''}

# tanween diacritical marks
TANWEEN = {u'\u064b':'an', u'\u064c':'un', u'\u064d':'in'}

# characters in 'al' particle
AL = [u'\u0627', u'\u0644']



# sound groupings used for X-SAMPA transcription adjustment

# for adjusting 'al' pronunciation
SUN_LETTERS = ['t', 'T', 'dZ', 'D', '4', 'z', 's', 'S', 's_?\\', 'd_?\\', 't_?\\', 'T_?\\', 'l', 'n']

# maps long vowels to their associated consonant pronunciation
LONG_TO_SHORT = {'A:':'?a', 'u:':'w', 'i:':'y'}


def main():
    """
    Reads in words from file, performs the appropriate transcription and adjustments,
    and prints the result to the output file.
    """

    # open word and output files
    source_file = codecs.open(sys.argv[1], 'r', encoding='utf-8')
    out_file = codecs.open(sys.argv[2], 'w', encoding='utf-8')

    for line in source_file:

        # remove extraneous characters
        line = line.strip()
        line = line.replace(u'\ufeff', '')

        characters = list(line)
        transcrip = [''] * len(characters)

        # test whether word has 'al' particle
        if characters[0:2] == AL:
            contains_al = True
        else:
            contains_al = False

        # get initial transcription through letter replacement
        transcrip = initial_replacement(characters, transcrip)

        # adjust transcription of alif maqsura and tanween characters
        transcrip = process_endings(characters, transcrip)

        # apply various transformations to X-SAMPA list to get final transcription
        if contains_al:
            transcrip = process_al(transcrip)
        transcrip = process_vowels(transcrip, contains_al)
        transcrip = add_short_vowels(transcrip, contains_al)

        # write word and transcription to file
        out_file.write(line + '\t')
        for symbol in transcrip:
            out_file.write(symbol)
        out_file.write('\n')



def initial_replacement(characters, transcrip):
    """
    Performs a "first pass" transcription using simple character-to-X-SAMPA dictionaries.
    All vowel characters are represented as their long vowel form.
    """

    for i in range (0, len(characters)):
        if characters[i] in CONSONANTS:
            transcrip[i] = CONSONANTS[characters[i]]
        elif characters[i] in COMBINED_HAMZA:
            transcrip[i] = COMBINED_HAMZA[characters[i]]
        elif characters[i] in DIACRITICS:
            transcrip[i] = DIACRITICS[characters[i]]
        elif characters[i] in TANWEEN:
            transcrip[i] = TANWEEN[characters[i]]
        elif characters[i] in SHORT_VOWELS:
            transcrip[i] = SHORT_VOWELS[characters[i]]
        if characters[i] in LONG_VOWELS:
            transcrip[i] = LONG_VOWELS[characters[i]]

    return transcrip


def process_endings(characters, transcrip):
    """
    Adjusts pronunciation of alif maqsura and tanween vowels.
    """

    last_idx = len(characters) - 1

    # adjust representation of alif maksura if it follows hamza
    if characters[last_idx] == u'\u0649' and characters[last_idx - 1] in COMBINED_HAMZA.keys():
        transcrip[last_idx-1] = '?'

    # shorten the long vowel that carries the tanween character
    if characters[last_idx] in TANWEEN:
        if characters[last_idx - 1] in LONG_VOWELS:
            transcrip[last_idx - 1] = ''

    return transcrip


def process_vowels(transcrip, contains_al):
    """
    Changes long vowels to their consonant equivalents if found in word-initial position,
    or followed by another long vowel.
    """

    if contains_al:
        start = 2
    else:
        start = 0

    # change word-initial long vowels to consonant pronunciation
    if transcrip[start] in LONG_TO_SHORT:
        transcrip[start] = LONG_TO_SHORT[transcrip[start]]

    # change long vowels followed by another long vowel to consonant pronunciation
    for i in range (start + 1, len(transcrip) - 1):
        current = transcrip[i]
        next = transcrip[i + 1]
        if current in LONG_TO_SHORT:
            if next in LONG_TO_SHORT:
                transcrip[i] = LONG_TO_SHORT[transcrip[i]]

    return transcrip

def process_al(transcrip):
    """
    Adjusts pronuncation to account for 'al' particle. If the initial consonant is a
    sun leter, removes /l/ and lengthens the initial consonant.
    """

    transcrip[0] = '?a'
    if transcrip[2] in SUN_LETTERS:
        transcrip[1] = transcrip[2]
        transcrip[2] = ":"

    return transcrip

def add_short_vowels(transcrip, contains_al):
    """
    Adds a fatha (short /a/) to the first syllable of the word, if:
    1) the word begins with a non-hamza consonant
    2) it has no pre-existing short vowels in the first syllable
    3) the initial consonant is not followed by an alif

    If the added fatha precedes a long vowel, changes the long vowel to its
    consonant equivalent.

    """

    if contains_al:
        start = 2
    else:
        start = 0

    if transcrip[start] in CONSONANTS.values():
        next = transcrip[start + 1]
        if not next in SHORT_VOWELS.values() and not next == 'a' and not next == 'A:':
            transcrip.insert(start + 1, 'a')
            # change following long vowel pronunciation
            if next in LONG_TO_SHORT.keys():
                transcrip[start + 2] = LONG_TO_SHORT[next]

    return transcrip


if __name__ == "__main__":
    main()








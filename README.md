arabicxsampa
============

Arabic-X-SAMPA Transcriber

This program reads in a file of Arabic words with one word per line, and outputs a tab-delimited file
consisting of the original Arabic word and its X-SAMPA transcription.

The command line arguments are:

<input_file>

This program is meant to be a preliminary attempt at the complicated task of Arabic transcription. Issues
addressed include:

- various pronunciations of the 'al' particle
- alternate long vowel and consonant pronunciations of the letters alif, waw, and ya
- short vowels and other diacritical marks

The program functions by constructing a "first pass" transcription using dictionaries of Arabic
characters to X-SAMPA sequences. It then adjusts the transcription of the word-final tanween and
alif maqsura characters.The transcription is then passed to various "filter" methods that adjust the
representation of long and short vowels, and the "al" particle.

Note: This program provides transcriptions for both voweled and unvoweled words. However, because
short-vowel distributions are word-specific, this program will not provide an exact transcription for
every unvoweled word. Instead, it takes a holistic approach in attempting to provide a reasonably accurate
transcription without resorting to using dictionaries of individual words. Because many Arabic words
have an fatha short vowel in the first syllable, this program inserts one if no other short vowel is present.


# acronym-finder
This program finds acronyms in the text and provides their in-text definitions if they exist.

This implementation is based on the paper entitled "Recognizing acronyms and their definitions" by K.Taghva and J.Gilbert published in 1999. Source: https://link.springer.com/article/10.1007/s100320050018

This implementation is not identical since we take a 16 word window on both sides of the acronym whose definition is to be extracted.

To run program, in command prompt run:
 
   python finder.py filename

Where filename may be text.txt, text1.txt, etc.

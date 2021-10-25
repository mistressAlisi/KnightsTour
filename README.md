# KnightsTour
The Knights' Tour is an exercise in computing science, algorithms and it's just a fun toy to play with!
In essence, it is a combination of a Trie string walker, and a Chess player that only knows how to move knights around.

The algorithm will efficiently search through a space-separated list of words, organised into a Trie structure:
These words will be matched against the characters stored inside an 8x8 matrix that represents a chess board. 
For each position on the board, Knight's tour will visit it first (only if its character matches strings in the Trie struct):

Then, Knights tour will recursively descend down the tree of possible moves that each individual square visited presents; with the
constraint that it only visits squares that contain characters that -are- found in the next node of the Trie in order to find the longest possible
string contained in the Trie, that is possible with the characters specified in the matrix.

In order to keep the algorithm fast, efficient and without doing a lot of deep recursion, the solution was implemented using a recursive chess walker defined in
"run_knights_tour" and "get_moves".

A series Shakespeare's plays have been scrapped from HTML to Text word lists and are located in texts/. 
Furthermore, a file 'test.txt' includes a supplied original small list of words that serve as a unit test for the algorithm presented in the Knights Tour.
All of the texts included in texts/ have their equivalent output supplied in outputs/OUT_filename.txt.

To run the code, simply execute it using Python3. No extra modules besides the standard Linux3 python modules should be required.
(For reference, those modules are: sys,getopt,urllib,re,string,argparse,bs4)
# To execute the Tour - knightsTour.py:
./knightsTour.py [file_name] is all that is necessary: for example: ./knightsTour texts/lll.txt. Output will be produced in STDOUT.
You might need to try python3 ./knigtsTour.py on some systems for the tool to execute correctly.

# To convert more HTML files to TXT files - html2txt.py:
We've also supplied a very small utility to scrape HTML Files to text output for this test. it is called html2txt.py
Html2txt efficiently strips out Markup, styles and punctuation only leaving a space-separated list of words ready to be used with
knightsTour. Usage is as follows:
./html2txt.py [in_url] [out_file]
URL addresses are supported in the in_url parameter.

# Surprise!
Is isn't it ironic, that provided with our matrix, the longest possible string matched inside 'Romeo and Juliet' is [INAUSPICIOUS]?

And for those interested in <em>Love's Labour's Lost</em>, the longest possible string is [ODOURIFEROUS]. ;)

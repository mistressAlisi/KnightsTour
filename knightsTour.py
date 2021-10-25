#!/usr/bin/python3
import argparse
# *** Definitions:
# Let's create our Classes first:
# The KnightPos class represents a position on a board of chess (A 8x8 Matrix):
# For convenience it includes a char function which gets the char from the matrix at the position held by the class:
class KnightPos:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "KnightPos=[y={},x={},char={}]".format(self.y, self.x,self.char())
    
    def char(self):
        return Matrix[self.x][self.y]

# This is the critical helper function of KnightsPos: get_moves: 
# get_moves implements a rapid algorithm to find valid possible next moves
# on the board, following the mathematical model that represents movements
# of Knight pieces on the board:
def get_moves(start, size,depth=0):
    moves = list()
    moves.append(KnightPos(start.x + 1, start.y + 2))
    moves.append(KnightPos(start.x + 1, start.y - 2))
    moves.append(KnightPos(start.x - 1, start.y + 2))
    moves.append(KnightPos(start.x - 1, start.y - 2))
    moves.append(KnightPos(start.x + 2, start.y + 1))
    moves.append(KnightPos(start.x + 2, start.y - 1))
    moves.append(KnightPos(start.x - 2, start.y + 1))
    moves.append(KnightPos(start.x - 2, start.y - 1))
    valid_moves = [
                   pos for pos in moves if
                   pos.x >= 0 and pos.x < size and
                   pos.y >= 0 and pos.y < size
                   ]
    return [valid_moves,depth+1]


# We will use a Trie structure to efficiently search through the words loaded from the supplied text file.
# Since Tries are a type of tree; we must define two classes, the Trie's tree struct, 
# and the TrieNode struch which will represent Nodes inside the Trie. 
# To keep track if we have found the end of a string, each TrieNode also carries an endOfString Boolean Flag.
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = TrieNode("")
    
    # The Insert function implements inserting a word into a Trie tree, creating nodes as needed and inserting nodes in the right position of the tree:
    def insert(self, word):
        node = self.root
        #traverse the word character by character 
        for char in word:
            #check if the character is there in the list of children 
            if char in node.children:
                node = node.children[char]
            else:
                # else make a new TrieNode corresponding to that character 
                new_node = TrieNode(char)
                # add the new node to the list of children 
                node.children[char] = new_node
                node = new_node
        #after traversing the word set .is_end to true for the last #char
        node.is_end = True
    
    # Depth-first-search is the basic algorithm that we will use to traverse the Trie: It is an efficient,
    # and fast way to traverse a tree and create a "breadcrumb" of letters in the stack:
    def dfs(self, node, pre):
        if node.is_end:
            self.output.append((pre + node.char))
        for child in node.children.values():
            self.dfs(child, pre + node.char)
    
    # search merely implements our DFS algorithm and returns the number of children (or an empty array) with the nodes
    # that match the search string supplied to the function:
    def search(self, x):
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []
         
        self.output = []
        self.dfs(node, x[:-1])
        return self.output
        
        

    

# This is our Matrix to do matching against:
# For all intents and purposes, it is an 8x8 standard Chess game from 
# a mathematical perspective:
# The characters just represent values held by each position on the board.
Matrix = [
    ['E','X','T','R','A','H','O','P'],
    ['N','E','T','W','O','R','K','S'],
    ['Q','I','H','A','C','I','Q','T'],
    ['L','F','U','N','U','R','X','B'],
    ['B','W','D','I','L','A','T','V'],
    ['O','S','S','Y','N','A','C','K'],
    ['Q','W','O','P','M','T','C','P'],
    ['K','I','P','A','C','K','E','T']
]



# *** Okay, that's all of our classes and our Matrix for Data. From here on out, it's functions that implement the Knight's tour and the Trie walking:

# run_knights_tour is a modified Chess-board walker that recursively explores possible next moves:
# But, unlike normal chess walkers that use a visited set to keep track of piece positions and avoid endless
# recursion, our knights_tour implementation relies on the Trie: To keep the solution fast and efficient,
# and to avoid uncessary recusive loops, knights_tour exclusively visits nodes and sub nodes where the canidate
# string matches the Trie. It will never visit nodes where the candidate strings do not match. 
# once the moves tree (or the Trie) are thoroughly explored; knights_tour returns the longest found string for the tour:
def run_knights_tour(start, size, current_string="",depth=0,CurrentString="",CurrentLength=0):
    moves_data = get_moves(start, size,depth)
    moves = moves_data[0]
    depth = moves_data[1]

    candidate = current_string
    for move in moves:
        candidate = current_string + move.char()
        # Only visit moves that yield candidate strings that are found in our trie:
        if (len(WordsTrie.search(candidate)) > 0):
            # IF we have a single candidate left, we're at the end of our journey!:
            candidate_search  = WordsTrie.search(candidate) 
            if (len(candidate_search)==1):
                return (candidate_search[0])
            # Else, keep going, and only replace our current longest string by one that's longer:
            # Recursively traverse the moves:
            candidate = run_knights_tour(move, size,candidate,depth,CurrentString,CurrentLength)
            candidate_length = len(candidate)
            if (candidate_length > CurrentLength):
                CurrentString = candidate
                CurrentLength = candidate_length
            depth += 1

    return CurrentString


# the_grand_tour is a combination Chess player and Trie walking function. Using the matrix representation of the board,
# a loaded trie of words, it will progressively visit each position of the board, and execute a full depth Knight's tour,
# in an attempt to find the longest string. It uses the recursive Chess/Trie walker run_knights_tour above; and keeps track
# of the string result of each square (each square is in the matrix is run by a run_knights_tour call) - the_grand_tour then
# keeps track of the length of strings returned and keeps only the longest string returned by any given square.
# Finally, the_grand_tour returns an array of the form [String,Length_of_String,Position_of_String]
# Where Position_of_String is the position the board where the string was found:
def the_grand_tour(size=8):
    count = 0
    longest_string_len = 0
    longest_string = ""
    longest_string_pos = False
    depth = 0
    for i in range(size):
        for j in range(size):
            start = KnightPos(i, j)
            # Don't visit squares that don't hold characters that don't form part our Trie:
            if (len(WordsTrie.search(start.char())) > 0):
                current_string = start.char()
                print("*** Knight is Touring from Square: {},{}:{} ***".format(i,j,start.char()))
                tour_data =  run_knights_tour(start, size,current_string,0)
                tour_len = len(tour_data)
                if (tour_len > longest_string_len):
                    longest_string = tour_data
                    longest_string_len = tour_len
                    longest_string_pos = start 
    return [longest_string,longest_string_len,longest_string_pos]



# After all that setup and definition, we're ready for some fun:
## LET THE USER Define the text file we will be using using argparse:
# If no file is specified, argparse will cause our program to exit:
parser = argparse.ArgumentParser(description='Find the longest possible string matching our Chess and Matrix Matching Game.')
parser.add_argument('fname', metavar='f', type=str, nargs='+',
                    help='Filename contaning space separated list of words to match.')
args = parser.parse_args()


# We will do now is open the provided word file:
words_file = open(args.fname[0],"r")
# And then we will construct a Trie from the words:
dictionary = words_file.read().upper().split(" ")[:-1]
WordsTrie = Trie()
for word in dictionary:
    WordsTrie.insert(word)
    
# Finally - We are ready: Evaluate the_grand_tour of our hypothetical Knight.
# In the end, we will have our longest string, it's length, and position for the entire Matrix Board:
tour_data =  the_grand_tour()
print("*** The longest string in '{}' is: '{}'. It occurs at Position: Y={},X={}. Length is: {}.***".format(args.fname[0],tour_data[0],tour_data[2].x,tour_data[2].y,tour_data[1]))

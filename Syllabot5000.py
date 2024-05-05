# File name: Syllabot5000
# Author: Branden Hernandez
# Date: 10/8/22
# Purpose: Two Data tries to hold words from syllabus, parser and menu creator
# Texas Tech University Department of Computer Science
from PyPDF2 import PdfFileReader
import string

# BuildingBlocks
loop = True
syllabus = ""
none = ""
query = ""
letter = ""
option = ""
options = []
default = "I can't find the answer. Please email the professor."


# Scrapper
def inputFile(syllabusFile, tree, wordTree):
    global syllabus
    pdf = PdfFileReader(syllabusFile)  # 3368_syllabus_fall2022.pdf
    for page in pdf.pages:
        syllabus += page.extractText()
    return parser(syllabus, tree, wordTree)  # feed the paser


def slicer(sentence):
    if sentence[len(sentence) - 1] == " ":  # if the last char is a blank
        sentence = sentence[:len(sentence) - 1]  # truncate string to delete last space
    return sentence


class wordNode:  # Create a node
    def __init__(self):  # override init pass in self
        self.children = {}  # set of children
        self.end = False  # indicate a terminal child


class wordTrie:  # Create trie
    def __init__(self):  # override init pass in self
        self.root = wordNode()  # create root node

    def insertWord(self, word):  # to insert words into trie
        current = self.root  # start at the blank root
        for letter in word:  # letter by letter of word passed in
            node = current.children.get(letter)  # make a node of the letter
            if node is None:  # self explainitory
                node = wordNode()  # create a node
                current.children.update({letter: node})  # add new nodes to hold remaining letters
            current = node  # make node current
        current.end = True  # set current to terminal

    def find(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return None
            current = current.children[letter]
        return current.end


class knowledgeNode:  # Create a node
    def __init__(self):  # override init pass in self
        self.data = ""  # data string to hold the answer
        self.children = {}  # set of children
        self.end = False  # indicate a terminal child


class knowledgeTrie:  # Create trie
    def __init__(self):  # override init pass in self
        self.root = knowledgeNode()  # create root node

    def insertWord(self, sentence, answer):  # to insert words into trie - sentence is user query
        current = self.root  # start at the blank root
        parsed = sentence.split(" ")  # spilt the words apart
        for word in parsed:  # one word at a time
            node = current.children.get(word)  # make a node of the word
            if node is None:  # self explainitory
                node = knowledgeNode()  # create a node
                current.children.update({word: node})  # add new nodes to hold remaining letters
            current = node  # make node current
        current.end = True  # set current to terminal
        current.data = answer  # Payload - answer goes here

    def findAnswer(self, sentence):  # pass in user query
        current = self.root  # start from the root
        parsed = sentence.split(" ")  # split user response into words
        for word in parsed:  # for each word
            if word not in current.children:  # if word is not in trie
                return default  # error response
            current = current.children[word]  # if word is in tree, make current
            answer = current.data  # at end of decent grab the answer
        return answer  # give the answer


# Parser
def parser(syllabus, tree, wordTree):
    A = 0
    Q = 1
    word = ""
    sentence = ""
    ignore = ""
    question = ""
    answer = ""

    for letter in syllabus:
        if letter != ' ':  # If char is not a space
            if letter == '\n':
                ignore = letter
                if sentence != " ":
                    answer += sentence
                    sentence = none  # clear
                    if answer != none:
                        if A >= 1:
                            tree.insertWord(question.lower(), answer)  # add input to knowledgeTrie
                        A += 1
            elif letter in string.punctuation:
                if letter == ':':
                    sentence += word
                    if sentence != none:
                        if Q >= 1:
                            sentence = slicer(sentence)  # remove extra space on end
                            question = sentence  # designate as question
                            options.append(sentence.lower())  # feed the sentence to the menu
                            stuffer = sentence.split(" ")  # if the menu option has more than one word
                            for each in stuffer:  # for each of the menu words
                                wordTree.insertWord(each.lower())  # insert word into trie learning each word
                        Q += 1  # Skip past title of syllabus
                        sentence = none  # clear
                        word = none  # clear
                        answer = none  # clear
                elif letter == '@':  # email
                    # print("-----Program email-----")
                    word += letter
                else:
                    word += letter
            elif letter == '•':
                ignore = letter
            else:
                word += letter  # build the word
        else:  # if there is a space
            if word == none:
                ignore = letter
            else:
                sentence += word + letter  # build the sentence
                word = none  # clear
    return menu(options)  # display menu


def menu(options):
    display = ""
    for i in range(len(options)):  # print each option
        display += f'{i}. {options[i]}' + "\n"  # format options to display numbers
    return display


# Interface
def interface(response, tree, wordTree):
    sentence = none  # clear
    loop = True
    display = none
    response = response.lower()
    if response == "exit":
        loop = False
    word4word = response.split(" ")  # split response fromuser into each word
    for word in word4word:  # for every word in the response
        if wordTrie.find(wordTree, word):  # if Syllabot5000 knows the word
            sentence += word + " "
        else:  # if it doesn't recognize the word
            if loop:
                ignore = word  # ignore words Syllabot5000 doesn't know (Add NN to learn full queries)
            else:  # if loop is false
                display = "Goodbye"  # print("Goodbye")
                sentence = "Goodbye"
    if sentence == none:
        display = "I don't understand, please try again"

    if loop and sentence != none:
        try:
            sentence = slicer(sentence)
            query = options[
                options.index(sentence)]  # if the sentence is in the menu select the menu option and place as query
            display = "Question: " + response + "\n\n" + "Answer: " + tree.findAnswer(
                options[int(options.index(query))])
        except:
            display = default
        query = none  # clear
        sentence = none  # clear
    return display

# ThanksForLooking

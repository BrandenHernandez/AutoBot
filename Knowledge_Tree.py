#File name: Knowledge_Tree
#Author: Branden Hernandez
#Date: 10/8/22
#Purpose: Data trie to hold words from user input and retireve a response

response = input('Say something: ') #get input from user
default = "I can't find the answer. Please email the professor."

class knowledgeNode: #Create a node
    def __init__(self): #override init pass in self
        self.data = "" #string to hold answer
        self.children = {} #set of children
        self.end = False #indicate a terminal child
        
class knowledgeTrie: #Create trie
    def __init__(self): #override init pass in self
        self.root = knowledgeNode() #create root node
        
    def insertWord(self, sentence): #to insert words into trie - sentence is query 
        current = self.root #start at the blank root
        parsed = sentence.split(" ")
        for word in parsed:
            #if word == "=":
            node = current.children.get(word) #make a node of the word
            if node == None: #self explainitory
                node = knowledgeNode() #create a node
                current.children.update({word:node}) #add new nodes to hold remaining letters
            print("I've added the word: ", '\"'+word+'\"') #Confirmation
            current = node #make node current
        current.end = True #set current to terminal 
        current.data = "Test" #Payload - answer goes here!
        
        
    def findAnswer(self, sentence):
        current = self.root
        parsed = sentence.split(" ")
        for word in parsed:
            if word not in current.children:
                return default
            current = current.children[word]
            answer = current.data
        return answer

tree = knowledgeTrie() #create a new knowledgeTrie
tree.insertWord(response.lower()) #add input to knowledgeTrie

answer = input("\nWhat would you like to know from the syllabus?\n") #test
print(knowledgeTrie.findAnswer(tree, answer.lower())) #test with first word from user

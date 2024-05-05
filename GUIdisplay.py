import tkinter.ttk
from tkinter import *
from tkinter import filedialog  # import filedialog module
import Syllabot5000 as SyllaBot

tree = SyllaBot.knowledgeTrie()  # create a new knowledgeTrie to learn questions and answers
wordTree = SyllaBot.wordTrie()  # create a new wordTrie to learn the language of questions


# Function for opening the file explorer window
def browseFiles():
    global menu
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a Syllabus",
                                          filetypes=[("PDF files", "*.pdf"), ("all files", "*.*")])
    label.configure(text="")  # Clear the screen
    menu = SyllaBot.inputFile(filename, tree, wordTree)  # Feed knowledge base and print menu
    display_menu()


def display_text():  # Display QnA
    global entry
    menuOptions.configure(text="")  # Clear the screen
    string = entry.get()  # Get input from user
    label.configure(text=SyllaBot.interface(string, tree, wordTree))


def display_info():  # Display my information
    menuOptions.configure(text="")  # Clear the screen
    label.configure(
        text="\nAuthor: Branden Hernandez\n\nDate: 11-24-22\n\nPurpose: Read in a Syllabus and answer questions about "
             "it.\n")


def display_credit():  # Display my information
    menuOptions.configure(text="")  # Clear the screen
    label.configure(
        text="\n\nDate: 11-24-22\n\nPurpose: Read in a Syllabus and answer questions about ")


def display_menu():  # Display my information
    menuOptions.configure(text=menu)  # Clear the screen


window = Tk()
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)
# Set window title
window.title('Syllabot - Your Personal Syllabus Helper')

# Set window size
#window.attributes('-fullscreen', True)

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)  # File menu
menubar.add_cascade(label="About", menu=aboutmenu)  # About menu

filemenu.add_command(label="Add Syllabus", command=browseFiles)
filemenu.add_command(label="Menu Options", command=display_menu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

aboutmenu.add_command(label="Info", command=display_info)
#aboutmenu.add_command(label="Credit", command=display_credit)

window.config(menu=menubar)

# Initialize a Label to display the User Input
menuOptions = Label(window, text="", font="Ariel 12")
menuOptions.pack()

label = Label(window, text="Welcome to Syllabot\n\nPlease upload a syllabus",
              font="Ariel 12 bold")

label.pack()

# Create an Entry widget to accept User Input
entry = Entry(bottomFrame, width=200)
entry.focus_set()
entry.pack()
# Create a Button to validate Entry Widget
tkinter.ttk.Button(bottomFrame, text="Okay", width=40, command=display_text).pack()

window.mainloop()

# Thanks for looking

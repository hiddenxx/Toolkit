# A Menu consists of one or more sub-Menu objects that a user can choose
# to run or subroutines that the user can call.


import sys
sys.path.insert(0,'/hiddenx/Toolkit/Google_Drive')
sys.path.insert(1,'/hiddenx/Toolkit/toolkitlogs')

from gDriver import display_files_and_folders
import logger

logger = logger.get_logger(__name__)
class Menu:

    # Constructor
    def __init__(self):
        self.options = {}
        self.setPrompt("Please choose an option:")
        self.setErrorText("Error! Please enter a valid option.")

    # Adds an option to this Menu. An option consists of a number,
    # name, and the actual object it corresponds to (submenu or procedure).
    # The last value in each key-value pair denotes whether the given option
    # should trigger an exit from the current Menu after it is called.
    def addOption(self, optionNumber, optionName, option, TriggersExit):
        self.options[optionNumber] = [optionName, option, TriggersExit]

    # Sets this Menu's error text
    def setErrorText(self, errorText):
        self.errorText = errorText

    # Sets this Menu's prompt
    def setPrompt(self, prompt):
        self.prompt = prompt

    # Returns the number of options in this Menu
    def size(self):
        return len(self.options)

    # Displays this Menu's error text
    def displayError(self):
        print("\n{}\n".format(self.errorText))

    # Prints the Menu in its entirety
    def display(self):
        print(self.prompt)
        for i in range(1, self.size()+1):
            print("{} - {}".format( i, self.options[i][0] ))
        print()

    # Runs this Menu
    def run(self):
        userInput = ""
        self.display()
        while True:
            userInput = input("Your selection: ")
            try:
                userInput = int(userInput)
                if userInput <= 0 or userInput > self.size():
                    self.displayError()
                else:
                    # If the menu option is a function, call it
                    if callable(self.options[userInput][1]):
                        self.options[userInput][1]()
                        # And if it's an option that triggers a return/exit, then return after it's called
                        if self.options[userInput][2]:
                            return
                        # Otherwise, redisplay the menu options
                        else:
                            self.display()
                    # But if the menu option is a submenu, run it
                    else:
                        self.options[userInput][1].run()
                        # And display the calling menu's options again upon return from the submenu
                        self.display()
            except ValueError:
                self.displayError()
def Return():
    return
def Exit():
    exit(1)


def menuController():
    mainMenu = Menu()
    mainMenu.setPrompt("Toolkit for SOCs")
    logger.info("Setting up Menu.")
    googleMenu = Menu()
    googleMenu.setPrompt("Select an Option\n")
    googleMenu.addOption(1,"Display",display_files_and_folders,False)
    googleMenu.addOption(2,"Return",Return,True)

    mainMenu.addOption(1,"Google Drive Toolkit",googleMenu,False)
    mainMenu.addOption(2,"Exit",Exit,True)
    mainMenu.run()

menuController()
# def Option1():
#     values = input("\n\tEnter some values: ")
#     print("\n\tYou entered these values:", end=" ")
#     for i in range(0, len(values)):
#         print(values[i], end=" ")
#     print()
#
# def MyLife():
#     print("\n\tLife's hard.\n")
#
# def GettingHelp():
#     print("\n\tRecursion jokes suck\n")

# def main():
#
#     mainMenu = Menu()
#     mainMenu.setPrompt("\nSelect an option:")
#
#     menu1 = Menu()
#     menu1.setPrompt("\nSelect an option:")
#     menu1.addOption(1, "Option1", Option1, False)
#     menu1.addOption(2, "Return", Return, True)
#
#     menu2 = Menu()
#     menu2.setPrompt("\nWhat would you like help with?")
#     menu2.addOption(1, "My life", MyLife, False)
#     menu2.addOption(2, "Getting help", GettingHelp, False)
#     menu2.addOption(3, "Return", Return, True)
#
#     mainMenu.addOption(1, "Enter new values", menu1, False)
#     mainMenu.addOption(2, "Help", menu2, False)
#     mainMenu.addOption(3, "Exit", Exit, True)
#     mainMenu.run()

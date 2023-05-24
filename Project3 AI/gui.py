from Tkinter import *
import tkFileDialog

def fileinput():
    """
    This function creates a Tkinter gui window to collect the files containing data to
    be loaded into the program. It contains all the necessary sub-functions to do so.
    :return: a 3-tuple of filenames
    """
    def submitfiles():
        """
        This function is executed when the submit button is pressed. It collects the
        entered filenames, quits if a filename has not been enteres, and if there
        are files it stores them in the global files variable.
        :return: None
        """
        global files
        attributesFile = attributesEntry.get().split('/')[-1]
        constraintsFile = constraintsEntry.get().split('/')[-1]
        preferencesFile = preferencesEntry.get().split('/')[-1]
        if attributesFile == '' or constraintsFile == '' or preferencesFile == '':
            print("Error: a file has not been specified")
            sys.exit()
        files = attributesFile, constraintsFile, preferencesFile
        root.destroy()

    def attributesbrowse():
        """
        This function executes when the user presses the browse button in-line with
        the attributes entry box. It opens a tk file dialog window and prints the
        filename into the entry box.
        :return: None
        """
        filename = tkFileDialog.askopenfilename()
        attributesEntry.delete(0, END)
        attributesEntry.insert(0, filename)

    def constraintsbrowse():
        """
        This function executes when the user presses the browse button in-line with
        the constraints entry box. It opens a tk file dialog window and prints the
        filename into the entry box.
        :return: None
        """
        filename = tkFileDialog.askopenfilename()
        constraintsEntry.delete(0, END)
        constraintsEntry.insert(0, filename)

    def preferencesbrowse():
        """
        This function executes when the user presses the browse button in-line with
        the preferences entry box. It opens a tk file dialog window and prints the
        filename into the entry box.
        :return: None
        """
        filename = tkFileDialog.askopenfilename()
        preferencesEntry.delete(0, END)
        preferencesEntry.insert(0, filename)

    def cancel():
        """
        This function destroys the file input window and re-opens the main window.
        :return: None
        """
        root.destroy()
        gui()

    root = Tk()
    root.title("Project 3 - Recommender System - File Input")

    filesFrame = Frame(root)
    filesFrame.pack()
    Label(filesFrame, text="Enter the file names below:").pack()

    attributesFrame = Frame(filesFrame)
    Label(attributesFrame, text="Attributes:   \t").grid(row=0, column=0, columnspan=1)
    attributesEntry = Entry(attributesFrame, width=100)
    attributesEntry.grid(row=0, column=1, columnspan=3)
    Button(attributesFrame, text="Browse", command=attributesbrowse).grid(row=0, column=4)
    attributesFrame.pack(padx=5, pady=5)

    constraintsFrame = Frame(filesFrame)
    Label(constraintsFrame, text="Constraints:\t").grid(row=0, column=0, columnspan=1)
    constraintsEntry = Entry(constraintsFrame, width=100)
    constraintsEntry.grid(row=0, column=1, columnspan=3)
    Button(constraintsFrame, text="Browse", command=constraintsbrowse).grid(row=0, column=4)
    constraintsFrame.pack(padx=5, pady=5)

    preferencesFrame = Frame(filesFrame)
    Label(preferencesFrame, text="Preferences:\t").grid(row=0, column=0, columnspan=1)
    preferencesEntry = Entry(preferencesFrame, width=100)
    preferencesEntry.grid(row=0, column=1, columnspan=3)
    Button(preferencesFrame, text="Browse", command=preferencesbrowse).grid(row=0, column=4)
    preferencesFrame.pack(padx=5, pady=5)

    buttonFrame = Frame(root)
    Button(buttonFrame, text="Submit Files", command=submitfiles).grid(row=0, column=0)
    Frame(buttonFrame, width=25).grid(row=0, column=1)
    Button(buttonFrame, text="Cancel", command=cancel).grid(row=0, column=2)
    buttonFrame.pack(pady=5)

    mainloop()
    return files

def manualinput():
    """
    This function opens a Tkinter window to allow the user to manually enter attributes,
    constraints, and preferences data. This data is writen to files and returned.
    :return: a 3-tuple of files
    """
    def write2file(filename, text):
        """
        This function writes given data to a given filename.
        :param filename:    a string that will be the name of the file written to
        :param text:    the data captured by the text windows upon submission
        :return:    None
        """
        try:
            f = open(filename, "w")
        except:
            print("error opening file to write data to")
        f.write(text)
        f.close()

    def submitdata():
        """
        This function gathers the text inside the text windows, sends it and a placeholder
        filename to the write2file function, stores the file names in the files 3-tuple, and
        destroys the data input window.
        :return:    None
        """
        global files
        attributesData = attributesText.get('0.0', END)
        constraintsData = constraintsText.get('0.0', END)
        preferencesData = preferencesText.get('0.0', END)
        # the following catches if user submits before entering any data
        if len(attributesData) == 1 or len(constraintsData) == 1 or len(preferencesData) == 1:
            print("Error: no data was entered")
            sys.exit()
        write2file('a.txt', attributesData)
        write2file('c.txt', constraintsData)
        write2file('p.txt', preferencesData)
        files = 'a.txt', 'c.txt', 'p.txt'
        root.destroy()

    def cancel():
        """
        This function destroys the data input window and re-opens the main window.
        :return:    None
        """
        root.destroy()
        gui()

    def help():
        """
        This function is executed when the Help button is pressed. It opens a window that
        contains a message describing the accepted data formats. It closes only when the user
        closes the window.
        :return: None
        """
        helproot = Tk()
        helproot.title("Project 3 - Recommender System - Help")
        Label(helproot, text="Below are the accepted data formats for this system.").pack()
        Frame(helproot, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)
        message = """              Attributes Data:
              appetizer: soup, salad
              entree: beef, fish
              drink: beer, wine
              dessert: cake, ice-cream
              ...
            
              Constraints Data:
              NOT soup OR NOT beer
              NOT soup or NOT wine
              ...
              
              Preferences Data:
              fish AND wine, 10
              wine OR cake, 6
              ..."""
        Message(helproot, text=message).pack(fill=X)
        Frame(helproot, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    root = Tk()
    root.title("Project 3 - Recommender System - Manual Input")

    dataFrame = Frame(root)
    dataFrame.pack(fill=X)
    Label(dataFrame, text="Enter your data below (or press Help to see accepted data formats):").pack()

    Frame(dataFrame, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    Label(dataFrame, text="Attributes:   \t").pack(side=TOP)
    attributesFrame = Frame(dataFrame)
    scrollbarY = Scrollbar(attributesFrame)
    scrollbarY.pack(side=RIGHT, fill=Y)
    attributesText = Text(attributesFrame, height= 10,
                          font=("Courier New", 12),
                          yscrollcommand=scrollbarY.set)
    attributesText.pack(fill=X)
    scrollbarY.config(command=attributesText.yview)
    attributesFrame.pack()

    Frame(dataFrame, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    Label(dataFrame, text="Constraints:\t").pack()
    constraintsFrame = Frame(dataFrame)
    scrollbarY = Scrollbar(constraintsFrame)
    scrollbarY.pack(side=RIGHT, fill=Y)
    constraintsText = Text(constraintsFrame, height=10,
                           font=("Courier New", 12),
                           yscrollcommand=scrollbarY.set)
    constraintsText.pack(fill=X)
    scrollbarY.config(command=constraintsText.yview)
    constraintsFrame.pack()

    Frame(dataFrame, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    Label(dataFrame, text="Preferences:\t").pack()
    preferencesFrame = Frame(dataFrame)
    scrollbarY = Scrollbar(preferencesFrame)
    scrollbarY.pack(side=RIGHT, fill=Y)
    preferencesText = Text(preferencesFrame, height=10,
                           font=("Courier New", 12),
                           yscrollcommand=scrollbarY.set)
    preferencesText.pack(fill=X)
    scrollbarY.config(command=preferencesText.yview)
    preferencesFrame.pack()

    Frame(root, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    buttonFrame = Frame(root)
    Button(buttonFrame, text="Submit Data", command=submitdata).grid(row=0, column=0)
    Frame(buttonFrame, width=25).grid(row=0, column=1)
    Button(buttonFrame, text="Help", command=help).grid(row=0, column=2)
    Frame(buttonFrame, width=25).grid(row=0, column=3)
    Button(buttonFrame, text="Cancel", command=cancel).grid(row=0, column=4)
    buttonFrame.pack(pady=5)

    mainloop()
    return files

def gui():
    """
    This function executes the main window of this program. It simply asks the user
    whether they would like to enter their data manually or through files, and then
    executes the function corresponding to the choice. It returns the 3-tuple of
    file names that each of the input windows return.
    :return:    a 3-tuple of file names
    """
    def fromtext():
        """
        This function executes if the user presses the Manually button. It calls
        the manualinput() function and stores the results into the global files
        variable.
        :return:    None
        """
        global files
        root.destroy()
        try:
            files = manualinput()
        except NameError:
            print("Data collection aborted.")
            sys.exit()

    def fromfiles():
        """
        This function executes if the user presses the From files button. It calls
        the fileinput() function and stores the results into the global files variable.
        :return:    None
        """
        global files
        root.destroy()
        try:
            files = fileinput()
        except NameError:
            print("File specification aborted.")
            sys.exit()

    root = Tk()
    root.title("Project 3 - Recommender System")

    label = Label(root, text="Please choose how you would like to enter your data.")
    label.pack(padx=30, pady=10)

    buttonFrame = Frame(root)
    manualButton = Button(buttonFrame, text="Manually", command=fromtext)
    manualButton.pack(side=LEFT, padx=15)
    filesButton = Button(buttonFrame, text="From files", command=fromfiles)
    filesButton.pack(side=RIGHT, padx=15)
    buttonFrame.pack(pady=5)

    mainloop()
    try:
        return files
    except NameError:
        print("Program aborted.")
        sys.exit()
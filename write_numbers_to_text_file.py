#write_numbers_to_text_file.py
#Writes a range of numbers between and including two numbers inputted by the user to a text file, with one number per line.
#Author: Charley Johnston
#Date: December 3, 2018

#V2 - Added undo function

from Tkinter import *
import tempfile
import base64
import zlib

#################################################

def check_if_E2_bigger_than_E1():

    global E1, E2
    
    if ( (int (E1.get() ) <= int( E2.get() ) ) ):
        return True
    else:
        return False

#################################################

def check_if_positive(get):
    if int(get) < 0:
        return False
    return True

#################################################
    
def check_if_number(get):

    try:
       val = int(get)
    except ValueError:
       return False
    return True

#################################################
   
def get_entries():

    global min_number, max_number, label3_text, item_class, root

    #Blank entries
    if E1.get() == "" or E2.get() == "":

        #Both blank entries
        if E1.get() == "" and E2.get() == "":
            label3_text.set("Error: Please input at least one value.")
            
        #Just E2 has an entry
        elif E1.get() == "" and E2.get() != "":

            #Check if input is a number
            if check_if_number( str(E2.get()) ):
                
                #Check if input is positive
                if check_if_positive( str(E2.get()) ):
                    label3_text.set("Min = Max = " + str( E2.get() ) + ", added to file.")
                    min_number = int(E2.get())
                    max_number = min_number
                    add_to_history(min_number, max_number)
                    item_class = str(E3.get())
                    add_to_text_file()
                    
                else:
                    label3_text.set("Error: Please only input positive numbers.")
                
            else:
                label3_text.set("Error: Please only input numbers.")

        #Just E1 has an entry
        elif E1.get() != "" and E2.get() == "":

            #Check if input is a number
            if check_if_number(str(E1.get())):

                #Check if input is positive
                if check_if_positive( str(E1.get()) ):
                    label3_text.set("Min = Max = " + str( E1.get() ) + ", added to file.")
                    min_number = int(E1.get())
                    max_number = min_number
                    add_to_history(min_number, max_number)
                    item_class = str(E3.get())
                    add_to_text_file()
                    
                else:
                    label3_text.set("Error: Please only input positive numbers.")
                
            else:
                label3_text.set("Error: Please only input numbers.")

    #Both E1 and E2 have entries 
    elif E1.get() != "" and E2.get() != "":

        #Check if inputs are numbers
        if check_if_number(str(E1.get())) and check_if_number(str(E2.get())):

            #Check if entries are positive numbers
            if check_if_positive( str(E1.get()) ) and check_if_positive( str(E2.get()) ):

                #Check that right entry is bigger than left entry
                if check_if_E2_bigger_than_E1():
                    label3_text.set("Min = " + str( E1.get() ) + " Max = " + str( E2.get() ) + ", added to file.")
                    min_number = int(E1.get())
                    max_number = int(E2.get())
                    add_to_history(min_number, max_number)
                    item_class = str(E3.get())
                    add_to_text_file()
                    
                else:
                    label3_text.set("Error: Right entry should be <= left entry")

            else:
                label3_text.set("Error: Please only input positive numbers.")
                
        else:
             label3_text.set("Error: Please only input numbers.")

#################################################

def add_to_text_file():

    global min_number, max_number, text_file_name, text_and_class_file_name, item_class
                
    #File with numbers and class
    try:
        with open(text_and_class_file_name, 'a') as the_file:

            for i in range(min_number, int(max_number) + 1):
                the_file.write(str(i) + "/" + str(item_class) + "/\n")

    except:
        with open(text_and_class_file_name, 'w') as the_file:

            for i in range(min_number, int(max_number) + 1):
                the_file.write(str(i) + "/" + str(item_class) + "/\n")


#############################################################################

def add_to_history(min_value, max_value):

    global min_number_history, max_number_history

    min_number_history.append(min_value)
    max_number_history.append(max_value)

#############################################################################

def find_str(s, char):
   index = 0

   if char in s:
       c = char[0]
       for ch in s:
           if ch == c:
               if s[index:index+len(char)] == char:
                   return index

           index += 1

   return -1

#################################################

#~~~~~~~~~Finish~~~~~~~~~~~~#
def undo_function():

    global min_number_history, max_number_history

    values = []

    try: 
        min_value = min_number_history.pop()
        max_value = max_number_history.pop()

        for i in range(min_value, max_value + 1):
            values.append(i)

        f = open("frame_and_class_list.txt","r")
        lines = f.readlines()
        f.close()

        f = open("frame_and_class_list.txt","w")
        for line in lines:
        
          contains = 0

          for i in range(len(values)):
              if find_str(line, str(values[i])) != -1:
                  contains = 1

          if contains == 0:
            f.write(line)

        
        f.close()

    except IndexError:
        label3_text.set("Error: There's nothing left to undo!")

#################################################

ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)
    
#Root
root = Tk()
root.iconbitmap(default=ICON_PATH)
root.title('')

#Labels
label_min = Label(root, text='\nMin', borderwidth=10).grid(row=1,column=1)
label_max = Label(root, text='\nMax', borderwidth=10).grid(row=1,column=3)

label1 = Label(root, text='Enter your range of numbers to\n write them to the text file.', borderwidth=10).grid(row=1,column=2)

label2 = Label(root, text='<-----------  from to  ----------->', borderwidth=10).grid(row=2,column=2)
label4 = Label(root, text='Item class', borderwidth=10).grid(row=3,column=2)

label3_text = StringVar()
label3 = Label(root, textvariable=label3_text, borderwidth=10).grid(row=5,column=2)
label3_text.set('Press "Enter" to write to the file!')

#Entries
E1 = Entry(root, borderwidth=5 )
E1.grid(row=2,column=1, padx=10, pady=5)

E2 = Entry(root, borderwidth=5 )
E2.grid(row=2,column=3, padx=10, pady=5)

E3 = Entry(root, borderwidth=5 )
E3.grid(row=4,column=2, padx=10, pady=5)

#Button
submit = Button(root, text ="Enter", command = get_entries).grid(row=6,column=2, padx=10, pady=10)
undo_button = Button(root, text ="Undo", command = undo_function).grid(row=6,column=3, padx=10, pady=10)

#Prevents resize of window
root.grid_columnconfigure(2, minsize=250)

min_number = 0
max_number = 0

#History for undo
min_number_history = []
max_number_history = []
item_class_history = []

item_class = ""

text_file_name = "frame_list.txt"
text_and_class_file_name = "frame_and_class_list.txt"

root.mainloop()

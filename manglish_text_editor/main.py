from transiterator import generate_word_list
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

init_dir = ''  # folder to work
global file_name
file_name = False


def translate_word(wd):
    """Searches the possible word list in the database and returns result"""

    word_list = generate_word_list(wd)

    if str(type(word_list[0])) == "<class 'tuple'>":
        result = word_list[0][0]
    else:
        result = word_list[0]
    return result


class MyApp(Tk):
    """
    Inherits the tkinter class to modify its functionalities.
    """

    def __init__(self):
        super().__init__()
        self.geometry("640x500")
        self.title("Manglish Text Editor")

        # Adding menu bar
        self.menu_bar = tk.Menu(self)
        # Adding file menu
        file_menu = tk.Menu(self.menu_bar, title='my title', tearoff=False)  # file
        self.menu_bar.add_cascade(label="file", menu=file_menu)  # Top Line
        file_menu.add_command(label="New", command=lambda: self.new_file())
        file_menu.add_command(label="Open..", command=lambda: self.open_file())
        file_menu.add_command(label="Save", command=lambda: self.save_file())
        file_menu.add_command(label="Save As..", command=lambda: self.save_as_file())
        file_menu.add_command(label="Close", command=lambda: self.close_file())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Add edit menu
        edit_menu = tk.Menu(self.menu_bar, title='my title', tearoff=False)  # file
        self.menu_bar.add_cascade(label="edit", menu=edit_menu)  # Top Line
        # TODO : Add option for malayalam keyboard, Convert an entire file from manglish to malayalam, Delete file
        edit_menu.add_command(label="Malayalam Keyboard", command=lambda: self.new_file())
        edit_menu.add_command(label="Convert File", command=lambda: self.open_file())
        edit_menu.add_command(label="Delete File", command=lambda: self.save_file())

        self.config(menu=self.menu_bar)  # adding menu to window

        # create a scroll_bar and associate it with txt
        self.scroll_bar = ttk.Scrollbar(self)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        # Adding text box and adding scroll bar for it.
        self.eng_text = tk.Text(self, selectbackground='yellow', selectforeground='black', undo=True,
                                yscrollcommand=self.scroll_bar.set, height=500)
        self.eng_text.bind("<space>", self.translate)
        self.eng_text.bind("<Return>", self.translate)
        self.eng_text.pack(side=LEFT, expand=True, fill=X)
        self.scroll_bar.config(command=self.eng_text.yview)

        # Add status bar at the bottom
        # status_bar = Label(self, text="Ready", anchor=E)
        # status_bar.grid(row=1)
        # status_bar.pack(fill=X, side=BOTTOM)

    def translate(self, event):
        """
        The method translates manglish text to malayalam using trans-iterate method.

        :param event: The event
        :return: None
        """
        final_result = ''
        sub_string = ''
        word = str(self.eng_text.get(0.0, tk.END)).rstrip("\n").split(" ")[-1].split('\n')[-1]
        current_mal_text = str(self.eng_text.get(0.0, tk.END)).rstrip('\n').rstrip(word)
        # Translating alphabets avoiding non-alphabetic characters
        for element in word:
            if element.isalpha():
                sub_string += element
            else:
                result = translate_word(sub_string) if sub_string else ''
                final_result += result + element
                sub_string = ''
        if sub_string:
            final_result += translate_word(sub_string) if sub_string else ''
        self.eng_text.delete(1.0, tk.END)
        self.eng_text.insert(0.0, current_mal_text)
        self.eng_text.insert(tk.END, final_result)

    def new_file(self):
        # Delete previous text
        self.eng_text.delete('1.0', END)

        global file_name
        file_name = False

    def open_file(self):
        # Delete previous text
        self.eng_text.delete('1.0', END)
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Rtf File", '*.rtf'),
                                                     ("All Files", '*.*')],
                                          defaultextension=".txt", initialdir=init_dir, title='Open File')
        if file:
            # Make file global so that it can be accessed on saving.
            global file_name
            file_name = file  # set the file name
            self.title(file_name)  # update the GUI title
            fob = open(file, 'r')  # open in read mode
            my_str1 = fob.read()  # read data from file & store in variable
            self.eng_text.insert(tk.END, my_str1)  # add new data from file to text box
            fob.close()

    def save_file(self):
        global file_name
        if file_name:  # if default file name is still there
            fob = open(file_name, 'w')  # open the file in write mode
            my_str1 = self.eng_text.get("1.0", tk.END)  # collect data from text widget
            fob.write(my_str1)  # write to file
            self.title(file_name)  # Update the GUI title with file name
            fob.close()  # Close file pointer
        else:
            self.save_as_file()  # call the function

    def save_as_file(self):
        file = filedialog.asksaveasfilename(
            title='Save File',
            filetypes=[("Text Files", "*.txt"), ("Rtf File", '*.rtf'),
                       ("All Files", '*.*')],
            defaultextension=".*", initialdir=init_dir)
        if file:  # if user has not cancelled the dialog to save
            fob = open(file, 'w')  # open the file in write mode
            my_str1 = self.eng_text.get("1.0", tk.END)  # collect data from text widget
            fob.write(my_str1)  # write to file
            self.title(file)  # Update the GUI title with file name
            fob.close()  # Close file pointer
        else:  # user has cancelled the operation
            print("No file chosen")

    def close_file(self):
        self.save_file()  # remove this line if not required
        self.eng_text.delete('1.0', tk.END)  # remove the content from text widget
        self.title('')  # remove the title of GUI

        global file_name
        file_name = False


if __name__ == "__main__":
    print("Running")
    myapp = MyApp()
    myapp.mainloop()

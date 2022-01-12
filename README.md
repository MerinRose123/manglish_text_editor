# Manglish Text Editor

This is a simple transliteration (romanization ) program which is used to convert manglish to malayalam (converts njaan 
to ഞാൻ ). It is aimed to help people who have difficulty in typing malayalam and who is good in typing English.

Tkinter is used for text editor creation and simple database lookup along with frequency data is used for the 
transliteration program.

# Requirements
  * The system should have python3 installed. Ths system i tested on python 3.8.
  * The system works on linux and Mac. Minor changes may be required to run this on windows.
  * The code requires tkinter to be installed. `pip install tk` command can be used for this.

# How to use
  * download or clone the repository using command `git clone <repo_address>`
  * It is recommended to run the code in a separate virtual environment.
  * Get into the main folder `manglish_text_editor` by `cd manglish_text_editor` in terminal.
  * When you run the program for the first time the frequency table needs to get created. For that run `python3 transiterator.py`. Note that it is a time consuming operation. 
  * run `python3 main.py`. This will open the text editor in another window.
  * The text editor is self explanatory.
  
# How it works
The program makes up a database of possible english typings of a malayalam word
and then for each user input it tries to find a near match in the database and along with that 
tries to create the original word.

![Text editor image](https://github.com/MerinRose123/manglish_text_editor/blob/main/text_editor.png?raw=true)

The text editor is created using python package named tkinter.

# Features
 * Text editor in which the typed english(manglish) word will be converted to malayalam on pressing space or enter key.
 * The text editor has options file save, open, save as, new etc.

# Future Scope
  1. Improve tokenizing
  2. use a better method to remove noise
  3. Improve learning algorithm
  4. In text editor add malayalam key board, conversion of an entire file at once, Delete file
  5. Give option to the user to select from the possible list of words on backspace press.
  6. Add bold, text space, font, points to the text editor.
  7. Add feature to convert malayalam to manglish.
  8. Add option select all, search, replace etc.

# Contributions
 * Pull requests are welcome. If someone wants to contribute to this project can fork and add the Functionalities.

  
  

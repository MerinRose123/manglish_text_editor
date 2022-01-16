# Manglish Text Editor

This is a simple transliteration (romanization ) program which is used to convert manglish to malayalam (converts njaan 
to ഞാൻ ). It is aimed to help people who have difficulty in typing malayalam and who is good at typing English.

Tkinter which is a python gui tool is used for text editor creation and simple database lookup along with frequency data is used for the 
transliteration program. This improves the accuracy of transliteration.

# Requirements
  * The system should have python3 installed. Ths system is tested on python 3.8.
  * The system works on linux and Mac. Minor changes may be required to run this on windows.
  * The code requires tkinter to be installed in the system.

# How to use
  * download or clone the repository using command `git clone <repo_address>`
  * It is recommended to run the code in a separate virtual environment.
  * Add the required packages by the command `pip install -r requirements.txt`
  * Get into the main folder `manglish_text_editor` by `cd manglish_text_editor` in terminal.
  * When you run the program for the first time the frequency table needs to get created. For that run `python3 transiterator.py`. Note that it is a time consuming operation. 
  * run `python3 main.py`. This will open the text editor in another window.
  * The text editor is self-explanatory.
  
# How it works
The transliteration program makes up a database of possible english typing's of a malayalam word
and then for each user input it tries to find a near match in the database and along with that 
tries to create the original word.

Text editor related functionalities are fulfilled by the options available in tkinter.

![Text editor image](https://github.com/MerinRose123/manglish_text_editor/blob/main/text_editor.png?raw=true)

# Features
 * Text editor in which the typed english(manglish) word will be converted to malayalam on pressing space or enter key.
 * The text editor has options file save, open, save as, new etc.
 * A tool box si added which has basic functionalities like bold, alignment, font color change, underlining etc.

# Future Scope
 1. Improve learning algorithm
 2. In text editor add malayalam keyboard, conversion of an entire file at once, Delete file
 3. Give option to the user to select from the possible list of words on backspace press.
 4. Add feature to convert malayalam to manglish.
 5. Add option select all, points, new window etc.

# Contributions
 * Pull requests are welcome. If someone wants to contribute to this project can fork and add the Functionalities.

  
  

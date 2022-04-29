# pocketbookNotes
Simple project to sort and view exported notes from Pocketbook 4 (in default, notes are mixed from different pages).
## Features
With this program, you can sort and view exported notes and save changes to html or pdf file.  
Current version works only for text notes, can't show bookmarked pages and screenshots.
## Depencencies (libraries)
Below each name of library is shown installation command using package installer for Python (pip):
- [tkinter](https://docs.python.org/3/library/tkinter.html)
```bash
pip install tk
```
- [pdfkit](https://pypi.org/project/pdfkit/)
```bash
pip install pdfkit
```
- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)
```bash
pip install BeautifulSoup
```
## Usage
1. Load exported note from Pocketbook 4 using **"Load unsorted notes"** button.  
1.1 To keep original order use **"Load sorted notes"** button.  
2. After load, all notes are shown as list on left side of window.  
2.1 Double click on note to view note content on the right side of window.  
2.2 Note content can't be edited, just selected. Use **"Copy note to clipboard"** button to copy whole content of selected note.  
2.3 Use **"Move note up"** / **"Move note down"** button to change order in list of notes.  
3. To export , use **"Save notes"** button.  
3.1 Select **.html** extension to save notes in changed order. To edit in future use **"Load sorted notes"** button to open this **.html** file.  
3.2 Select **.pdf** extension to save notes as pdf.  
## License
Project is under [MIT License](LICENSE.md).
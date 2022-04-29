from bs4 import BeautifulSoup
from Note import Note

class Parser:
    def __init__(self):
        self.soup = None

    def parse_html_file(self, file_content):
        notes_list = []
        self.soup = BeautifulSoup(file_content, from_encoding="utf-8", features="html.parser")
        self.soup.prettify()
        notes = self.soup.find_all(class_='bookmark')
        # TODO add title
        for note in notes:
            page_number = note.find(class_='bm-page')
            bookmark_content_node = note.find(class_='bm-text')
            if page_number and bookmark_content_node:
                bookmark_content_text = bookmark_content_node.getText(strip=True)
                #bookmark_content_text = bookmark_content_node.get_text()
                note_object = Note(page=page_number.string, content=bookmark_content_text)
                notes_list.append(note_object)
        return notes_list

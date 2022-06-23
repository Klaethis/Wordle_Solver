from wordle_gui import *

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QScrollArea,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wordle Solver")

        layout = QHBoxLayout()
        
        self.puzzle = WordlePuzzle()
        layout.addWidget(self.puzzle)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.possibilities = words.copy()
        self.possibilities.sort()
        self.dictionary = QLabel('<br>'.join(self.possibilities))
        scroll.setWidget(self.dictionary)
        layout.addWidget(scroll)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
    def keyPressEvent(self, e):
        if e.key() >= 65 and e.key() <= 90: 
            self.puzzle.active_letter.setText(f'{chr(e.key())}')
            self.puzzle.increment_letter()
        elif e.key() == 16777219: # Backspace
            if self.puzzle.active_letter != ' ':
                self.puzzle.active_letter.reset()
            else:
                self.puzzle.decrement_letter()
        elif e.key() == 16777220: # Enter
            self.cull_dictionary()
            self.puzzle.increment_word()
            self.puzzle.active_letter.setFocus()
        elif e.key() == 16777268:
            self.puzzle.reset()
            self.possibilities = words.copy()
            self.dictionary.setText('<br>'.join(self.possibilities))
            for word in self.puzzle.words:
                word.setEnabled(False)
            self.puzzle.active_word.setEnabled(True)
            self.puzzle.active_word.setFocus()
            
    def cull_dictionary(self):
        for letter in self.puzzle.active_word:
            if letter.state == 0:
                clue_count = [x for x in self.puzzle.active_word if x.state > 0].count(str(letter))
                self.possibilities = [word for word in self.possibilities if str(letter) != word[letter.index] and word.count(str(letter)) <= clue_count]
            elif letter.state == 1:
                self.possibilities = [word for word in self.possibilities if str(letter) in word and word[letter.index] != letter.text().lower()]
            elif letter.state == 2:
                self.possibilities = [word for word in self.possibilities if word[letter.index] == str(letter)]
        self.dictionary.setText('<br>'.join(self.possibilities))

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
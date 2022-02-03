import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
)

from words import words

class WordleLetter(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = 2
        self.button_clicked()
        self.clicked.connect(self.button_clicked)
        self._index = 0
    
    @property
    def index(self) -> int:
        return self._index
    @index.setter
    def index(self, value:int):
        self._index = value
        
    def button_clicked(self):
        if self.state == 2:
            self.state = 0
        elif self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 2
        style_color = 'grey' if self.state == 0 else 'yellow' if self.state == 1 else 'green'
        self.setStyleSheet(f'font-size: 40px; background-color: {style_color}')
    
    def reset(self):
        self.state = 2
        self.setText(' ')
        self.button_clicked()
            
class WordleWord(QWidget):
    
    @property
    def active_letter(self):
        return self.letters[self._active_letter]
    
    def increment_letter(self):
        if self._active_letter < len(self.letters) - 1:
            self._active_letter += 1
            
    def decrement_letter(self):
        if self._active_letter > 0:
            self._active_letter -= 1
    
    def __init__(self):
        super().__init__()
        
        self._active_letter = 0
        
        layout = QHBoxLayout()
        self.letters = []
        
        for num in range(5):
            new_letter = WordleLetter(' ')
            new_letter.index = num
            self.letters.append(new_letter)
            layout.addWidget(new_letter)
            
        self.setLayout(layout)
    
    def reset(self):
        for letter in self.letters:
            letter.reset()
        self._active_letter = 0
        
class WordlePuzzle(QWidget):
    
    @property
    def active_letter(self) -> WordleLetter:
        return self.words[self._active_word].active_letter
    
    @property
    def active_word(self) -> WordleWord:
        return self.words[self._active_word]
    
    def increment_letter(self):
        self.active_word.increment_letter()
        
    def decrement_letter(self):
        self.active_word.decrement_letter()
    
    def increment_word(self):
        if self._active_word < len(self.words) - 1:
            self._active_word += 1
    
    def __init__(self):
        super().__init__()
        
        self._active_word = 0
        
        layout = QVBoxLayout()
        self.words = []
        
        for num in range(6):
            new_row = WordleWord()
            if num > 0:
                new_row.setEnabled(False)
            self.words.append(new_row)
            layout.addWidget(new_row)
            
        self.setLayout(layout)
        
    def reset(self):
        for word in self.words:
            word.reset()
        self._active_word = 0

# Subclass QMainWindow to customize your application's main window
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
            if self.puzzle.active_letter.text() == ' ':
                self.puzzle.decrement_letter()
                self.puzzle.active_letter.setText(' ')
            else:
                self.puzzle.active_letter.setText(' ')
        elif e.key() == 16777220: # Enter
            self.cull_dictionary()
            self.puzzle.active_word.setEnabled(False)
            self.puzzle.increment_word()
            self.puzzle.active_word.setEnabled(True)
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
        for letter in self.puzzle.active_word.letters:
            if letter.state == 0:
                self.possibilities = [word for word in self.possibilities if letter.text().lower() not in word]
            elif letter.state == 1:
                self.possibilities = [word for word in self.possibilities if letter.text().lower() in word and word[letter.index] != letter.text().lower()]
            elif letter.state == 2:
                self.possibilities = [word for word in self.possibilities if word[letter.index] == letter.text().lower()]
        self.dictionary.setText('<br>'.join(self.possibilities))

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
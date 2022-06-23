from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from words import words

class WordleLetter(QPushButton):
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, WordleLetter) and not isinstance(__o, str):
            return False
        return str(__o) == str(self)
    
    def __str__(self) -> str:
        return self.text().lower()
    
    def __init__(self, is_game:bool=False):
        super().__init__()
        self.reset()
        if not is_game:
            self.clicked.connect(self.button_clicked)
        self._index = 0
    
    @property
    def index(self) -> int:
        return self._index
    @index.setter
    def index(self, value:int):
        if value > 5:
            self._index = 5
        elif value < 0:
            self._index = 0
        else:
            self._index = value
        
    @property
    def state(self) -> int:
        return self._state
    @state.setter
    def state(self, new_state:int=0):
        if new_state > 3:
            new_state = 3
        elif new_state < 0:
            new_state = 0
        self._state = new_state
        style_color = 'grey' if new_state == 0 else 'yellow' if new_state == 1 else 'green' if new_state == 2 else 'red'
        self.setStyleSheet(f'font-size: 40px; background-color: {style_color}')
        
    def button_clicked(self):
        self.state = self.state + 1 if self.state < 2 else 0
    
    def reset(self):
        self.state = 0
        self.setText(' ')
            
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
            self.active_letter.reset()
        else:
            self.active_letter.reset()
            
    def setEnabled(self, a0: bool) -> None:
        super().setEnabled(a0)
        if self.isEnabled():
            self.active_indicator.setText('X')
        else:
            self.active_indicator.setText('')
            
    def count(self, __o) -> int:
        return str(self).count(str(__o))
    
    def __str__(self) -> str:
        return ''.join([str(x) for x in self.letters]).lower()
    
    def __getitem__(self, item:int) -> str:
        return self.letters[item]
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, WordleWord):
            return False
        return str(__o) == str(self)
    
    def __init__(self, is_game:bool=False):
        super().__init__()
        
        self._active_letter = 0
        
        layout = QHBoxLayout()
        self.letters = []
        
        for num in range(5):
            new_letter = WordleLetter(is_game)
            new_letter.index = num
            self.letters.append(new_letter)
            layout.addWidget(new_letter)
        
        self.active_indicator = QLabel()
        layout.addWidget(self.active_indicator)
            
        self.setLayout(layout)
    
    def reset(self):
        for letter in self.letters:
            letter.reset()
        self._active_letter = 0
        self.setEnabled(False)
        
class WordlePuzzle(QWidget):
    
    @property
    def active_letter(self) -> WordleLetter:
        return self.active_word.active_letter
    
    def increment_letter(self):
        self.active_word.increment_letter()
        
    def decrement_letter(self):
        self.active_word.decrement_letter()
    
    def increment_word(self):
        if self.active_word.index < len(self.words) - 1:
            self.active_word.setEnabled(False)
            self.active_word = self.words[self.active_word.index + 1]
            self.active_word.setEnabled(True)
    
    def __init__(self, is_game:bool=False):
        super().__init__()
        
        self._active_word = 0
        
        layout = QVBoxLayout()
        self.words = []
        
        for num in range(6):
            new_word = WordleWord(is_game)
            new_word.index = num
            if num > 0:
                new_word.setEnabled(False)
            self.words.append(new_word)
            layout.addWidget(new_word)
            
        self.reset()
            
        self.setLayout(layout)
        
    def reset(self):
        for word in self.words:
            word.reset()
            word.setEnabled(False)
        self.active_word = self.words[0]
        self.active_word.setEnabled(True)
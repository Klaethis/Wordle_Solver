from wordle_gui import *
from random import choice
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QMessageBox,
)

class MainWindow(QMainWindow):
    selected_word = ""
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wordle Game")

        layout = QHBoxLayout()
        
        self.puzzle = WordlePuzzle(is_game=True)
        layout.addWidget(self.puzzle)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
        self.new_game()
        
    def keyPressEvent(self, e):
        if e.key() >= 65 and e.key() <= 90: 
            self.puzzle.active_letter.setText(f'{chr(e.key())}')
            current_letter = self.puzzle.active_letter
            for prev_guess in self.puzzle.words[:self.puzzle.active_word.index]:
                if current_letter == prev_guess[current_letter.index]:
                    if prev_guess[current_letter.index].state != 2:
                        current_letter.state = 3
                    else:
                        current_letter.state = 2
                elif prev_guess[current_letter.index].state == 2:
                    current_letter.state = 3
                else:
                    # clues = [x for x in prev_guess if x.state > 0 and x.state < 3]
                    # for clue in clues:
                        # if self.puzzle.active_word.count(str(current_letter)) > clues.count(str(current_letter)) and str(current_letter) in prev_guess:
                        #     current_letter.state = 3
                    in_clues = [x for x in prev_guess if x.state > 0 and x.state < 3]
                    out_clues = [x for x in prev_guess if x.state == 0]
                    if current_letter in out_clues and self.puzzle.active_word.count(str(current_letter)) > in_clues.count(str(current_letter)) and str(current_letter) in prev_guess:
                        current_letter.state = 3
            self.puzzle.increment_letter()
        elif e.key() == 16777219: # Backspace
            if self.puzzle.active_letter != ' ':
                self.puzzle.active_letter.reset()
            else:
                self.puzzle.decrement_letter()
        elif e.key() == 16777220: # Enter
            if self.check_word():
                if all([x.state == 2 for x in self.puzzle.active_word.letters]):
                    dlg = QMessageBox()
                    dlg.setWindowTitle('Success')
                    dlg.setText('You win!')
                    dlg.exec()
                    self.new_game()
                else:
                    self.puzzle.increment_word()
                    self.puzzle.active_letter.setFocus()
        elif e.key() == 16777268:
            self.new_game()
    
    def new_game(self):
        self.puzzle.reset()
        self.puzzle.active_word.setEnabled(True)
        self.puzzle.active_word.setFocus()
        self.selected_word = choice(words)
    
    def check_word(self) -> bool:
        guess:WordleWord = self.puzzle.active_word
        letter:WordleLetter = None
        solution = self.selected_word
        
        if str(guess) not in words:
            return False
        
        
        bad_guess = False
        for letter in guess.letters:
            for prev_guess in self.puzzle.words[:guess.index]:
                if letter.state == 3:
                    bad_guess = True
                elif letter == prev_guess[letter.index] and prev_guess[letter.index].state != 2:
                    letter.state = 3
                    bad_guess = True
                elif letter != prev_guess[letter.index] and prev_guess[letter.index].state == 2:
                    letter.state = 3
                    bad_guess = True
        for prev_guess in self.puzzle.words[:guess.index]:
            clues = [x for x in prev_guess if x.state > 0 and x.state < 3]
            for clue in clues:
                if guess.count(str(clue)) < clues.count(str(clue)):
                    bad_guess = True
        if bad_guess:
            return False
        
        guessed = []
        for letter in guess:
            if letter == solution[letter.index]:
                letter.state = 2
                guessed.append(str(letter))
        
        remaining = [x for x in guess if x.state < 2]
        for letter in remaining:
            if str(letter) in solution and guessed.count(str(letter)) < solution.count(str(letter)):
                guessed.append(str(letter))
                letter.state = 1
        
        return True

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
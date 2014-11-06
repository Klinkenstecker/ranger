from ranger.core.shared import SettingsAware
import ranger
import math

BASE10 = "0123456789"

def baseconvert(number, fromdigits, todigits):
    # make an integer value out of the number
    value = 0
    for digit in str(number):
        value = value * len(fromdigits) + fromdigits.index(digit)
                
    # create the result in base 'len(todigits)'
    if value == 0:
        res = todigits[0]
    else:
        res = ""
        while value > 0:
            digit = value % len(todigits)
            res = todigits[digit] + res
            value = int(value / len(todigits))
                        
    return res


class QuickJump:
    def __init__(self, fm=None):
        self.activated = False
        # the already entered keys 
        self.key_sequence = ""
        # the length of the key sequence needed to determine a line
        self.levels = 0
        if fm is not None:
            self.fm = fm

    def activate(self, newState):
        settings = self.fm.settings
        if self.activated != newState:
            self.activated = newState
            self.fm.ui.browser.main_column.request_redraw()
            self.key_sequence = ""
            self.letter_base = ""
            if len(settings.quick_jump_letters) < 2:
                settings.quick_jump_letters = "fdsartgbvecwxqyiopmnhzulkj"

    def draw_display(self, line, numFiles):
        letter = self.calc_next_letter(line, numFiles)
        return [[letter.capitalize(), ['quick_jump']]]

    def calc_next_letter(self, line, numFiles):
        if not self.activated:
            return ""

        self.letter_base = self.calc_base(numFiles)
        in_letter_base = baseconvert(line, BASE10, self.letter_base)
        # add leadings 'zeros'
        while len(in_letter_base) < self.levels:
            in_letter_base = self.letter_base[0] + in_letter_base
        
        if self.key_sequence is in_letter_base[0:len(self.key_sequence)]:
            return in_letter_base[len(self.key_sequence)]
        return ""

    def calc_base(self, numFiles):
        maxNumLetters = len(self.fm.settings.quick_jump_letters)
        self.levels = int(math.log(numFiles) / math.log(maxNumLetters)) + 1
        numLetters = int(math.ceil(math.pow(numFiles, float(1)/self.levels)))
        return self.fm.settings.quick_jump_letters[0:numLetters] 

    def press(self, key):
        if not (self.activated and chr(key) in self.letter_base):
            return False

        self.key_sequence = self.key_sequence + chr(key)
        self.fm.ui.browser.main_column.request_redraw()

        if len(self.key_sequence) == self.levels:
            line = int(baseconvert(self.key_sequence, self.letter_base, BASE10))
            self.fm.move(to = line + self.fm.ui.browser.main_column.scroll_begin)
            self.key_sequence = ""

        return True

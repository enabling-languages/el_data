import icu as _icu
import sqlite3 as _sqlite3
from functools import partialmethod as _partialmethod
from .data import UCD, UCDString, BINARY_PROPERTIES, BLOCKS
# from .cldr import CLDR
import os.path as _path
try:
  from typing import Self as _Self
except ImportError:
  from typing_extensions import Self as _Self

class LaoUCD(UCD):

    conn = None

    CHARACTERS = _icu.UnicodeSet(r'[\p{Lao}]')
    # CONSONANTS
    # PREVOWELSx
    # VOWELS
    # TONES
    PUNCTUATION = _icu.UnicodeSet(r'[[\p{Lao}]&[\p{P}]]')
    PUNCTUATION_COMMON = _icu.UnicodeSet(r"[\u0021\u0023-\u0026\u0028\u0029\u002B-\u002F\u003C-\u0040\u005B-\u005D\u005F\u007B\u007D\u00A1\u00AB\u00B1\u00BB\u00D7\u00F7\u2018\u2019\u201C\u201D\u2026\u2039\u203A\u20AC]")
    PUNCTUATION_ALL = PUNCTUATION.addAll(PUNCTUATION_COMMON)
    NUMBERS = _icu.UnicodeSet(r'[[\p{Lao}]&[\p{Nd}]]')
    NUMBERS_ALL = _icu.UnicodeSet(r'[[[\p{Lao}]&[\p{Nd}]][0-9]]')


    METADATA = {
        'script': {
            'label': 'Lao',
            'alternative-label': 'Akson Lao',
            'type': 'Abugida',
            'direction': 'left-to-right',
            'iso_15924': 'Laao',
            'iso_15924_numeric': 356,
            'blocks': ['Lao']
        }
    }

    def __init__(self, char):
      BASE_DIR = _path.dirname(_path.abspath(__file__))
      data_db = _path.join(BASE_DIR, "data.db")
      if LaoUCD.conn is None:
         try:
            LaoUCD.conn = _sqlite3.connect(data_db)
            LaoUCD.cursor = LaoUCD.conn.cursor()
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         # else:
         #    print("Connection established")
      self._char = char
      self._name = _icu.Char.charName(self._char)
      self._cp = f'{ord(self._char):04X}'
      self.data = (
            self._char,
            self._cp,
            self._name,
            self.script(),
            self.block(),
            self.general_category_code(),
            self.bidi_class_code(),
            self.combining_class()
      )
      self.entities = (
            self._char,
            self._xchar(),
            self._dchar(),
            self._ochar(),
            self._bchar(),
            self._html_entity(),
            self._dec_ncr(exclude_ascii=False, as_char=False),
            self._hex_ncr(exclude_ascii=False, as_char=False)
        )

    def is_lao_float(self: _Self, laoNumber: str) -> bool:
        pass

    def is_lao_integer(self: _Self, laoNumber: str) -> bool:
        # return 0x0ED0 <= ord(LaoNumber) <= 0x0ED9
        # add grouping separator 
        return laoNumber in self.DIGITS
    

class LaoUCDString(UCDString):
    def __init__(self: _Self, chars: str):
        self._chars = [LaoUCD(char) for char in chars]
        self.data = [c.data for c in self._chars]
        self.entities = [c.entities for c in self._chars]

    def __len__(self: _Self) -> int:
        return len(self._chars)

    def __getitem__(self: _Self, i) -> _Self:
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            return LaoUCDString("".join([
                self.data[index][0] for index in range(start, stop, step)
            ]))
        else:
            return LaoUCDString(self.data[i][0])

    def to_string(self: _Self) -> str:
        """Convert EthiopicUCD String object to a string.

        Returns:
            str: _description_
        """
        return "".join(self.characters())


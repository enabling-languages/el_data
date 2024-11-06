import icu as _icu
import sqlite3 as _sqlite3
from functools import partialmethod as _partialmethod
from rich.console import Console as _Console
from rich.table import Table as _Table, box as _box
from .data import UCD, UCDString, BINARY_PROPERTIES, BLOCKS
import os.path as _path

class Unikemet(UCD):

    conn = None

    METADATA = {

    }

    def __init__(self, char):
      BASE_DIR = _path.dirname(_path.abspath(__file__))
      data_db = _path.join(BASE_DIR, "data.db")
      if Unikemet.conn is None:
         try:
            Unikemet.conn = _sqlite3.connect(data_db)
            Unikemet.cursor = Unikemet.conn.cursor()
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         else:
            print("Connection established")
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

    def _get_unikemet_properties(self, property):
        query = f"SELECT {property} FROM unikemet WHERE codepoint = '{self._cp}'"
        return Unikemet.cursor.execute(query).fetchone()[0]

    def _get_all_unikemet_properties(self):
        query = "SELECT * FROM unikemet WHERE codepoint = '{self._cp}'"
        return Unikemet.cursor.execute(query).fetchall()



class UnikemetString(UCDString):
    def __init__(self, chars):
        self._chars = [Unikemet(char) for char in chars]
        self.data = [c.data for c in self._chars]
        self.entities = [c.entities for c in self._chars]


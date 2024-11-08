import icu as _icu
import sqlite3 as _sqlite3
from functools import partialmethod as _partialmethod
from rich.console import Console as _Console
from rich.table import Table as _Table, box as _box
from .data import UCD, UCDString, BINARY_PROPERTIES, BLOCKS
# from .cldr import CLDR
import os.path as _path

class EthiopicUCD(UCD):

    conn = None

    CHARACTERS = _icu.UnicodeSet(r'[\p{Ethiopic}]')
    SYLLABLES = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{L}]]')
    PUNCTUATION = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{P}]]')
    NUMERALS = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{N}]]')
    MARKS = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{Mn}]]')
    ZAIMA_QIRTS = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{So}]]')

    METADATA = {
        'script': {
            'label': 'Ethiopic',
            'alternative-label': 'Geʽez',
            'type': 'Abugida',
            'direction': 'left-to-right',
            'iso_15924': 'Ethi',
            'iso_15924_numeric': 430,
            'blocks': ['Ethiopic', 'Ethiopic Supplement', 'Ethiopic Extended', 'Ethiopic Extended-A', 'Ethiopic Extended-B']
        },
        'locales': {
            'CLDR': ['am', 'am_ET', 'gez', 'gez_ER', 'gez_ET', 'ti', 'ti_ER', 'ti_ET'],
            'SLDR': ['am', 'am_ET', 'aiw_Ethi', 'gez', 'gez_ER', 'gez_ET', 'ti', 'ti_ER', 'ti_ET'],
            'glibc': []
        },
        'families':  {
            'ሀ': {'label':'ሆይ', 'romanised': 'Hoy'},
            'ለ': {'label':'ላዊ', 'romanised': 'Lawi'},
            'ሐ': {'label':'ሐውት', 'romanised': 'ሐውት'},
            'መ': {'label':'ማይ', 'romanised': 'ማይ'},
            'ሠ': {'label':'ሠውት', 'romanised': 'ሠውት'},
            'ረ': {'label':'ርእስ', 'romanised': 'ርእስ'},
            'ሰ': {'label':'ሳት', 'romanised': 'ሳት'},
            'ሸ': {'label':'ሻ-ሳት', 'romanised': 'ሻ-ሳት'},
            'ቀ': {'label':'ቃፍ', 'romanised': 'ቃፍ'},
            'በ': {'label':'ቤት', 'romanised': 'ቤት'},
            'ቨ': {'label':'ቬ-ቤት', 'romanised': 'ቬ-ቤት'},
            'ተ': {'label':'ታው', 'romanised': 'ታው'},
            'ቸ': {'label':'ቻ-ታው', 'romanised': 'ቻ-ታው'},
            'ኀ': {'label':'ኀርም', 'romanised': 'ኀርም'},
            'ነ': {'label':'ነሐስ', 'romanised': 'ነሐስ'},
            'ኘ': {'label':'ኛ-ነሐስ', 'romanised': 'ኛ-ነሐስ'},
            'አ': {'label':'አልፍ', 'romanised': 'አልፍ'},
            'ከ': {'label':'ካፍ', 'romanised': 'ካፍ'},
            'ኸ': {'label':'ኻ-ካፍ', 'romanised': 'ኻ-ካፍ'},
            'ወ': {'label':'ወዌ', 'romanised': 'ወዌ'},
            'ዐ': {'label':'ዐይን', 'romanised': 'ዐይን'},
            'ዘ': {'label':'ዘይ', 'romanised': 'ዘይ'},
            'ዠ': {'label':'ዠ-ዘይ', 'romanised': 'ዠ-ዘይ'},
            'የ': {'label':'የመነ', 'romanised': 'የመነ'},
            'ደ': {'label':'ድንት', 'romanised': 'ድንት'},
            'ጀ': {'label':'ጅ-ድንት', 'romanised': 'ጅ-ድንት'},
            'ገ': {'label':'ገምል', 'romanised': 'ገምል'},
            'ጠ': {'label':'ጠይት', 'romanised': 'ጠይት'},
            'ጨ': {'label':'ጨ-ጠይት', 'romanised': 'ጨ-ጠይት'},
            'ጰ': {'label':'ጰይት', 'romanised': 'ጰይት'},
            'ጸ': {'label':'ጸደይ', 'romanised': 'ጸደይ'},
            'ፀ': {'label':'ፀጳ', 'romanised': 'ፀጳ'},
            'ፈ': {'label':'አፍ', 'romanised': 'አፍ'},
            'ፐ': {'label':'ፕሳ', 'romanised': 'ፕሳ'}
        },
        'orders': {
            'ግዕዝ': {'enum': 1, 'romanised': 'Geʽez'},
            'ካዕብ': {'enum': 2, 'romanised': 'Kaib'},
            'ሣልስ': {'enum': 3, 'romanised': 'Salis'},
            'ራዕብ': {'enum': 4, 'romanised': 'Rabi'},
            'ኃምስ': {'enum': 5, 'romanised': 'Hamis'},
            'ሳድስ': {'enum': 6, 'romanised': 'Sadis'},
            'ሳብዕ': {'enum': 7, 'romanised': 'Sabi'},
            'ሳምን': {'enum': 8, 'romanised': 'Samin'},
            'ዘመደ-ግዕዝ': {'enum': 9, 'romanised': 'Zemede-Geʽez'},
            'ዘመደ-ካዕብ': {'enum': 10, 'romanised': 'Zemede-Kaʽeb'},
            'ዘመደ-ሣልስ': {'enum': 11, 'romanised': 'Zemede-Salis'},
            'ዘመደ-ራብዕ': {'enum': 12, 'romanised': 'Zemede-Rabi'},
            'ዘመደ-ኃምስ': {'enum': 13, 'romanised': 'Zemede-Hamis'},
            'ዘመደ-ባዕድ': {'enum': 14, 'romanised': 'Zemede-Baʽed'}
        }
    }

    def __init__(self, char):
      BASE_DIR = _path.dirname(_path.abspath(__file__))
      data_db = _path.join(BASE_DIR, "data.db")
      if EthiopicUCD.conn is None:
         try:
            EthiopicUCD.conn = _sqlite3.connect(data_db)
            EthiopicUCD.cursor = EthiopicUCD.conn.cursor()
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         # else:
         #    print("Connection established")
      self._char = char
      self._name = _icu.Char.charName(self._char)
      self._cp = f'{ord(self._char):04X}'
      self._family, self._order = self._order_family()
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

    def _order_family(self):
        if self._char in self.SYLLABLES:
            query = f"SELECT ቤተሰብ, ቤት FROM ethiopic WHERE ሆሄ = '{self._char}'"
            return EthiopicUCD.cursor.execute(query).fetchall()[0]
        return (None, None)

    def is_ethiopic_numeral(self, ethNumber):
        # return 0x1369 <= ord(ethNumber) <= 0x137C
        return ethNumber in self.NUMERALS

    def get_family(self, mode: str = 'default'):
        if mode.lower() == 'label':
            return self.METADATA['families'][self._family]['label']
        elif mode.lower() in ['romanised', 'romanized']:
            return self.METADATA['families'][self._family]['romanised']
        return self._family

    def get_family_members(self):
        query = f"SELECT ሆሄ FROM ethiopic WHERE ቤተሰብ = '{self._family}'"
        result = EthiopicUCD.cursor.execute(query).fetchall()
        return [t[0] for t in result]

    def get_family_pattern(self):
        uset = self.get_family_uset()
        return uset.toPattern()

    def get_family_uset(self):
        pattern = rf'[{" ".join(self.get_family_members())}]'
        return _icu.UnicodeSet(pattern)

    def get_order(self, mode: str = 'default') -> str | int:
        if mode.lower() == 'enum':
            return self.METADATA['orders'][self._order]['enum']
        elif mode.lower() in ['romanised', 'romanized']:
            return self.METADATA['orders'][self._order]['romanised']
        return self._order

    def get_order_members(self):
        query = f"SELECT ሆሄ FROM ethiopic WHERE ቤት = '{self._order}'"
        result = EthiopicUCD.cursor.execute(query).fetchall()
        return [t[0] for t in result]

    def get_order_pattern(self):
        uset = self.get_order_uset()
        return uset.toPattern()

    def get_order_uset(self):
        pattern = rf'[{" ".join(self.get_order_members())}]'
        return _icu.UnicodeSet(pattern)

    def convert_order(self, order:str) -> str:
        query = f'SELECT ሆሄ FROM ethiopic WHERE ቤተሰብ = "{self._family}" and ቤት = "{order}";'
        return EthiopicUCD.cursor.execute(query).fetchone()[0]

class EthiopicUCDString(UCDString):
    def __init__(self, chars):
        self._chars = [EthiopicUCD(char) for char in chars]
        self.data = [c.data for c in self._chars]
        self.entities = [c.entities for c in self._chars]

    def __len__(self):
        return len(self._chars)

    def __getitem__(self, i):
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            return EthiopicUCDString("".join([
                self.data[index][0] for index in range(start, stop, step)
            ]))
        else:
            # return EthiopicUCD(self.data[i][0])
            return EthiopicUCDString(self.data[i][0])

    def get_family(self) -> list[str]:
            return [c.get_family() for c in self._chars]

    def get_order(self) -> list[str]:
        return [c.get_order() for c in self._chars]

    def is_ethiopic_numeral(self, ethNumber: str) -> bool:
        if len(ethNumber) == 1:
            # return 0x1369 <= ord(ethNumber) <= 0x137C
            return ethNumber in EthiopicUCD.NUMERALS
        return set(ethNumber).issubset(EthiopicUCD.NUMERALS)

    def convert_order(self, order, idx: int|None = None, as_string: bool = False):
        if idx == None:
            results = [c.convert_order(order) for c in self._chars]
        else:
            results = [c.convert_order(order) if i == idx else c.character() for i, c in enumerate(self._chars)]
        if as_string:
            return ''.join(results)
        return results

    def to_string(self):
        return "".join(self.characters())

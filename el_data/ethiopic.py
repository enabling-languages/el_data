import icu as _icu
import sqlite3 as _sqlite3
from functools import partialmethod as _partialmethod
from rich.console import Console as _Console
from rich.table import Table as _Table, box as _box
from .data import UCD, UCDString, BINARY_PROPERTIES, BLOCKS
# from .cldr import CLDR
import os.path as _path
try:
  from typing import Self as _Self
except ImportError:
  from typing_extensions import Self as _Self

homophonic_syllable_equivalences = {
    'am': {
        "ሀ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ሐ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ሃ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ሓ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ኀ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ኃ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ኻ": 'ሀ,ሃ,ሐ,ሓ,ኀ,ኃ,ኻ',
        "ሁ": 'ሁ,ሑ,ኁ,ኹ',
        "ሑ": 'ሁ,ሑ,ኁ,ኹ',
        "ኁ": 'ሁ,ሑ,ኁ,ኹ',
        "ኹ": 'ሁ,ሑ,ኁ,ኹ',
        "ሂ": "ሂ,ሒ,ኂ,ኺ",
        "ሒ": "ሂ,ሒ,ኂ,ኺ",
        "ኂ": "ሂ,ሒ,ኂ,ኺ",
        "ኺ": "ሂ,ሒ,ኂ,ኺ",
        "ሄ": "ሄ,ሔ,ኄ,ኼ",
        "ሔ": "ሄ,ሔ,ኄ,ኼ",
        "ኄ": "ሄ,ሔ,ኄ,ኼ",
        "ኼ": "ሄ,ሔ,ኄ,ኼ",
        "ህ": "ህ,ሕ,ኅ,ኽ",
        "ሕ": "ህ,ሕ,ኅ,ኽ",
        "ኅ": "ህ,ሕ,ኅ,ኽ",
        "ኽ": "ህ,ሕ,ኅ,ኽ",
        "ሆ": "ሆ,ሖ,ኆ,ኈ,ኾ,ዀ",
        "ሖ": "ሆ,ሖ,ኆ,ኈ,ኾ,ዀ",
        "ኆ": "ሆ,ሖ,ኆ,ኈ,ኾ,ዀ",
        "ኈ": "ሆ,ሖ,ኆ,ኈ,ኾ,ዀ",
        "ኾ": "ሆ,ሖ,ኆ,ኈ,ኾ,ዀ",
        "ዀ": "ሆ,ሖ,ኆ,ኈ,ኾ,ዀ",
        "ሗ": "ሗ,ኋ,ዃ",
        "ኋ": "ሗ,ኋ,ዃ",
        "ዃ": "ሗ,ኋ,ዃ",
        "ሰ": "ሰ,ሠ",
        "ሠ": "ሰ,ሠ",
        "ሱ": "ሱ,ሡ",
        "ሡ": "ሱ,ሡ",
        "ሲ": "ሲ,ሢ",
        "ሢ": "ሲ,ሢ",
        "ሳ": "ሳ,ሣ",
        "ሣ": "ሳ,ሣ",
        "ሴ": "ሴ,ሤ",
        "ሤ": "ሴ,ሤ",
        "ስ": "ስ,ሥ",
        "ሥ": "ስ,ሥ",
        "ሶ": "ሶ,ሦ",
        "ሦ": "ሶ,ሦ",
        "ሷ": "ሷ,ሧ",
        "ሧ": "ሷ,ሧ",
        "ቁ": "ቁ,ቍ",
        "ቍ": "ቁ,ቍ",
        "ቆ": "ቆ,ቈ",
        "ቈ": "ቆ,ቈ",
        "አ": "አ,ኣ,ዐ,ዓ",
        "ኣ": "አ,ኣ,ዐ,ዓ",
        "ዐ": "አ,ኣ,ዐ,ዓ",
        "ዓ": "አ,ኣ,ዐ,ዓ",
        "ኡ": "ኡ,ዑ",
        "ዑ": "ኡ,ዑ",
        "ኢ": "ኢ,ዒ",
        "ዒ": "ኢ,ዒ",
        "ኤ": "ኤ,ዔ",
        "ዔ": "ኤ,ዔ",
        "እ": "እ,ዕ",
        "ዕ": "እ,ዕ",
        "ኦ": "ኦ,ዖ",
        "ዖ": "ኦ,ዖ",
        "ኮ": "ኮ,ኰ",
        "ኰ": "ኮ,ኰ",
        "ጎ": "ጎ,ጐ",
        "ጐ": "ጎ,ጐ",
        "ጸ": "ጸ,ፀ",
        "ፀ": "ጸ,ፀ",
        "ጹ": "ጹ,ፁ",
        "ፁ": "ጹ,ፁ",
        "ጺ": "ጺ,ፂ",
        "ፂ": "ጺ,ፂ",
        "ጻ": "ጻ,ፃ",
        "ፃ": "ጻ,ፃ",
        "ጼ": "ጼ,ፄ",
        "ፄ": "ጼ,ፄ",
        "ጽ": "ጽ,ፅ",
        "ፅ": "ጽ,ፅ",
        "ጾ": "ጾ,ፆ",
        "ፆ": "ጾ,ፆ"
        },
    "ti": {
        "ሀ": "ሀ,ሃ,ኀ,ኃ",
        "ሃ": "ሀ,ሃ,ኀ,ኃ",
        "ኀ": "ሀ,ሃ,ኀ,ኃ",
        "ኃ": "ሀ,ሃ,ኀ,ኃ",
        "ሁ": "ሁ,ኁ",
        "ኁ": "ሁ,ኁ",
        "ሂ": "ሂ,ኂ",
        "ኂ": "ሂ,ኂ",
        "ሄ": "ሄ,ኄ",
        "ኄ": "ሄ,ኄ",
        "ህ": "ህ,ኅ",
        "ኅ": "ህ,ኅ",
        "ሆ": "ሆ,ኆ,ኈ",
        "ኆ": "ሆ,ኆ,ኈ",
        "ኈ": "ሆ,ኆ,ኈ",
        "ሐ": "ሐ,ሓ",
        "ሓ": "ሐ,ሓ",
        "ሰ": "ሰ,ሠ",
        "ሠ": "ሰ,ሠ",
        "ሱ": "ሱ,ሡ",
        "ሡ": "ሱ,ሡ",
        "ሲ": "ሲ,ሢ",
        "ሢ": "ሲ,ሢ",
        "ሳ": "ሳ,ሣ",
        "ሣ": "ሳ,ሣ",
        "ሴ": "ሴ,ሤ",
        "ሤ": "ሴ,ሤ",
        "ስ": "ስ,ሥ",
        "ሥ": "ስ,ሥ",
        "ሶ": "ሶ,ሦ",
        "ሦ": "ሶ,ሦ",
        "ሷ": "ሷ,ሧ",
        "ሧ": "ሷ,ሧ",
        "ቁ": "ቁ,ቍ",
        "ቍ": "ቁ,ቍ",
        "ቆ": "ቆ,ቈ",
        "ቈ": "ቆ,ቈ",
        "አ": "አ,ኣ",
        "ኣ": "አ,ኣ",
        "ኮ": "ኮ,ኰ",
        "ኰ": "ኮ,ኰ",
        "ዐ": "ዐ,ዓ",
        "ዓ": "ዐ,ዓ",
        "ጎ": "ጎ,ጐ",
        "ጐ": "ጎ,ጐ",
        "ጸ": "ጸ,ፀ",
        "ፀ": "ጸ,ፀ",
        "ጹ": "ጹ,ፁ",
        "ፁ": "ጹ,ፁ",
        "ጺ": "ጺ,ፂ",
        "ፂ": "ጺ,ፂ",
        "ጻ": "ጻ,ፃ",
        "ፃ": "ጻ,ፃ",
        "ጼ": "ጼ,ፄ",
        "ፄ": "ጼ,ፄ",
        "ጽ": "ጽ,ፅ",
        "ፅ": "ጽ,ፅ",
        "ጾ": "ጾ,ፆ",
        "ፆ": "ጾ,ፆ"
    },
    "gez": {
        "ሀ": "ሀ,ሃ",
        "ሃ": "ሀ,ሃ",
        "ሐ": "ሐ,ሓ",
        "ሓ": "ሐ,ሓ",
        "ኀ": "ኀ,ኃ",
        "ኃ": "ኀ,ኃ",
        "አ": "አ,ኣ",
        "ኣ": "አ,ኣ",
        "ኮ": "ኮ,ኰ",
        "ኰ": "ኮ,ኰ",
        "ዐ": "ዐ,ዓ",
        "ዓ": "ዐ,ዓ",
        "ጎ": "ጎ,ጐ",
        "ጐ": "ጎ,ጐ"
    }
}

homophonic_family_equivalences = {
    "am": {
        "ሀ": 'ሀ-ሆ,ሐ-ሗ,ኀ-ኆ,ኈ-ኍ,ኸ-ኾ,ዀ-ዅ',
        "ሐ": 'ሀ-ሆ,ሐ-ሗ,ኀ-ኆ,ኈ-ኍ,ኸ-ኾ,ዀ-ዅ',
        "ኀ": 'ሀ-ሆ,ሐ-ሗ,ኀ-ኆ,ኈ-ኍ,ኸ-ኾ,ዀ-ዅ',
        "ኸ": 'ሀ-ሆ,ሐ-ሗ,ኀ-ኆ,ኈ-ኍ,ኸ-ኾ,ዀ-ዅ',
        "ሰ": "ሰ-ሷ,ሠ-ሧ",
        "ሠ": "ሰ-ሷ,ሠ-ሧ",
        "አ": "አ-ኧ,ዐ-ዖ",
        "ዐ": "አ-ኧ,ዐ-ዖ",
        "ጸ": "ጸ-ጿ,ፀ-ፆ",
        "ፀ": "ጸ-ጿ,ፀ-ፆ"
    },
    "ti": {
        "ሀ": "ሀ-ሆ,ኀ-ኆ,ኈ-ኍ",
        "ኀ": "ሀ-ሆ,ኀ-ኆ,ኈ-ኍ",
        "ሰ": "ሰ-ሷ,ሠ-ሧ",
        "ሠ": "ሰ-ሷ,ሠ-ሧ",
        "ጸ": "ጸ-ጿ,ፀ-ፆ",
        "ፀ": "ጸ-ጿ,ፀ-ፆ"
    }
}

class EthiopicUCD(UCD):

    conn = None

    CHARACTERS = _icu.UnicodeSet(r'[\p{Ethiopic}]')
    SYLLABLES = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{L}]]')
    PUNCTUATION = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{P}]]')
    PUNCTUATION_COMMON = _icu.UnicodeSet(r"[\u0021\u0023-\u0026\u0028\u0029\u002B-\u002F\u003C-\u0040\u005B-\u005D\u005F\u007B\u007D\u00A1\u00AB\u00B1\u00BB\u00D7\u00F7\u2018\u2019\u201C\u201D\u2026\u2039\u203A\u20AC]")
    PUNCTUATION_ALL = PUNCTUATION.addAll(PUNCTUATION_COMMON)
    WORD_SEPARATORS = _icu.UnicodeSet(r'[[\p{Zs}}][፡።]]')
    NUMBERS = _icu.UnicodeSet(r'[[\p{Ethiopic}]&[\p{N}]]')
    NUMBERS_ALL = _icu.UnicodeSet(r'[[[\p{Ethiopic}]&[\p{N}]][0-9]]')
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

    def _order_family(self: _Self):
        if self._char in self.SYLLABLES:
            query = f"SELECT ቤተሰብ, ቤት FROM ethiopic WHERE ሆሄ = '{self._char}'"
            return EthiopicUCD.cursor.execute(query).fetchall()[0]
        return (None, None)

    def is_ethiopic_numeral(self: _Self, ethNumber: str) -> bool:
        # return 0x1369 <= ord(ethNumber) <= 0x137C
        return ethNumber in self.NUMERALS

    def get_family(self: _Self, mode: str = 'default') -> str:
        if mode.lower() == 'label':
            return self.METADATA['families'][self._family]['label']
        elif mode.lower() in ['romanised', 'romanized']:
            return self.METADATA['families'][self._family]['romanised']
        return self._family

    def get_family_members(self: _Self) -> list[str]:
        query = f"SELECT ሆሄ FROM ethiopic WHERE ቤተሰብ = '{self._family}'"
        result = EthiopicUCD.cursor.execute(query).fetchall()
        return [t[0] for t in result]

    def get_family_pattern(self: _Self) -> str:
        uset = self.get_family_uset()
        return uset.toPattern()

    def get_family_uset(self: _Self) -> _icu.UnicodeSet:
        pattern = rf'[{" ".join(self.get_family_members())}]'
        return _icu.UnicodeSet(pattern)

    def get_order(self: _Self, mode: str = 'default') -> str | int:
        if mode.lower() == 'enum':
            return self.METADATA['orders'][self._order]['enum']
        elif mode.lower() in ['romanised', 'romanized']:
            return self.METADATA['orders'][self._order]['romanised']
        return self._order

    def get_order_members(self: _Self) -> list[str]:
        query = f"SELECT ሆሄ FROM ethiopic WHERE ቤት = '{self._order}'"
        result = EthiopicUCD.cursor.execute(query).fetchall()
        return [t[0] for t in result]

    def get_order_pattern(self: _Self) -> str:
        uset = self.get_order_uset()
        return uset.toPattern()

    def get_order_uset(self: _Self) -> _icu.UnicodeSet:
        pattern = rf'[{" ".join(self.get_order_members())}]'
        return _icu.UnicodeSet(pattern)

    def convert_order(self: _Self, order:str) -> str:
        query = f'SELECT ሆሄ FROM ethiopic WHERE ቤተሰብ = "{self._family}" and ቤት = "{order}";'
        return EthiopicUCD.cursor.execute(query).fetchone()[0]

class EthiopicUCDString(UCDString):
    def __init__(self: _Self, chars: str):
        self._chars = [EthiopicUCD(char) for char in chars]
        self.data = [c.data for c in self._chars]
        self.entities = [c.entities for c in self._chars]

    def __len__(self: _Self) -> int:
        return len(self._chars)

    def __getitem__(self: _Self, i) -> _Self:
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            return EthiopicUCDString("".join([
                self.data[index][0] for index in range(start, stop, step)
            ]))
        else:
            # return EthiopicUCD(self.data[i][0])
            return EthiopicUCDString(self.data[i][0])

    def get_family(self: _Self, mode: str = 'default') -> list[str]:
        """_summary_

        Args:
            self (_Self): _description_
            mode (str, optional): _description_. Defaults to 'default'.

        Returns:
            list[str]: _description_
        """
        return [c.get_family(mode = mode) for c in self._chars]

    def get_order(self: _Self, mode: str = 'default') -> list[str]:
        """_summary_

        Args:
            self (_Self): _description_
            mode (str, optional): _description_. Defaults to 'default'.

        Returns:
            list[str]: _description_
        """
        return [c.get_order(mode = mode) for c in self._chars]

    def is_ethiopic_numeral(self: _Self, ethNumber: str) -> bool:
        """_summary_

        Args:
            ethNumber (str): _description_

        Returns:
            bool: _description_
        """
        if len(ethNumber) == 1:
            # return 0x1369 <= ord(ethNumber) <= 0x137C
            return ethNumber in EthiopicUCD.NUMERALS
        return set(ethNumber).issubset(EthiopicUCD.NUMERALS)

    def convert_order(self: _Self, order, idx: int|None = None, as_string: bool = False) -> list[str] | str:
        """Convert each syllable, or syllable at index, to the corresponding syllable of the specified order.

        Args:
            order (_type_): Order that syllable(s) will be converted to.
            idx (int | None, optional): Index of syllable to be converted. If not specified, all characters are converted. Defaults to None.  Alternatively use slices.
            as_string (bool, optional): Retrun characters as a string if True, else return as a list of characters. Defaults to False.

        Returns:
            list[str] | str: A list or syllbales or string.
        """
        if idx is None:
            results = [c.convert_order(order) for c in self._chars]
        else:
            results = [c.convert_order(order) if i == idx else c.character() for i, c in enumerate(self._chars)]
        if as_string:
            return ''.join(results)
        return results

    def to_string(self: _Self) -> str:
        """Convert EthiopicUCD String object to a string.

        Returns:
            str: _description_
        """
        return "".join(self.characters())

# def get_ethiopic_order(char: str) -> str:
#     if len(char) != 1:
#         raise ValueError("Input must be a single character")
#     return EthiopicUCD(char).get_order_members()

def ethiopic_order(order: int|str) -> list[str]:
    """Create a list of all characters in a given Ethiopic order.

    Used to get a list of characters in a given Ethiopic order. Useful for
    creating named lists for regular expressions patterns with the `regex` module.

    Examples:
        ethiopic_order(1)
        ethiopic_order('1')
        ethiopic_order('1,7')
        ethiopic_order('1-3')
        ethiopic_order('1-3,7')

    Args:
        order (int|str): Ethiopic order number or range of orders.

    Raises:
        ValueError: Input must be an integer between 1 and 14

    Returns:
        list[str]: List of characters in the specified orders.
    """
    if isinstance(order, int) and not 0 < order < 15:
        raise ValueError('Input must be an integer between 1 and 14')
    order_examples = {
        1: 'መ', 2 : 'ሙ', 3 : 'ሚ', 4 : 'ማ', 5 : 'ሜ',
        6 : 'ም', 7 : 'ሞ', 8 : 'ⶁ', 9 : 'ᎀ', 10 : 'ᎁ', 
        11 : 'ሟ', 12 : 'ᎂ', 13 : 'ᎃ', 14 : 'ፙ'
    }
    if isinstance(order, int):
        return EthiopicUCD(order_examples[order]).get_order_members()
    else:
        orders = expand_range(order)
        pattern = []
        for o in orders:
            pattern = pattern + EthiopicUCD(order_examples[o]).get_order_members()
        return pattern

def ethiopic_family(family: str) -> list[str]:
    """Create a list of all characters in a given Ethiopic family.

    Used to get a list of characters in a given Ethiopic family. Useful for
    creating named lists for regular expressions patterns with the `regex` module.

    Examples:
        ethiopic_family('ለ')
        ethiopic_family('ለ,መ')
        ethiopic_family('ለ-መ')
        ethiopic_family('ጸ,ለ-መ')

    Args:
        family (str): Ethiopic family.

    Returns:
        list[str]: List of characters in the specified family.
    """    
    # if len(family) != 1:
    #     raise ValueError("Input must be a single character")
    pattern = []
    if len(family) == 1:
        pattern = EthiopicUCD(family).get_family_members()
    else:
        families = expand_range(family)
        for f in families:
            pattern = pattern + EthiopicUCD(f).get_family_members()
    return pattern

def filter_orders(families: str, orders: int|str) -> list[str]:
    """Create a list of all characters in given Ethiopic families and orders. 
   
    Used to get a list of characters in a given Ethiopic family and order. Useful
    for creating named lists for regular expressions patterns with the `regex` module.
    I.e. syllables of specified orders restricted to specified families).

    Examples:
        filter_orders('መ-ቀ', '4,6') ➡︎ ['ር', 'ሻ', 'ሣ', 'ማ', 'ራ', 'ቅ', 'ሥ', 'ስ', 'ቃ', 'ም', 'ሳ', 'ሽ']

    Args:
        family (str): Ethiopic family.
        order (int|str): Ethiopic order number or range of orders.

    Returns:
        list[str]: List of characters in the specified family and order.
    """
    family = ethiopic_family(families)
    order = ethiopic_order(orders)
    return list(set(family) & set(order))

# def expand_range(char_range: str) -> list[str]:
#     """Expand Ethiopic order and family range into a list of orders or families.
#
#     Used to expand Ethiopic order and family ranges into a list of characters. Useful for
#
#     e.g. 
#         expand_range('1,3-6') -> ['1', '3', '4', '5', '6']
#         expand_range('ለ-መ') -> ['ለ', 'ሐ', 'መ']
#         expand_range('ጸለ-መ') -> ['ለ', 'ሐ', 'መ', 'ጸ']
#
#     Args:
#         char_range (str): Ethiopic character range.
#
#     Returns:
#         list[str]: List of characters in the specified range.
#     """
#     char_range = char_range.replace(',', '')
#     chars = _icu.UnicodeSet(rf'[{char_range}]') 
#     if all([x.isdigit() for x in chars]):
#         return list(chars)
#     family_ids = EthiopicUCD.METADATA['families'].keys()
#     return [x for x in list(chars) if x in family_ids]

def expand_range(char_range: str) -> list[str, int]:
    """Expand Ethiopic order and family range into a list of orders or families.

    Used to expand Ethiopic order and family ranges into a list of characters. Useful for

    e.g. 
        expand_range('1,3-6') -> ['1', '3', '4', '5', '6']
        expand_range('ለ-መ') -> ['ለ', 'ሐ', 'መ']
        expand_range('ጸ,ለ-መ') -> ['ለ', 'ሐ', 'መ', 'ጸ']

    Args:
        char_range (str): Ethiopic order or family range.

    Returns:
        list[str, int]: List of characters in the specified range. Either as a list of order numbers or family names.
    """
    family_ids = EthiopicUCD.METADATA['families'].keys()
    if "," in char_range:
        char_range = char_range.split(',')
        char_range = [x.strip() for x in char_range]
    else:
        char_range = [char_range]
    results = []
    for item in char_range:
        if "-" in item:
            if any([x.isdigit() for x in item]):
                start, end = item.split('-')
                sub_range = list(range(int(start), int(end)+1))
                results = results + sub_range
            else:
               sub_range = list(_icu.UnicodeSet(rf'[{item}]'))
               results = results + sub_range
        else:
            if item.isdigit():
                results.append(int(item)) 
            else: 
                if len(item) == 1:
                    results.append(item)
                else:
                    results = results + list(_icu.UnicodeSet(rf'[{item}]'))
    if not any([isinstance(x, int) for x in results]):
        results = [x for x in results if x in family_ids]
    return results

def homophonic_equivalences(char: str, family: bool = False, language: str = 'am') -> list[str]:
    # Returns a list of language specific homophonic equivalences for the given character or family.
    if family and language not in ['am', 'ti']:
        raise ValueError('Language must be "am" or "ti"')
    if not family and language not in ['am', 'gez', 'ti']:
        raise ValueError('Language must be "am", "gez" or "ti"')
    homophones = []
    if family:
        homophones = expand_range(homophonic_family_equivalences.get(language).get(char, []))
    else:
        homophones = expand_range(homophonic_syllable_equivalences.get(language, {}).get(char, []))
    return homophones

def homophonic_normalisation(text: str, language: str = 'am') -> str:
    if language not in ['am', 'gez', 'ti']:
        raise ValueError('Language must be "am", "gez" or "ti"')
    chars = [*text]
    chars = [homophonic_syllable_equivalences.get(language).get(char, char)[0] for char in chars]
    return ''.join(chars)

def homophonic_compare(text1: str, text2: str, language: str = 'am') -> bool:
    if language not in ['am', 'gez', 'ti']:
        raise ValueError('Language must be "am", "gez" or "ti"')
    return homophonic_normalisation(text1, language) == homophonic_normalisation(text2, language)

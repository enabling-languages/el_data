# import pandas as _pd
# import numpy as _np
import sqlite3 as _sqlite3
import icu as _icu
import os.path as _path

class Encodings():
    conn = None
    _collator = _icu.Collator.createInstance(_icu.Locale('und'))
    _collator.setAttribute(_icu.UCollAttribute.NUMERIC_COLLATION, _icu.UCollAttributeValue.ON)

    def __init__(self, codepoint='0x00', encoding='iso-8859-1'):
        BASE_DIR = _path.dirname(_path.abspath(__file__))
        data_db = _path.join(BASE_DIR, "data.db")
        if Encodings.conn is None:
            try:
                Encodings.conn = _sqlite3.connect(data_db)
                Encodings.cursor = Encodings.conn.cursor()
                print("Connection established")
            except Exception as error:
                print("Error: Connection not established {}".format(error))
        else:
            print("Existing connection")
        self._codepoint = self._normalise_codepoint(codepoint)
        self._encoding = encoding
        self._available_8bit = self._available_encodings()
        # self._python_encodings = _py_available_encodings()

    def _available_encodings(self):
        columns = Encodings.cursor.execute("PRAGMA table_info('encodings')").fetchall()
        return [column[1] for column in columns if column[1] != 'codepoint']

    def _normalise_codepoint(self, codepoint=''):
        if isinstance(codepoint, int):
            codepoint = f'0x{codepoint:02X}'
        else:
            codepoint = f'0x{int(codepoint,16):02X}'
        return codepoint

    def _sorted(self, lst):
        return sorted(lst, key = Encodings._collator.getSortKey)

    def codepoint_data(self, codepoint=''):
        if codepoint:
            self._codepoint = self._normalise_codepoint(codepoint)
        query = f'SELECT * FROM encodings WHERE codepoint = "{self._codepoint}";'
        Encodings.cursor.execute(query)
        record = Encodings.cursor.fetchone()
        data_keys = ['codepoint'] + self._available_8bit
        return {data_keys[i]: record[i] for i in range(len(data_keys))}

    def encoding_data(self, enc=''):
        if enc:
            self._encoding = enc.lower()
        query = f'SELECT "{self._encoding}" FROM encodings;'
        Encodings.cursor.execute(query)
        records = Encodings.cursor.fetchall()
        results = [*enumerate([r[0] for r in records])]
        return {f'0x{i[0]:02X}': i[1] for i in results}

    def match_character(self, character, codepoint='', ):
        if codepoint:
            self._codepoint = self._normalise_codepoint(codepoint)
        character_codepoint = f'0x{ord(character):04X}'
        record = self.codepoint_data(self._codepoint)
        data = list({k for k, v in record.items() if v == character_codepoint})
        return self._sorted(data)



def get_surrogate_pair(char, as_int=False, as_char=False):
    char = chr(char) if isinstance(char, int) else char
    pair = char.encode('utf-16-be', 'surrogatepass').hex(' ', 2).upper().split()
    if as_char:
        return [chr(int(i, 16)) for i in pair]
    return [int(lone, 16) for lone in pair] if as_int else pair

# print(get_surrogate_pair('𐀀'))
# print(get_surrogate_pair('𐀀', True))
# print(get_surrogate_pair('\U00010000'))
# print(get_surrogate_pair('\U00010000', True))
# print(get_surrogate_pair(0x10000))
# print(get_surrogate_pair(0x10000, True))
# print(get_surrogate_pair('𐀀', as_char=True))

def explore_surrogates(surrogate_char, emoji_only=False):
    surrogate_char = chr(surrogate_char) if isinstance(surrogate_char, int) else surrogate_char
    if not 0xD800 <= ord(surrogate_char) <= 0xDFFF:
        return None
    non_bmp = _icu.UnicodeSet(r'[[\p{Emoji}]-[\u0000-\uFFFF]]') if emoji_only else _icu.UnicodeSet(r'[[[\p{Any}]-[\u0000-\uFFFF]]-[\p{Unassigned}]]')
    surrogate_byte = surrogate_char.encode('utf-16-be', 'surrogatepass')
    if 0xD800 <= ord(surrogate_char) <= 0xDBFF:
        return [e for e in list(non_bmp) if e.encode('utf-16-be').startswith(surrogate_byte)]
    return [e for e in list(non_bmp) if e.encode('utf-16-be').endswith(surrogate_byte)]

# len(explore_surrogates('\ud83d'))
# len(explore_surrogates('\ud83d', True))
# len(explore_surrogates(0xd83d))
# len(explore_surrogates(0xd83d, True))
# len(explore_surrogates('\udc00'))
# len(explore_surrogates('\udc00', True))
# len(explore_surrogates(0xdc00))
# len(explore_surrogates(0xdc00, True))


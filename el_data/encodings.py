# import pandas as _pd
# import numpy as _np
import sqlite3 as _sqlite3
import icu as _icu

class Encodings():
    conn = None
    _collator = _icu.Collator.createInstance(_icu.Locale('und'))
    _collator.setAttribute(_icu.UCollAttribute.NUMERIC_COLLATION, _icu.UCollAttributeValue.ON)

    def __init__(self, codepoint='0x00', encoding='iso-8859-1'):
        data_db = "data.db"
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

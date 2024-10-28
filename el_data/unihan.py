import icu as _icu
import sqlite3 as _sqlite3
from .data import UCD, UCDString
from functools import partialmethod as _partialmethod
# import json as _json
from rich.console import Console as _Console
import os.path as _path

class Unihan(UCD):

   conn = None

   def __init__(self, char):
      BASE_DIR = _path.dirname(_path.abspath(__file__))
      data_db = _path.join(BASE_DIR, "data.db")
      if Unihan.conn is None:
         try:
            Unihan.conn = _sqlite3.connect(data_db)
            Unihan.cursor = Unihan.conn.cursor()
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
      self._properties = ['id', 'ucn', 'char', 'kCangjie', 'kCantonese', 'kDefinition', 'kHanYu', 'kIRGHanyuDaZidian', 'kIRGKangXi', 'kIRG_GSource', 'kIRG_JSource', 'kIRG_TSource', 'kJapanese', 'kKangXi', 'kMandarin', 'kMojiJoho', 'kMorohashi', 'kRSUnicode', 'kSemanticVariant', 'kTotalStrokes', 'kCihaiT', 'kHanyuPinyin', 'kIRG_KSource', 'kSBGY', 'kJIS0213', 'kNelson', 'kRSAdobe_Japan1_6', 'kStrange', 'kCowles', 'kMatthews', 'kOtherNumeric', 'kPhonetic', 'kSpoofingVariant', 'kGSR', 'kIRG_KPSource', 'kIRG_VSource', 'kFenn', 'kFennIndex', 'kKarlgren', 'kVietnameseNumeric', 'kIRG_HSource', 'kUnihanCore2020', 'kTraditionalVariant', 'kFourCornerCode', 'kSMSZD2003Index', 'kTGH', 'kTGHZ2013', 'kXHC1983', 'kMeyerWempe', 'kVietnamese', 'kSimplifiedVariant', 'kSMSZD2003Readings', 'kHangul', 'kKoreanName', 'kSpecializedSemanticVariant', 'kEACC', 'kLau', 'kCheungBauer', 'kCheungBauerIndex', 'kIRG_USource', 'kIICore', 'kTang', 'kZhuangNumeric', 'kZVariant', 'kTaiwanTelegraph', 'kIRG_MSource', 'kJapaneseKun', 'kJapaneseOn', 'kJa', 'kIRG_UKSource', 'kAlternateTotalStrokes', 'kBigFive', 'kCCCII', 'kCNS1986', 'kCNS1992', 'kDaeJaweon', 'kFrequency', 'kGB0', 'kGB1', 'kGradeLevel', 'kHDZRadBreak', 'kHKGlyph', 'kHanyuPinlu', 'kIRGDaeJaweon', 'kJis0', 'kJoyoKanji', 'kKorean', 'kKoreanEducationHanja', 'kMainlandTelegraph', 'kPrimaryNumeric', 'kXerox', 'kGB5', 'kJis1', 'kPseudoGB1', 'kGB3', 'kGB8', 'kJinmeiyoKanji', 'kIBMJapan', 'kAccountingNumeric', 'kGB7', 'kCompatibilityVariant', 'kIRG_SSource']

   def _all_unihan(self):
      query = f"SELECT * FROM unihan WHERE char = '{self._char}'"
      results = Unihan.cursor.execute(query).fetchall()
      return results

   def _get_uh_property(self, property):
      query = f"SELECT {property} FROM unihan WHERE char = '{self._char}'"
      result = Unihan.cursor.execute(query).fetchone()
      # return _json.loads(result[0])
      if len(result[0]) == 1:
         data = result[0][0]
         return data.replace('"', '')
      return result[0]

   def char(self):
         return self._char

   kCangjie = _partialmethod(_get_uh_property, property = 'kCangjie')
   kCantonese = _partialmethod(_get_uh_property, property = 'kCantonese')
   kDefinition = _partialmethod(_get_uh_property, property = 'kDefinition')
   kHanYu = _partialmethod(_get_uh_property, property = 'kHanYu')
   kIRGHanyuDaZidian = _partialmethod(_get_uh_property, property = 'kIRGHanyuDaZidian')
   kIRGKangXi = _partialmethod(_get_uh_property, property = 'kIRGKangXi')
   kIRG_GSource = _partialmethod(_get_uh_property, property = 'kIRG_GSource')
   kIRG_JSource = _partialmethod(_get_uh_property, property = 'kIRG_JSource')
   kIRG_TSource = _partialmethod(_get_uh_property, property = 'kIRG_TSource')
   kJapanese = _partialmethod(_get_uh_property, property = 'kJapanese')
   kKangXi = _partialmethod(_get_uh_property, property = 'kKangXi')
   kMandarin = _partialmethod(_get_uh_property, property = 'kMandarin')
   kMojiJoho = _partialmethod(_get_uh_property, property = 'kMojiJoho')
   kMorohashi = _partialmethod(_get_uh_property, property = 'kMorohashi')
   kRSUnicode = _partialmethod(_get_uh_property, property = 'kRSUnicode')
   kSemanticVariant = _partialmethod(_get_uh_property, property = 'kSemanticVariant')
   kTotalStrokes = _partialmethod(_get_uh_property, property = 'kTotalStrokes')
   kCihaiT = _partialmethod(_get_uh_property, property = 'kCihaiT')
   kHanyuPinyin = _partialmethod(_get_uh_property, property = 'kHanyuPinyin')
   kIRG_KSource = _partialmethod(_get_uh_property, property = 'kIRG_KSource')
   kSBGY = _partialmethod(_get_uh_property, property = 'kSBGY')
   kJIS0213 = _partialmethod(_get_uh_property, property = 'kJIS0213')
   kNelson = _partialmethod(_get_uh_property, property = 'kNelson')
   kRSAdobe_Japan1_6 = _partialmethod(_get_uh_property, property = 'kRSAdobe_Japan1_6')
   kStrange = _partialmethod(_get_uh_property, property = 'kStrange')
   kCowles = _partialmethod(_get_uh_property, property = 'kCowles')
   kMatthews = _partialmethod(_get_uh_property, property = 'kMatthews')
   kOtherNumeric = _partialmethod(_get_uh_property, property = 'kOtherNumeric')
   kPhonetic = _partialmethod(_get_uh_property, property = 'kPhonetic')
   kSpoofingVariant = _partialmethod(_get_uh_property, property = 'kSpoofingVariant')
   kGSR = _partialmethod(_get_uh_property, property = 'kGSR')
   kIRG_KPSource = _partialmethod(_get_uh_property, property = 'kIRG_KPSource')
   kIRG_VSource = _partialmethod(_get_uh_property, property = 'kIRG_VSource')
   kFenn = _partialmethod(_get_uh_property, property = 'kFenn')
   kFennIndex = _partialmethod(_get_uh_property, property = 'kFennIndex')
   kKarlgren = _partialmethod(_get_uh_property, property = 'kKarlgren')
   kVietnameseNumeric = _partialmethod(_get_uh_property, property = 'kVietnameseNumeric')
   kIRG_HSource = _partialmethod(_get_uh_property, property = 'kIRG_HSource')
   kUnihanCore2020 = _partialmethod(_get_uh_property, property = 'kUnihanCore2020')
   kTraditionalVariant = _partialmethod(_get_uh_property, property = 'kTraditionalVariant')
   kFourCornerCode = _partialmethod(_get_uh_property, property = 'kFourCornerCode')
   kSMSZD2003Index = _partialmethod(_get_uh_property, property = 'kSMSZD2003Index')
   kTGH = _partialmethod(_get_uh_property, property = 'kTGH')
   kTGHZ2013 = _partialmethod(_get_uh_property, property = 'kTGHZ2013')
   kXHC1983 = _partialmethod(_get_uh_property, property = 'kXHC1983')
   kMeyerWempe = _partialmethod(_get_uh_property, property = 'kMeyerWempe')
   kVietnamese = _partialmethod(_get_uh_property, property = 'kVietnamese')
   kSimplifiedVariant = _partialmethod(_get_uh_property, property = 'kSimplifiedVariant')
   kSMSZD2003Readings = _partialmethod(_get_uh_property, property = 'kSMSZD2003Readings')
   kHangul = _partialmethod(_get_uh_property, property = 'kHangul')
   kKoreanName = _partialmethod(_get_uh_property, property = 'kKoreanName')
   kSpecializedSemanticVariant = _partialmethod(_get_uh_property, property = 'kSpecializedSemanticVariant')
   kEACC = _partialmethod(_get_uh_property, property = 'kEACC')
   kLau = _partialmethod(_get_uh_property, property = 'kLau')
   kCheungBauer = _partialmethod(_get_uh_property, property = 'kCheungBauer')
   kCheungBauerIndex = _partialmethod(_get_uh_property, property = 'kCheungBauerIndex')
   kIRG_USource = _partialmethod(_get_uh_property, property = 'kIRG_USource')
   kIICore = _partialmethod(_get_uh_property, property = 'kIICore')
   kTang = _partialmethod(_get_uh_property, property = 'kTang')
   kZhuangNumeric = _partialmethod(_get_uh_property, property = 'kZhuangNumeric')
   kZVariant = _partialmethod(_get_uh_property, property = 'kZVariant')
   kTaiwanTelegraph = _partialmethod(_get_uh_property, property = 'kTaiwanTelegraph')
   kIRG_MSource = _partialmethod(_get_uh_property, property = 'kIRG_MSource')
   kJapaneseKun = _partialmethod(_get_uh_property, property = 'kJapaneseKun')
   kJapaneseOn = _partialmethod(_get_uh_property, property = 'kJapaneseOn')
   kJa = _partialmethod(_get_uh_property, property = 'kJa')
   kIRG_UKSource = _partialmethod(_get_uh_property, property = 'kIRG_UKSource')
   kAlternateTotalStrokes = _partialmethod(_get_uh_property, property = 'kAlternateTotalStrokes')
   kBigFive = _partialmethod(_get_uh_property, property = 'kBigFive')
   kCCCII = _partialmethod(_get_uh_property, property = 'kCCCII')
   kCNS1986 = _partialmethod(_get_uh_property, property = 'kCNS1986')
   kCNS1992 = _partialmethod(_get_uh_property, property = 'kCNS1992')
   kDaeJaweon = _partialmethod(_get_uh_property, property = 'kDaeJaweon')
   kFrequency = _partialmethod(_get_uh_property, property = 'kFrequency')
   kGB0 = _partialmethod(_get_uh_property, property = 'kGB0')
   kGB1 = _partialmethod(_get_uh_property, property = 'kGB1')
   kGradeLevel = _partialmethod(_get_uh_property, property = 'kGradeLevel')
   kHDZRadBreak = _partialmethod(_get_uh_property, property = 'kHDZRadBreak')
   kHKGlyph = _partialmethod(_get_uh_property, property = 'kHKGlyph')
   kHanyuPinlu = _partialmethod(_get_uh_property, property = 'kHanyuPinlu')
   kIRGDaeJaweon = _partialmethod(_get_uh_property, property = 'kIRGDaeJaweon')
   kJis0 = _partialmethod(_get_uh_property, property = 'kJis0')
   kJoyoKanji = _partialmethod(_get_uh_property, property = 'kJoyoKanji')
   kKorean = _partialmethod(_get_uh_property, property = 'kKorean')
   kKoreanEducationHanja = _partialmethod(_get_uh_property, property = 'kKoreanEducationHanja')
   kMainlandTelegraph = _partialmethod(_get_uh_property, property = 'kMainlandTelegraph')
   kPrimaryNumeric = _partialmethod(_get_uh_property, property = 'kPrimaryNumeric')
   kXerox = _partialmethod(_get_uh_property, property = 'kXerox')
   kGB5 = _partialmethod(_get_uh_property, property = 'kGB5')
   kJis1 = _partialmethod(_get_uh_property, property = 'kJis1')
   kPseudoGB1 = _partialmethod(_get_uh_property, property = 'kPseudoGB1')
   kGB3 = _partialmethod(_get_uh_property, property = 'kGB3')
   kGB8 = _partialmethod(_get_uh_property, property = 'kGB8')
   kJinmeiyoKanji = _partialmethod(_get_uh_property, property = 'kJinmeiyoKanji')
   kIBMJapan = _partialmethod(_get_uh_property, property = 'kIBMJapan')

   # kAccountingNumeric
   #  	The value of the ideograph when used as an accounting numeral to prevent fraud in Chinese and derivative numeric systems. A numeral such as 十 (ten) is easily transformed into 千 (thousand) by adding a single stroke, so monetary documents often use an accounting form of the numeral, such as 拾 (ten), instead of the more common—and simpler—form. Ideographs with this property will have a single, well-defined value, which a native reader can reasonably be expected to understand.
   #
   kAccountingNumeric = _partialmethod(_get_uh_property, property = 'kAccountingNumeric')
   kGB7 = _partialmethod(_get_uh_property, property = 'kGB7')
   kCompatibilityVariant = _partialmethod(_get_uh_property, property = 'kCompatibilityVariant')
   kIRG_SSource = _partialmethod(_get_uh_property, property = 'kIRG_SSource')
   # ucn = _partialmethod(_get_uh_property, property = 'ucn')
   def ucn(self):
      result =  self._get_uh_property('ucn')
      return result

   def _meta(self, property, category = None):
      console = _Console()
      property_meta = {
         'kAccountingNumeric': {'Property': 'kAccountingNumeric',
            'Status': 'Informative',
            'Category': 'Numeric Values',
            'Introduced': '3.2',
            'Delimiter': 'space',
            'Syntax': r'[0-9]+',
            'Description': 'The value of the ideograph when used as an accounting numeral to prevent fraud in Chinese and derivative numeric systems. A numeral such as 十 (ten) is easily transformed into 千 (thousand) by adding a single stroke, so monetary documents often use an accounting form of the numeral, such as 拾 (ten), instead of the more common—and simpler—form. Ideographs with this property will have a single, well-defined value, which a native reader can reasonably be expected to understand.\n\nThe three Chinese numeric-value properties should have no overlap; that is, ideographs with a kAccountingNumeric value should not have a kOtherNumeric or kPrimaryNumeric value as well.'
         },
         'kAlternateTotalStrokes': {
            'Property': 'kAlternateTotalStrokes',
            'Status': 'Provisional',
            'Category': 'Dictionary-like Data',
            'Introduced': '15.0',
            'Delimiter': 'space',
            'Syntax': r'(\d+:[BHJKMPSUV]+)|-',
            'Description': 'The total number of strokes in the ideograph (including the radical). Each value consists either of a decimal value followed by an IRG source specifier as defined in Section 3.10, or of the special value “-” (U+002D - HYPHEN-MINUS).\n\nThe IRG source specifier indicates the IRG sources for which a particular value is preferred. The source identifiers “G” and “T” are not used in this property, as these IRG sources are fully covered by the kTotalStrokes property./n/nThe stroke count value is the one for the glyph as shown in the code charts./n/nMultiple stroke counts are listed in increasing numeric order. Stroke counts may not be repeated./n/nIf there is a single kTotalStrokes value for a ideograph, the IRG sources sharing this stroke count should not be explicitly listed. If all IRG sources share this stroke count, then the value of “-” is used. The kAlternateTotalStrokes value for U+4E95 井 is therefore “-” instead of “4:HJKPV.”/n/nThe kAlternateTotalStrokes “-” value may not be used where there are two kTotalStrokes values for an ideograph. Thus, the kAlternateTotalStrokes value for U+9AA8 骨 is “10:HJKPV.”/n/nFor IRG sources which do not include a source reference, the kAlternateTotalStrokes property should not have a corresponding value./n/nUnlike the kTotalStrokes property, the data in this property is not to be taken as exhaustive. Where it is defined for an ideograph, however, it includes explicit or implicit values for all IRG sources containing the ideograph.'
         },
         'kBigFive': {
            'Property': 'kBigFive',
            'Status': 'Provisional',
            'Category': 'Other Mappings',
            'Introduced': '2.0',
            'Delimiter': 'N/A',
            'Syntax': '[0-9A-F]{4}\'?',
            'Description': 'The Big Five mapping for this ideograph in hexadecimal; note that this does not cover any of the Big Five extensions in common use, including the ETEN extensions. An apostrophe (U+0027 \' APOSTROPHE) at the end of the property value indicates an alternate Big Five mapping for two ideographs that map differently in CNS 11643, specifically U+5284 劄 (Big Five) versus U+7B9A 箚 (CNS 11643) and U+5F5D 彝 (Big Five) versus U+5F5E 彞 (CNS 11643).'
         },
         'kCangjie': {
            'Property': 'kCangjie',
            'Status': 'Provisional',
            'Category': 'Dictionary-like Data',
            'Introduced': '3.1.1',
            'Delimiter': 'N/A',
            'Syntax': '[A-Z]+',
            'Description': 'The cangjie input code for the ideograph. This incorporates data from the file cangjie-table.b5 by Christian Wittern.'
         },
         'kCantonese': {
            'Property': 'kCantonese',
            'Status': 'Provisional',
            'Category': 'Readings',
            'Introduced': '2.0',
            'Delimiter': 'space',
            'Syntax': '[a-z]{1,6}[1-6]',
            'Description': 'The most customary jyutping (Cantonese) reading for this ideograph.\n\nThis property is targeted specifically for use by CLDR collation and transliteration. As such, it is subject to considerations that help keep jyutping-based Han collation (and its tailorings) and transliteration reasonably stable. The values may not in all cases track the preferred reading in some dictionaries.\n\nAmong the sources used for Cantonese data are the following:\n\nCasey, G. Hugh, S.J. Ten Thousand Characters: An Analytic Dictionary. Hong Kong: Kelley and Walsh, 1980. (kPhonetic)\n\nCheung Kwan-hin, and Robert S. Bauer, The Representation of Cantonese with Chinese Characters, Journal of Chinese Linguistics Monograph Series Number 18, 2002. ISSN 0091-3723 (kCheungBauer, kCheungBauerIndex)\n\nCowles, Roy T. A Pocket Dictionary of Cantonese. Hong Kong: University Press, 1999. ISBN 962-209-122-9 (kCowles)\n\nJiu Bingcoi 饒秉才, ed. Guangzhou Yin Zidian / Gwongzau Jam Zidin 廣州音字典 (Guangzhou Pronouncing Character Dictionary). Hong Kong: Joint Publishing (H.K.) Co., Ltd, 1989. ISBN 962-04-0389-4\n\nLangwen Chuji Zhongwen Cidian / Longman Cokap Zungman Cidin 朗文初級中文詞典 (Longman’s Elementary Chinese Dictionary). Hong Kong: Longman, 2001. ISBN 962-00-5148-3\n\nLau, Sidney. A Practical Cantonese-English Dictionary. Hong Kong: Government Printer, 1977 (kLau).\n\nMeyer, Bernard F., and Theodore F. Wempe. Student’s Cantonese-English Dictionary. Maryknoll, New York: Catholic Foreign Mission Society of America, 1947 (kMeyerWempe).\n\nWong Gongsang 黃港生, ed. Xin Shangwu Cidian / San Soengmou Cidin 商務新詞典 (New Commercial Press Dictionary). Hong Kong: 商務印書館(香港)有限公司 (Commercial Press [Hong Kong], Ltd.), 1991. ISBN 962-07-0133-X\n\nWong Gongsang 黃港生, ed. Xin Shangwu Zidian / San Soengmou Zidin 新商務字典 (New Commercial Press Character Dictionary). Hong Kong: 商務印書館(香港)有限公司 (Commercial Press [Hong Kong], Ltd.), 2003. ISBN 962-07-0140-2 (kSMSZD2003Index)\n\nZhonghua Xin Zidian / Zungwaa San Zidin 中華新字典 (New Chung Hwa Character Dictionary). Hong Kong: 中華書局 (Chung Hwa Book Co.), 2003. ISBN 962-231-001-X'
         }
      }
      data = property_meta.get(property)
      if category and data:
         console.print(data[category])
      elif data:
         console.print(data)
      else:
         console.print('[red bold]Property metadata unavailable.')
      return None

class UnihanString(UCDString):
    def __init__(self, chars):
        self._chars = [Unihan(char) for char in chars]
        self.data = [c.data for c in self._chars]

    def __str__(self):
        return "".join(self.characters())

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(chars={self.characters()})"

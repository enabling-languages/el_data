import icu as _icu
from functools import partialmethod as _partialmethod
import html as _html
from rich.console import Console as _Console
from rich.table import Table as _Table, box as _box
from hexdump import hexdump as _hexdump
from typing import Self as _Self

#
# Refer to
#   * https://unicode-org.github.io/icu/userguide/strings/properties.html
#   * https://util.unicode.org/UnicodeJsps/properties.html
#   * https://util.unicode.org/UnicodeJsps/properties.jsp

BINARY_PROPERTIES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36, 42, 43, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]
ICU_VERSION = float('.'.join(_icu.ICU_VERSION.split('.')[0:2]))
# Unicode 16.0 blocks
BLOCKS = {'basic_latin': {'start': '0000', 'end': '007F'}, 'latin-1_supplement': {'start': '0080', 'end': '00FF'}, 'latin_extended-a': {'start': '0100', 'end': '017F'}, 'latin_extended-b': {'start': '0180', 'end': '024F'}, 'ipa_extensions': {'start': '0250', 'end': '02AF'}, 'spacing_modifier_letters': {'start': '02B0', 'end': '02FF'}, 'combining_diacritical_marks': {'start': '0300', 'end': '036F'}, 'greek_and_coptic': {'start': '0370', 'end': '03FF'}, 'cyrillic': {'start': '0400', 'end': '04FF'}, 'cyrillic_supplement': {'start': '0500', 'end': '052F'}, 'armenian': {'start': '0530', 'end': '058F'}, 'hebrew': {'start': '0590', 'end': '05FF'}, 'arabic': {'start': '0600', 'end': '06FF'}, 'syriac': {'start': '0700', 'end': '074F'}, 'arabic_supplement': {'start': '0750', 'end': '077F'}, 'thaana': {'start': '0780', 'end': '07BF'}, 'nko': {'start': '07C0', 'end': '07FF'}, 'samaritan': {'start': '0800', 'end': '083F'}, 'mandaic': {'start': '0840', 'end': '085F'}, 'syriac_supplement': {'start': '0860', 'end': '086F'}, 'arabic_extended-b': {'start': '0870', 'end': '089F'}, 'arabic_extended-a': {'start': '08A0', 'end': '08FF'}, 'devanagari': {'start': '0900', 'end': '097F'}, 'bengali': {'start': '0980', 'end': '09FF'}, 'gurmukhi': {'start': '0A00', 'end': '0A7F'}, 'gujarati': {'start': '0A80', 'end': '0AFF'}, 'oriya': {'start': '0B00', 'end': '0B7F'}, 'tamil': {'start': '0B80', 'end': '0BFF'}, 'telugu': {'start': '0C00', 'end': '0C7F'}, 'kannada': {'start': '0C80', 'end': '0CFF'}, 'malayalam': {'start': '0D00', 'end': '0D7F'}, 'sinhala': {'start': '0D80', 'end': '0DFF'}, 'thai': {'start': '0E00', 'end': '0E7F'}, 'lao': {'start': '0E80', 'end': '0EFF'}, 'tibetan': {'start': '0F00', 'end': '0FFF'}, 'myanmar': {'start': '1000', 'end': '109F'}, 'georgian': {'start': '10A0', 'end': '10FF'}, 'hangul_jamo': {'start': '1100', 'end': '11FF'}, 'ethiopic': {'start': '1200', 'end': '137F'}, 'ethiopic_supplement': {'start': '1380', 'end': '139F'}, 'cherokee': {'start': '13A0', 'end': '13FF'}, 'unified_canadian_aboriginal_syllabics': {'start': '1400', 'end': '167F'}, 'ogham': {'start': '1680', 'end': '169F'}, 'runic': {'start': '16A0', 'end': '16FF'}, 'tagalog': {'start': '1700', 'end': '171F'}, 'hanunoo': {'start': '1720', 'end': '173F'}, 'buhid': {'start': '1740', 'end': '175F'}, 'tagbanwa': {'start': '1760', 'end': '177F'}, 'khmer': {'start': '1780', 'end': '17FF'}, 'mongolian': {'start': '1800', 'end': '18AF'}, 'unified_canadian_aboriginal_syllabics_extended': {'start': '18B0', 'end': '18FF'}, 'limbu': {'start': '1900', 'end': '194F'}, 'tai_le': {'start': '1950', 'end': '197F'}, 'new_tai_lue': {'start': '1980', 'end': '19DF'}, 'khmer_symbols': {'start': '19E0', 'end': '19FF'}, 'buginese': {'start': '1A00', 'end': '1A1F'}, 'tai_tham': {'start': '1A20', 'end': '1AAF'}, 'combining_diacritical_marks_extended': {'start': '1AB0', 'end': '1AFF'}, 'balinese': {'start': '1B00', 'end': '1B7F'}, 'sundanese': {'start': '1B80', 'end': '1BBF'}, 'batak': {'start': '1BC0', 'end': '1BFF'}, 'lepcha': {'start': '1C00', 'end': '1C4F'}, 'ol_chiki': {'start': '1C50', 'end': '1C7F'}, 'cyrillic_extended-c': {'start': '1C80', 'end': '1C8F'}, 'georgian_extended': {'start': '1C90', 'end': '1CBF'}, 'sundanese_supplement': {'start': '1CC0', 'end': '1CCF'}, 'vedic_extensions': {'start': '1CD0', 'end': '1CFF'}, 'phonetic_extensions': {'start': '1D00', 'end': '1D7F'}, 'phonetic_extensions_supplement': {'start': '1D80', 'end': '1DBF'}, 'combining_diacritical_marks_supplement': {'start': '1DC0', 'end': '1DFF'}, 'latin_extended_additional': {'start': '1E00', 'end': '1EFF'}, 'greek_extended': {'start': '1F00', 'end': '1FFF'}, 'general_punctuation': {'start': '2000', 'end': '206F'}, 'superscripts_and_subscripts': {'start': '2070', 'end': '209F'}, 'currency_symbols': {'start': '20A0', 'end': '20CF'}, 'combining_diacritical_marks_for_symbols': {'start': '20D0', 'end': '20FF'}, 'letterlike_symbols': {'start': '2100', 'end': '214F'}, 'number_forms': {'start': '2150', 'end': '218F'}, 'arrows': {'start': '2190', 'end': '21FF'}, 'mathematical_operators': {'start': '2200', 'end': '22FF'}, 'miscellaneous_technical': {'start': '2300', 'end': '23FF'}, 'control_pictures': {'start': '2400', 'end': '243F'}, 'optical_character_recognition': {'start': '2440', 'end': '245F'}, 'enclosed_alphanumerics': {'start': '2460', 'end': '24FF'}, 'box_drawing': {'start': '2500', 'end': '257F'}, 'block_elements': {'start': '2580', 'end': '259F'}, 'geometric_shapes': {'start': '25A0', 'end': '25FF'}, 'miscellaneous_symbols': {'start': '2600', 'end': '26FF'}, 'dingbats': {'start': '2700', 'end': '27BF'}, 'miscellaneous_mathematical_symbols-a': {'start': '27C0', 'end': '27EF'}, 'supplemental_arrows-a': {'start': '27F0', 'end': '27FF'}, 'braille_patterns': {'start': '2800', 'end': '28FF'}, 'supplemental_arrows-b': {'start': '2900', 'end': '297F'}, 'miscellaneous_mathematical_symbols-b': {'start': '2980', 'end': '29FF'}, 'supplemental_mathematical_operators': {'start': '2A00', 'end': '2AFF'}, 'miscellaneous_symbols_and_arrows': {'start': '2B00', 'end': '2BFF'}, 'glagolitic': {'start': '2C00', 'end': '2C5F'}, 'latin_extended-c': {'start': '2C60', 'end': '2C7F'}, 'coptic': {'start': '2C80', 'end': '2CFF'}, 'georgian_supplement': {'start': '2D00', 'end': '2D2F'}, 'tifinagh': {'start': '2D30', 'end': '2D7F'}, 'ethiopic_extended': {'start': '2D80', 'end': '2DDF'}, 'cyrillic_extended-a': {'start': '2DE0', 'end': '2DFF'}, 'supplemental_punctuation': {'start': '2E00', 'end': '2E7F'}, 'cjk_radicals_supplement': {'start': '2E80', 'end': '2EFF'}, 'kangxi_radicals': {'start': '2F00', 'end': '2FDF'}, 'ideographic_description_characters': {'start': '2FF0', 'end': '2FFF'}, 'cjk_symbols_and_punctuation': {'start': '3000', 'end': '303F'}, 'hiragana': {'start': '3040', 'end': '309F'}, 'katakana': {'start': '30A0', 'end': '30FF'}, 'bopomofo': {'start': '3100', 'end': '312F'}, 'hangul_compatibility_jamo': {'start': '3130', 'end': '318F'}, 'kanbun': {'start': '3190', 'end': '319F'}, 'bopomofo_extended': {'start': '31A0', 'end': '31BF'}, 'cjk_strokes': {'start': '31C0', 'end': '31EF'}, 'katakana_phonetic_extensions': {'start': '31F0', 'end': '31FF'}, 'enclosed_cjk_letters_and_months': {'start': '3200', 'end': '32FF'}, 'cjk_compatibility': {'start': '3300', 'end': '33FF'}, 'cjk_unified_ideographs_extension_a': {'start': '3400', 'end': '4DBF'}, 'yijing_hexagram_symbols': {'start': '4DC0', 'end': '4DFF'}, 'cjk_unified_ideographs': {'start': '4E00', 'end': '9FFF'}, 'yi_syllables': {'start': 'A000', 'end': 'A48F'}, 'yi_radicals': {'start': 'A490', 'end': 'A4CF'}, 'lisu': {'start': 'A4D0', 'end': 'A4FF'}, 'vai': {'start': 'A500', 'end': 'A63F'}, 'cyrillic_extended-b': {'start': 'A640', 'end': 'A69F'}, 'bamum': {'start': 'A6A0', 'end': 'A6FF'}, 'modifier_tone_letters': {'start': 'A700', 'end': 'A71F'}, 'latin_extended-d': {'start': 'A720', 'end': 'A7FF'}, 'syloti_nagri': {'start': 'A800', 'end': 'A82F'}, 'common_indic_number_forms': {'start': 'A830', 'end': 'A83F'}, 'phags-pa': {'start': 'A840', 'end': 'A87F'}, 'saurashtra': {'start': 'A880', 'end': 'A8DF'}, 'devanagari_extended': {'start': 'A8E0', 'end': 'A8FF'}, 'kayah_li': {'start': 'A900', 'end': 'A92F'}, 'rejang': {'start': 'A930', 'end': 'A95F'}, 'hangul_jamo_extended-a': {'start': 'A960', 'end': 'A97F'}, 'javanese': {'start': 'A980', 'end': 'A9DF'}, 'myanmar_extended-b': {'start': 'A9E0', 'end': 'A9FF'}, 'cham': {'start': 'AA00', 'end': 'AA5F'}, 'myanmar_extended-a': {'start': 'AA60', 'end': 'AA7F'}, 'tai_viet': {'start': 'AA80', 'end': 'AADF'}, 'meetei_mayek_extensions': {'start': 'AAE0', 'end': 'AAFF'}, 'ethiopic_extended-a': {'start': 'AB00', 'end': 'AB2F'}, 'latin_extended-e': {'start': 'AB30', 'end': 'AB6F'}, 'cherokee_supplement': {'start': 'AB70', 'end': 'ABBF'}, 'meetei_mayek': {'start': 'ABC0', 'end': 'ABFF'}, 'hangul_syllables': {'start': 'AC00', 'end': 'D7AF'}, 'hangul_jamo_extended-b': {'start': 'D7B0', 'end': 'D7FF'}, 'high_surrogates': {'start': 'D800', 'end': 'DB7F'}, 'high_private_use_surrogates': {'start': 'DB80', 'end': 'DBFF'}, 'low_surrogates': {'start': 'DC00', 'end': 'DFFF'}, 'private_use_area': {'start': 'E000', 'end': 'F8FF'}, 'cjk_compatibility_ideographs': {'start': 'F900', 'end': 'FAFF'}, 'alphabetic_presentation_forms': {'start': 'FB00', 'end': 'FB4F'}, 'arabic_presentation_forms-a': {'start': 'FB50', 'end': 'FDFF'}, 'variation_selectors': {'start': 'FE00', 'end': 'FE0F'}, 'vertical_forms': {'start': 'FE10', 'end': 'FE1F'}, 'combining_half_marks': {'start': 'FE20', 'end': 'FE2F'}, 'cjk_compatibility_forms': {'start': 'FE30', 'end': 'FE4F'}, 'small_form_variants': {'start': 'FE50', 'end': 'FE6F'}, 'arabic_presentation_forms-b': {'start': 'FE70', 'end': 'FEFF'}, 'halfwidth_and_fullwidth_forms': {'start': 'FF00', 'end': 'FFEF'}, 'specials': {'start': 'FFF0', 'end': 'FFFF'}, 'linear_b_syllabary': {'start': '10000', 'end': '1007F'}, 'linear_b_ideograms': {'start': '10080', 'end': '100FF'}, 'aegean_numbers': {'start': '10100', 'end': '1013F'}, 'ancient_greek_numbers': {'start': '10140', 'end': '1018F'}, 'ancient_symbols': {'start': '10190', 'end': '101CF'}, 'phaistos_disc': {'start': '101D0', 'end': '101FF'}, 'lycian': {'start': '10280', 'end': '1029F'}, 'carian': {'start': '102A0', 'end': '102DF'}, 'coptic_epact_numbers': {'start': '102E0', 'end': '102FF'}, 'old_italic': {'start': '10300', 'end': '1032F'}, 'gothic': {'start': '10330', 'end': '1034F'}, 'old_permic': {'start': '10350', 'end': '1037F'}, 'ugaritic': {'start': '10380', 'end': '1039F'}, 'old_persian': {'start': '103A0', 'end': '103DF'}, 'deseret': {'start': '10400', 'end': '1044F'}, 'shavian': {'start': '10450', 'end': '1047F'}, 'osmanya': {'start': '10480', 'end': '104AF'}, 'osage': {'start': '104B0', 'end': '104FF'}, 'elbasan': {'start': '10500', 'end': '1052F'}, 'caucasian_albanian': {'start': '10530', 'end': '1056F'}, 'vithkuqi': {'start': '10570', 'end': '105BF'}, 'todhri': {'start': '105C0', 'end': '105FF'}, 'linear_a': {'start': '10600', 'end': '1077F'}, 'latin_extended-f': {'start': '10780', 'end': '107BF'}, 'cypriot_syllabary': {'start': '10800', 'end': '1083F'}, 'imperial_aramaic': {'start': '10840', 'end': '1085F'}, 'palmyrene': {'start': '10860', 'end': '1087F'}, 'nabataean': {'start': '10880', 'end': '108AF'}, 'hatran': {'start': '108E0', 'end': '108FF'}, 'phoenician': {'start': '10900', 'end': '1091F'}, 'lydian': {'start': '10920', 'end': '1093F'}, 'meroitic_hieroglyphs': {'start': '10980', 'end': '1099F'}, 'meroitic_cursive': {'start': '109A0', 'end': '109FF'}, 'kharoshthi': {'start': '10A00', 'end': '10A5F'}, 'old_south_arabian': {'start': '10A60', 'end': '10A7F'}, 'old_north_arabian': {'start': '10A80', 'end': '10A9F'}, 'manichaean': {'start': '10AC0', 'end': '10AFF'}, 'avestan': {'start': '10B00', 'end': '10B3F'}, 'inscriptional_parthian': {'start': '10B40', 'end': '10B5F'}, 'inscriptional_pahlavi': {'start': '10B60', 'end': '10B7F'}, 'psalter_pahlavi': {'start': '10B80', 'end': '10BAF'}, 'old_turkic': {'start': '10C00', 'end': '10C4F'}, 'old_hungarian': {'start': '10C80', 'end': '10CFF'}, 'hanifi_rohingya': {'start': '10D00', 'end': '10D3F'}, 'garay': {'start': '10D40', 'end': '10D8F'}, 'rumi_numeral_symbols': {'start': '10E60', 'end': '10E7F'}, 'yezidi': {'start': '10E80', 'end': '10EBF'}, 'arabic_extended-c': {'start': '10EC0', 'end': '10EFF'}, 'old_sogdian': {'start': '10F00', 'end': '10F2F'}, 'sogdian': {'start': '10F30', 'end': '10F6F'}, 'old_uyghur': {'start': '10F70', 'end': '10FAF'}, 'chorasmian': {'start': '10FB0', 'end': '10FDF'}, 'elymaic': {'start': '10FE0', 'end': '10FFF'}, 'brahmi': {'start': '11000', 'end': '1107F'}, 'kaithi': {'start': '11080', 'end': '110CF'}, 'sora_sompeng': {'start': '110D0', 'end': '110FF'}, 'chakma': {'start': '11100', 'end': '1114F'}, 'mahajani': {'start': '11150', 'end': '1117F'}, 'sharada': {'start': '11180', 'end': '111DF'}, 'sinhala_archaic_numbers': {'start': '111E0', 'end': '111FF'}, 'khojki': {'start': '11200', 'end': '1124F'}, 'multani': {'start': '11280', 'end': '112AF'}, 'khudawadi': {'start': '112B0', 'end': '112FF'}, 'grantha': {'start': '11300', 'end': '1137F'}, 'tulu-tigalari': {'start': '11380', 'end': '113FF'}, 'newa': {'start': '11400', 'end': '1147F'}, 'tirhuta': {'start': '11480', 'end': '114DF'}, 'siddham': {'start': '11580', 'end': '115FF'}, 'modi': {'start': '11600', 'end': '1165F'}, 'mongolian_supplement': {'start': '11660', 'end': '1167F'}, 'takri': {'start': '11680', 'end': '116CF'}, 'myanmar_extended-c': {'start': '116D0', 'end': '116FF'}, 'ahom': {'start': '11700', 'end': '1174F'}, 'dogra': {'start': '11800', 'end': '1184F'}, 'warang_citi': {'start': '118A0', 'end': '118FF'}, 'dives_akuru': {'start': '11900', 'end': '1195F'}, 'nandinagari': {'start': '119A0', 'end': '119FF'}, 'zanabazar_square': {'start': '11A00', 'end': '11A4F'}, 'soyombo': {'start': '11A50', 'end': '11AAF'}, 'unified_canadian_aboriginal_syllabics_extended-a': {'start': '11AB0', 'end': '11ABF'}, 'pau_cin_hau': {'start': '11AC0', 'end': '11AFF'}, 'devanagari_extended-a': {'start': '11B00', 'end': '11B5F'}, 'sunuwar': {'start': '11BC0', 'end': '11BFF'}, 'bhaiksuki': {'start': '11C00', 'end': '11C6F'}, 'marchen': {'start': '11C70', 'end': '11CBF'}, 'masaram_gondi': {'start': '11D00', 'end': '11D5F'}, 'gunjala_gondi': {'start': '11D60', 'end': '11DAF'}, 'makasar': {'start': '11EE0', 'end': '11EFF'}, 'kawi': {'start': '11F00', 'end': '11F5F'}, 'lisu_supplement': {'start': '11FB0', 'end': '11FBF'}, 'tamil_supplement': {'start': '11FC0', 'end': '11FFF'}, 'cuneiform': {'start': '12000', 'end': '123FF'}, 'cuneiform_numbers_and_punctuation': {'start': '12400', 'end': '1247F'}, 'early_dynastic_cuneiform': {'start': '12480', 'end': '1254F'}, 'cypro-minoan': {'start': '12F90', 'end': '12FFF'}, 'egyptian_hieroglyphs': {'start': '13000', 'end': '1342F'}, 'egyptian_hieroglyph_format_controls': {'start': '13430', 'end': '1345F'}, 'egyptian_hieroglyphs_extended-a': {'start': '13460', 'end': '143FF'}, 'anatolian_hieroglyphs': {'start': '14400', 'end': '1467F'}, 'gurung_khema': {'start': '16100', 'end': '1613F'}, 'bamum_supplement': {'start': '16800', 'end': '16A3F'}, 'mro': {'start': '16A40', 'end': '16A6F'}, 'tangsa': {'start': '16A70', 'end': '16ACF'}, 'bassa_vah': {'start': '16AD0', 'end': '16AFF'}, 'pahawh_hmong': {'start': '16B00', 'end': '16B8F'}, 'kirat_rai': {'start': '16D40', 'end': '16D7F'}, 'medefaidrin': {'start': '16E40', 'end': '16E9F'}, 'miao': {'start': '16F00', 'end': '16F9F'}, 'ideographic_symbols_and_punctuation': {'start': '16FE0', 'end': '16FFF'}, 'tangut': {'start': '17000', 'end': '187FF'}, 'tangut_components': {'start': '18800', 'end': '18AFF'}, 'khitan_small_script': {'start': '18B00', 'end': '18CFF'}, 'tangut_supplement': {'start': '18D00', 'end': '18D7F'}, 'kana_extended-b': {'start': '1AFF0', 'end': '1AFFF'}, 'kana_supplement': {'start': '1B000', 'end': '1B0FF'}, 'kana_extended-a': {'start': '1B100', 'end': '1B12F'}, 'small_kana_extension': {'start': '1B130', 'end': '1B16F'}, 'nushu': {'start': '1B170', 'end': '1B2FF'}, 'duployan': {'start': '1BC00', 'end': '1BC9F'}, 'shorthand_format_controls': {'start': '1BCA0', 'end': '1BCAF'}, 'symbols_for_legacy_computing_supplement': {'start': '1CC00', 'end': '1CEBF'}, 'znamenny_musical_notation': {'start': '1CF00', 'end': '1CFCF'}, 'byzantine_musical_symbols': {'start': '1D000', 'end': '1D0FF'}, 'musical_symbols': {'start': '1D100', 'end': '1D1FF'}, 'ancient_greek_musical_notation': {'start': '1D200', 'end': '1D24F'}, 'kaktovik_numerals': {'start': '1D2C0', 'end': '1D2DF'}, 'mayan_numerals': {'start': '1D2E0', 'end': '1D2FF'}, 'tai_xuan_jing_symbols': {'start': '1D300', 'end': '1D35F'}, 'counting_rod_numerals': {'start': '1D360', 'end': '1D37F'}, 'mathematical_alphanumeric_symbols': {'start': '1D400', 'end': '1D7FF'}, 'sutton_signwriting': {'start': '1D800', 'end': '1DAAF'}, 'latin_extended-g': {'start': '1DF00', 'end': '1DFFF'}, 'glagolitic_supplement': {'start': '1E000', 'end': '1E02F'}, 'cyrillic_extended-d': {'start': '1E030', 'end': '1E08F'}, 'nyiakeng_puachue_hmong': {'start': '1E100', 'end': '1E14F'}, 'toto': {'start': '1E290', 'end': '1E2BF'}, 'wancho': {'start': '1E2C0', 'end': '1E2FF'}, 'nag_mundari': {'start': '1E4D0', 'end': '1E4FF'}, 'ol_onal': {'start': '1E5D0', 'end': '1E5FF'}, 'ethiopic_extended-b': {'start': '1E7E0', 'end': '1E7FF'}, 'mende_kikakui': {'start': '1E800', 'end': '1E8DF'}, 'adlam': {'start': '1E900', 'end': '1E95F'}, 'indic_siyaq_numbers': {'start': '1EC70', 'end': '1ECBF'}, 'ottoman_siyaq_numbers': {'start': '1ED00', 'end': '1ED4F'}, 'arabic_mathematical_alphabetic_symbols': {'start': '1EE00', 'end': '1EEFF'}, 'mahjong_tiles': {'start': '1F000', 'end': '1F02F'}, 'domino_tiles': {'start': '1F030', 'end': '1F09F'}, 'playing_cards': {'start': '1F0A0', 'end': '1F0FF'}, 'enclosed_alphanumeric_supplement': {'start': '1F100', 'end': '1F1FF'}, 'enclosed_ideographic_supplement': {'start': '1F200', 'end': '1F2FF'}, 'miscellaneous_symbols_and_pictographs': {'start': '1F300', 'end': '1F5FF'}, 'emoticons': {'start': '1F600', 'end': '1F64F'}, 'ornamental_dingbats': {'start': '1F650', 'end': '1F67F'}, 'transport_and_map_symbols': {'start': '1F680', 'end': '1F6FF'}, 'alchemical_symbols': {'start': '1F700', 'end': '1F77F'}, 'geometric_shapes_extended': {'start': '1F780', 'end': '1F7FF'}, 'supplemental_arrows-c': {'start': '1F800', 'end': '1F8FF'}, 'supplemental_symbols_and_pictographs': {'start': '1F900', 'end': '1F9FF'}, 'chess_symbols': {'start': '1FA00', 'end': '1FA6F'}, 'symbols_and_pictographs_extended-a': {'start': '1FA70', 'end': '1FAFF'}, 'symbols_for_legacy_computing': {'start': '1FB00', 'end': '1FBFF'}, 'cjk_unified_ideographs_extension_b': {'start': '20000', 'end': '2A6DF'}, 'cjk_unified_ideographs_extension_c': {'start': '2A700', 'end': '2B73F'}, 'cjk_unified_ideographs_extension_d': {'start': '2B740', 'end': '2B81F'}, 'cjk_unified_ideographs_extension_e': {'start': '2B820', 'end': '2CEAF'}, 'cjk_unified_ideographs_extension_f': {'start': '2CEB0', 'end': '2EBEF'}, 'cjk_unified_ideographs_extension_i': {'start': '2EBF0', 'end': '2EE5F'}, 'cjk_compatibility_ideographs_supplement': {'start': '2F800', 'end': '2FA1F'}, 'cjk_unified_ideographs_extension_g': {'start': '30000', 'end': '3134F'}, 'cjk_unified_ideographs_extension_h': {'start': '31350', 'end': '323AF'}, 'tags': {'start': 'E0000', 'end': 'E007F'}, 'variation_selectors_supplement': {'start': 'E0100', 'end': 'E01EF'}, 'supplementary_private_use_area-a': {'start': 'F0000', 'end': 'FFFFF'}, 'supplementary_private_use_area-b': {'start': '100000', 'end': '10FFFF'}}

# Move to utilities?
def prep_label(label):
    return label.replace(" ", "_").lower()

class InvalidCharLengthException(Exception):
    "Raised when the method requires exactly one character, but additional characters were given."
    pass

def get_property(char: str, property: int, short_name: bool = False, max_ver: float | None = None) -> str | bool | None:
    """_summary_

    Args:
        char (str): Single character to be evaluated
        property (int): Unicode property to evaluate.
        short_name (bool, optional): Return abbreviation for property value.
            Only applies to non-binary properties. Defaults to False.
            Where _icu.UPropertyNameChoice.SHORT_PROPERTY_NAME is 0 and
            _icu.UPropertyNameChoice.LONG_PROPERTY_NAME is 1

        Examples:
            get_property('𞤀', _icu.UProperty.ALPHABETIC)
            get_property('𞤀', _icu.UProperty.BLOCK)
            get_property('𞤀', _icu.UProperty.SCRIPT)
            get_property('\U0001e900', 4106, True)
            get_property('𞤀', _icu.UProperty.GENERAL_CATEGORY)
            get_property('𞤀', _icu.UProperty.GENERAL_CATEGORY, True)

        Refer to:
            * https://unicode-org.github.io/_icu/userguide/strings/properties.html
            * https://unicode-org.github.io/_icu-docs/apidoc/released/_icu4c/uchar_8h.html
            * https://www.unicode.org/Public/UCD/latest/ucd/PropertyAliases.txt
            * https://www.unicode.org/reports/tr44/#Properties

    Returns:
        str | bool | None: Property value for the character
    """
    if len(char) != 1:
        print("Please specify a single character.")
        return None

    if property in BINARY_PROPERTIES:
        return _icu.Char.hasBinaryProperty(char, property)
    name_choice = 0 if short_name else 1
    value = _icu.Char.getIntPropertyValue(char, property)
    return _icu.Char.getPropertyValueName(property, value, name_choice)

class UCD():
    def __init__(self, char):
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

    def __str__(self):
        return self._char

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(char={self._char}, codepoint={self._cp}, name={self._name})"

    def _get_property(self, property: int, short_name: bool = False) -> str | bool:
        char = self._char
        if property in BINARY_PROPERTIES:
            return _icu.Char.hasBinaryProperty(char, property)

        name_choice = 0 if short_name else 1
        value = _icu.Char.getIntPropertyValue(char, property)
        return _icu.Char.getPropertyValueName(property, value, name_choice)

    def _bchar(self):
        return bin(ord(self._char))
    def _ochar(self):
        return oct(ord(self._char))
    def _dchar(self):
        return ord(self._char)
    def _xchar(self):
        return hex(ord(self._char))

    def _hex_ncr(self, exclude_ascii: bool, as_char: bool):
        char = self._char
        dchar = ord(char)
        if exclude_ascii and dchar <= 127:
            return '-' if not as_char else char
        return f'&#x{dchar:04X};'

    def _dec_ncr(self, exclude_ascii: bool, as_char: bool):
        char = self._char
        dchar = ord(char)
        if exclude_ascii and dchar <= 127:
            return '-' if not as_char else char
        return f'&#{dchar:04};'

    def _html_entity(self):
        dchar = ord(self._char)
        entity = _html.entities.codepoint2name.get(dchar)
        return f'&{entity};' if entity else '-'

    UNICODE_VERSION = _icu.UNICODE_VERSION

    def age(self):
        return _icu.Char.charAge(self._char)

    alphabetic = _partialmethod(_get_property, property = _icu.UProperty.ALPHABETIC, short_name = False)
    ascii_hex_digit = _partialmethod(_get_property, property = _icu.UProperty.ASCII_HEX_DIGIT, short_name = False)
    basic_emoji = _partialmethod(_get_property, property = _icu.UProperty.BASIC_EMOJI, short_name = False)
    bidi_class = _partialmethod(_get_property, property = _icu.UProperty.BIDI_CLASS, short_name = False)
    bidi_class_code = _partialmethod(_get_property, property = _icu.UProperty.BIDI_CLASS, short_name = True)
    bidi_control = _partialmethod(_get_property, property = _icu.UProperty.BIDI_CONTROL, short_name = False)
    bidi_mirrored = _partialmethod(_get_property, property = _icu.UProperty.BIDI_MIRRORED, short_name = False)

    def bidi_mirroring_glyph(self):
        result = _icu.Char.charMirror(self._char)
        if result != self._char:
            return result
        return None

    def bidi_paired_bracket(self):
        result = _icu.Char.getBidiPairedBracket(self._char)
        if result != self._char:
            return result
        return None

    bidi_paired_bracket_type = _partialmethod(_get_property, property = _icu.UProperty.BIDI_PAIRED_BRACKET_TYPE, short_name = False)
    bidi_paired_bracket_type_code = _partialmethod(_get_property, property = _icu.UProperty.BIDI_PAIRED_BRACKET_TYPE, short_name = True)
    block = _partialmethod(_get_property, property = _icu.UProperty.BLOCK, short_name = False)
    block_code = _partialmethod(_get_property, property = _icu.UProperty.BLOCK, short_name = True)
    # see combining_class for numeric equivalent
    canonical_combining_class = _partialmethod(_get_property, property = _icu.UProperty.CANONICAL_COMBINING_CLASS, short_name = False)
    canonical_combining_class_code = _partialmethod(_get_property, property = _icu.UProperty.CANONICAL_COMBINING_CLASS, short_name = True)

    def case_folding(self):
        return _icu.CaseMap.fold(self._char)

    case_ignorable = _partialmethod(_get_property, property = _icu.UProperty.CASE_IGNORABLE, short_name = False)
    case_sensitive = _partialmethod(_get_property, property = _icu.UProperty.CASE_SENSITIVE, short_name = False)
    cased = _partialmethod(_get_property, property = _icu.UProperty.CASED, short_name = False)
    changes_when_casefolded = _partialmethod(_get_property, property = _icu.UProperty.CHANGES_WHEN_CASEFOLDED, short_name = False)
    changes_when_casemapped = _partialmethod(_get_property, property = _icu.UProperty.CHANGES_WHEN_CASEMAPPED, short_name = False)
    changes_when_lowercased = _partialmethod(_get_property, property = _icu.UProperty.CHANGES_WHEN_LOWERCASED, short_name = False)
    changes_when_nfkc_casefolded = _partialmethod(_get_property, property = _icu.UProperty.CHANGES_WHEN_NFKC_CASEFOLDED, short_name = False)
    changes_when_titlecased = _partialmethod(_get_property, property = _icu.UProperty.CHANGES_WHEN_TITLECASED, short_name = False)
    changes_when_uppercased = _partialmethod(_get_property, property = _icu.UProperty.CHANGES_WHEN_UPPERCASED, short_name = False)

    def character(self):
        return self._char

    def codepoint(self, decimal=False) -> str:
        if decimal:
            return int(self._cp, 16)
        return self._cp

    def combining_class(self):
        # see canonical_combining_class, canonical_combining_class_code for alphabetic equivalent
        return _icu.Char.getCombiningClass(self._char)

    dash = _partialmethod(_get_property, property = _icu.UProperty.DASH, short_name = False)
    decomposition_type = _partialmethod(_get_property, property = _icu.UProperty.DECOMPOSITION_TYPE, short_name = False)
    default_ignorable_code_point = _partialmethod(_get_property, property = _icu.UProperty.DEFAULT_IGNORABLE_CODE_POINT, short_name = False)
    diacritic = _partialmethod(_get_property, property = _icu.UProperty.DIACRITIC, short_name = False)

    # digit same as digit_value
    def digit(self):
        value = _icu.Char.digit(self._char)
        return value if value != -1 else None

    def digit_value(self):
        value = _icu.Char.charDigitValue(self._char)
        return value if value != -1 else None

    # direction - same as bidi_class
    def direction(self):
        value = _icu.charDirection(self._char)
        return _icu.Char.getPropertyValueName(_icu.UProperty.BIDI_CLASS, value, _icu.UPropertyNameChoice.LONG_PROPERTY_NAME)

    # direction_code - same as bidi_class_code
    def direction_code(self):
        value = _icu.charDirection(self._char)
        return _icu.Char.getPropertyValueName(_icu.UProperty.BIDI_CLASS, value, _icu.UPropertyNameChoice.SHORT_PROPERTY_NAME)

    east_asian_width = _partialmethod(_get_property, property = _icu.UProperty.EAST_ASIAN_WIDTH, short_name = False)
    east_asian_width_code = _partialmethod(_get_property, property = _icu.UProperty.EAST_ASIAN_WIDTH, short_name = True)
    emoji = _partialmethod(_get_property, property = _icu.UProperty.EMOJI, short_name = False)
    emoji_component = _partialmethod(_get_property, property = _icu.UProperty.EMOJI_COMPONENT, short_name = False)
    emoji_keycap_sequence = _partialmethod(_get_property, property = _icu.UProperty.EMOJI_KEYCAP_SEQUENCE, short_name = False)
    emoji_modifier = _partialmethod(_get_property, property = _icu.UProperty.EMOJI_MODIFIER, short_name = False)
    emoji_modifier_base = _partialmethod(_get_property, property = _icu.UProperty.EMOJI_MODIFIER_BASE, short_name = False)
    emoji_presentation = _partialmethod(_get_property, property = _icu.UProperty.EMOJI_PRESENTATION, short_name = False)
    extended_pictographic = _partialmethod(_get_property, property = _icu.UProperty.EXTENDED_PICTOGRAPHIC, short_name = False)
    extender = _partialmethod(_get_property, property = _icu.UProperty.EXTENDER, short_name = False)

    def fc_nfkc_closure(self):
        return _icu.Char.getFC_NFKC_Closure(self._char)

    # def for_digit(self, radix=10):
    #     return _icu.Char.forDigit(int(self._char), radix)

    full_composition_exclusion = _partialmethod(_get_property, property = _icu.UProperty.FULL_COMPOSITION_EXCLUSION, short_name = False)
    general_category = _partialmethod(_get_property, property = _icu.UProperty.GENERAL_CATEGORY, short_name = False)
    general_category_code = _partialmethod(_get_property, property = _icu.UProperty.GENERAL_CATEGORY, short_name = True)
    general_category_mask = _partialmethod(_get_property, property = _icu.UProperty.GENERAL_CATEGORY_MASK, short_name = False)
    grapheme_base = _partialmethod(_get_property, property = _icu.UProperty.GRAPHEME_BASE, short_name = False)
    grapheme_cluster_break = _partialmethod(_get_property, property = _icu.UProperty.GRAPHEME_CLUSTER_BREAK, short_name = False)
    grapheme_extend = _partialmethod(_get_property, property = _icu.UProperty.GRAPHEME_EXTEND, short_name = False)
    grapheme_link = _partialmethod(_get_property, property = _icu.UProperty.GRAPHEME_LINK, short_name = False)
    hangul_syllable_type = _partialmethod(_get_property, property = _icu.UProperty.HANGUL_SYLLABLE_TYPE, short_name = False)
    hangul_syllable_type_code = _partialmethod(_get_property, property = _icu.UProperty.HANGUL_SYLLABLE_TYPE, short_name = True)
    hex_digit = _partialmethod(_get_property, property = _icu.UProperty.HEX_DIGIT, short_name = False)

    def html_entity(self, hexadecimal = True):
        if int(self._cp, 16) < 128:
            return _html.escape(self._char)
        if hexadecimal:
            return f'&#x{self._cp};'
        return f'&#{int(self._cp, 16)};'

    id_continue = _partialmethod(_get_property, property = _icu.UProperty.ID_CONTINUE, short_name = False)
    id_start = _partialmethod(_get_property, property = _icu.UProperty.ID_START, short_name = False)
    hyphen = _partialmethod(_get_property, property = _icu.UProperty.HYPHEN, short_name = False)
    ideographic = _partialmethod(_get_property, property = _icu.UProperty.IDEOGRAPHIC, short_name = False)
    ids_binary_operator = _partialmethod(_get_property, property = _icu.UProperty.IDS_BINARY_OPERATOR, short_name = False)
    ids_trinary_operator = _partialmethod(_get_property, property = _icu.UProperty.IDS_TRINARY_OPERATOR, short_name = False)

    def in_set(self, uset):
        return True if self._char in list(_icu.UnicodeSet(uset)) else False

    indic_positional_category = _partialmethod(_get_property, property = _icu.UProperty.INDIC_POSITIONAL_CATEGORY, short_name = False)
    indic_syllabic_category = _partialmethod(_get_property, property = _icu.UProperty.INDIC_SYLLABIC_CATEGORY, short_name = False)
    int_start = _partialmethod(_get_property, property = _icu.UProperty.INT_START, short_name = False)

    def is_alnum(self) -> bool:
        return _icu.Char.isalnum(self._char)

    def is_alpha(self) -> bool:
        return _icu.Char.isalpha(self._char)

    def is_ascii(self):
        char = self._char
        return char.isascii()

    def is_base(self) -> bool:
        return _icu.Char.isbase(self._char)

    def is_blank(self) -> bool:
        return _icu.Char.isblank(self._char)

    def is_cased(self) -> bool:
        # _icu.UProperty.CASED : 49
        return self._get_property(property = 49)

    def is_cntrl(self) -> bool:
        return _icu.Char.iscntrl(self._char)

    def is_defined(self) -> bool:
        return _icu.Char.isdefined(self._char)

    def is_digit(self) -> bool:
        return _icu.Char.isdigit(self._char)

    def is_graph(self) -> bool:
        return _icu.Char.isgraph(self._char)

    def is_id_ignorable(self):
        return _icu.Char.isIDIgnorable(self._char)

    def is_id_part(self):
        return _icu.Char.isIDPart(self._char)

    def is_id_start(self):
        return _icu.Char.isIDStart(self._char)

    def is_iso_control(self):
        return _icu.Char.isISOControl(self._char)

    def is_java_id_part(self):
        return _icu.Char.isJavaIDPart(self._char)

    def is_java_id_start(self):
        return _icu.Char.isJavaIDStart(self._char)

    def is_java_space_char(self):
        return _icu.Char.isJavaSpaceChar(self._char)

    def is_lower(self) -> bool:
        return _icu.Char.islower(self._char)

    def is_mirrored(self):
        return _icu.Char.isMirrored(self._char)

    def is_nfc(self):
        char = self._char
        norm_char = _icu.Normalizer2.getNFCInstance().normalize(char)
        return norm_char == char

    def is_nfkc(self):
        char = self._char
        norm_char = _icu.Normalizer2.getNFKCInstance().normalize(char)
        return norm_char == char

    def is_nfd(self):
        char = self._char
        norm_char = _icu.Normalizer2.getNFDInstance().normalize(char)
        return norm_char == char

    def is_nfkd(self):
        char = self._char
        norm_char = _icu.Normalizer2.getNFKDInstance().normalize(char)
        return norm_char == char

    def is_print(self):
        return _icu.Char.isprint(self._char)

    def is_punct(self):
        return _icu.Char.ispunct(self._char)

    def is_space(self):
        return _icu.Char.isspace(self._char)

    def is_script(self, sc:str) -> bool:
        return True if self.script() == sc or self.script_code == sc else False

    def is_title(self) -> bool:
        return _icu.Char.istitle(self._char)

    def is_u_alphabetic(self):
        return _icu.Char.isUAlphabetic(self._char)

    def is_u_lowercase(self):
        return _icu.Char.isULowercase(self._char)

    def is_u_uppercase(self):
        return _icu.Char.isUUppercase(self._char)

    def is_u_whitespace(self):
        return _icu.Char.isUWhiteSpace(self._char)

    def is_upper(self) -> bool:
        return _icu.Char.isupper(self._char)

    def is_whitespace(self):
        return _icu.Char.isWhitespace(self._char)

    def is_xdigit(self):
        return _icu.Char.isxdigit(self._char)
    join_control = _partialmethod(_get_property, property = _icu.UProperty.JOIN_CONTROL, short_name = False)
    joining_group = _partialmethod(_get_property, property = _icu.UProperty.JOINING_GROUP, short_name = False)
    joining_type = _partialmethod(_get_property, property = _icu.UProperty.JOINING_TYPE, short_name = False)
    lead_canonical_combining_class = _partialmethod(_get_property, property = _icu.UProperty.LEAD_CANONICAL_COMBINING_CLASS, short_name = False)
    line_break = _partialmethod(_get_property, property = _icu.UProperty.LINE_BREAK, short_name = False)
    logical_order_exception = _partialmethod(_get_property, property = _icu.UProperty.LOGICAL_ORDER_EXCEPTION, short_name = False)
    lowercase = _partialmethod(_get_property, property = _icu.UProperty.LOWERCASE, short_name = False)

    def lowercase_mapping(self):
        return _icu.CaseMap.toLower(self._char)

    mask_start = _partialmethod(_get_property, property = _icu.UProperty.MASK_START, short_name = False)
    math = _partialmethod(_get_property, property = _icu.UProperty.MATH, short_name = False)

    def mirror(self):
        return _icu.Char.charMirror(self._char)

    def name(self) -> str:
        return self._name

    def name_alias(self):
        return _icu.Char.charName(self._char, _icu.UCharNameChoice.CHAR_NAME_ALIAS)

    nfc_inert = _partialmethod(_get_property, property = _icu.UProperty.NFC_INERT, short_name = False)
    nfc_quick_check = _partialmethod(_get_property, property = _icu.UProperty.NFC_QUICK_CHECK, short_name = False)

    def nfd_contains(self, uset=_icu.UnicodeSet(r'[:Latin:]')) -> list[str]:
        normalizer = _icu.Normalizer2.getNFDInstance()
        domain = list(uset)
        return [item for item in domain if self._char in normalizer.normalize(item)]

    nfd_inert = _partialmethod(_get_property, property = _icu.UProperty.NFD_INERT, short_name = False)
    nfd_quick_check = _partialmethod(_get_property, property = _icu.UProperty.NFD_QUICK_CHECK, short_name = False)

    def nfkc_casefold(self):
        return _icu.Normalizer2.getNFKCCasefoldInstance().normalize(self._char)

    nfkc_inert = _partialmethod(_get_property, property = _icu.UProperty.NFKC_INERT, short_name = False)
    nfkc_quick_check = _partialmethod(_get_property, property = _icu.UProperty.NFKC_QUICK_CHECK, short_name = False)

    def nfkd_contains(self, uset=_icu.UnicodeSet(r'[:Latin:]')) -> list[str]:
        # UCD('b').nfkd_contains(_icu.UnicodeSet(r'[:Any:]'))
        normalizer = _icu.Normalizer2.getNFKDInstance()
        domain = list(uset)
        return [item for item in domain if self._char in normalizer.normalize(item)]

    nfkd_inert = _partialmethod(_get_property, property = _icu.UProperty.NFKD_INERT, short_name = False)
    nfkd_quick_check = _partialmethod(_get_property, property = _icu.UProperty.NFKD_QUICK_CHECK, short_name = False)
    noncharacter_code_point = _partialmethod(_get_property, property = _icu.UProperty.NONCHARACTER_CODE_POINT, short_name = False)
    numeric_type = _partialmethod(_get_property, property = _icu.UProperty.NUMERIC_TYPE, short_name = False)
    numeric_type_code = _partialmethod(_get_property, property = _icu.UProperty.NUMERIC_TYPE, short_name = True)

    def numeric_value(self):
        return _icu.Char.getNumericValue(self._char)

    pattern_syntax = _partialmethod(_get_property, property = _icu.UProperty.PATTERN_SYNTAX, short_name = False)
    pattern_white_space = _partialmethod(_get_property, property = _icu.UProperty.PATTERN_WHITE_SPACE, short_name = False)
    posix_alnum = _partialmethod(_get_property, property = _icu.UProperty.POSIX_ALNUM, short_name = False)
    posix_blank = _partialmethod(_get_property, property = _icu.UProperty.POSIX_BLANK, short_name = False)
    posix_graph = _partialmethod(_get_property, property = _icu.UProperty.POSIX_GRAPH, short_name = False)
    posix_print = _partialmethod(_get_property, property = _icu.UProperty.POSIX_PRINT, short_name = False)
    posix_xdigit = _partialmethod(_get_property, property = _icu.UProperty.POSIX_XDIGIT, short_name = False)
    prepended_concatenation_mark = _partialmethod(_get_property, property = _icu.UProperty.PREPENDED_CONCATENATION_MARK, short_name = False)
    quotation_mark = _partialmethod(_get_property, property = _icu.UProperty.QUOTATION_MARK, short_name = False)
    radical = _partialmethod(_get_property, property = _icu.UProperty.RADICAL, short_name = False)  # https://en.wikipedia.org/wiki/List_of_radicals_in_Unicode
    regional_indicator = _partialmethod(_get_property, property = _icu.UProperty.REGIONAL_INDICATOR, short_name = False)  # https://en.wikipedia.org/wiki/Regional_indicator_symbol
    # Move following to ucds()
    # rgi_emoji = _partialmethod(_get_property, property = _icu.UProperty.RGI_EMOJI, short_name = False)
    # rgi_emoji_flag_sequence = _partialmethod(_get_property, property = _icu.UProperty.RGI_EMOJI_FLAG_SEQUENCE, short_name = False)
    # rgi_emoji_modifier_sequence = _partialmethod(_get_property, property = _icu.UProperty.RGI_EMOJI_MODIFIER_SEQUENCE, short_name = False)
    # rgi_emoji_tag_sequence = _partialmethod(_get_property, property = _icu.UProperty.RGI_EMOJI_TAG_SEQUENCE, short_name = False)
    # rgi_emoji_zwj_sequence = _partialmethod(_get_property, property = _icu.UProperty.RGI_EMOJI_ZWJ_SEQUENCE, short_name = False)
    script = _partialmethod(_get_property, property = _icu.UProperty.SCRIPT, short_name = False)
    script_code = _partialmethod(_get_property, property = _icu.UProperty.SCRIPT, short_name = True)

    def script_extensions(self):
        return [_icu.Script(sc).getName() for sc in _icu.Script.getScriptExtensions(self._char)]

    def script_extensions_codes(self):
        return [_icu.Script(sc).getShortName() for sc in _icu.Script.getScriptExtensions(self._char)]

    segment_starter = _partialmethod(_get_property, property = _icu.UProperty.SEGMENT_STARTER, short_name = False)
    sentence_break = _partialmethod(_get_property, property = _icu.UProperty.SENTENCE_BREAK, short_name = False)

    def simple_case_folding(self):
        return _icu.Char.foldCase(self._char)
    def simple_lowercase_mapping(self):
        return _icu.Char.tolower(self._char)
    def simple_titlecase_mapping(self):
        return _icu.Char.totitle(self._char)
    def simple_uppercase_mapping(self):
        return _icu.Char.toupper(self._char)

    soft_dotted = _partialmethod(_get_property, property = _icu.UProperty.SOFT_DOTTED, short_name = False)
    s_term = _partialmethod(_get_property, property = _icu.UProperty.S_TERM, short_name = False)
    terminal_punctuation = _partialmethod(_get_property, property = _icu.UProperty.TERMINAL_PUNCTUATION, short_name = False)

    def titlecase_mapping(self):
        return _icu.CaseMap.toTitle(self._char)

    trail_canonical_combining_class = _partialmethod(_get_property, property = _icu.UProperty.TRAIL_CANONICAL_COMBINING_CLASS, short_name = False)

    # type same as general_category
    def type(self):
        value = _icu.Char.charType(self._char)
        _icu.Char.getPropertyValueName(_icu.UProperty.GENERAL_CATEGORY, value, _icu.UPropertyNameChoice.LONG_PROPERTY_NAME)

    # type_code same as general_category_code
    def type_code(self):
        value = _icu.Char.charType(self._char)
        _icu.Char.getPropertyValueName(_icu.UProperty.GENERAL_CATEGORY, value, _icu.UPropertyNameChoice.SHORT_PROPERTY_NAME)

    unified_ideograph = _partialmethod(_get_property, property = _icu.UProperty.UNIFIED_IDEOGRAPH, short_name = False)
    uppercase = _partialmethod(_get_property, property = _icu.UProperty.UPPERCASE, short_name = False)

    def uppercase_mapping(self):
        return _icu.CaseMap.toUpper(self._char)

    def utf8_bytes(self):
        char = self._char
        return char.encode('utf-8').hex(' ')

    def utf16_le_bytes(self):
        char = self._char
        return char.encode('utf-16-le').hex(' ')

    def utf16_be_bytes(self):
        char = self._char
        return char.encode('utf-16-be').hex(' ')

    def utf32_le_bytes(self):
        char = self._char
        return char.encode('utf-32-le').hex(' ')

    def utf32_be_bytes(self):
        char = self._char
        return char.encode('utf-32-be').hex(' ')

    variation_selector = _partialmethod(_get_property, property = _icu.UProperty.VARIATION_SELECTOR, short_name = False)
    vertical_orientation = _partialmethod(_get_property, property = _icu.UProperty.VERTICAL_ORIENTATION, short_name = False)
    white_space = _partialmethod(_get_property, property = _icu.UProperty.WHITE_SPACE, short_name = False)
    word_break = _partialmethod(_get_property, property = _icu.UProperty.WORD_BREAK, short_name = False)
    xid_continue = _partialmethod(_get_property, property = _icu.UProperty.XID_CONTINUE, short_name = False)
    xid_start = _partialmethod(_get_property, property = _icu.UProperty.XID_START, short_name = False)

class UCDString():
    def __init__(self, chars):
        self._chars = [UCD(char) for char in chars]
        self.data = [c.data for c in self._chars]
        self.entities = [c.entities for c in self._chars]

    def __str__(self):
        return "".join(self.characters())

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(chars={self.characters()})"

    def __len__(self: _Self) -> int:
        return len(self._chars)

    def __getitem__(self: _Self, i) -> _Self:
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            return UCDString("".join([
                self.data[index][0] for index in range(start, stop, step)
            ]))
        else:
            return UCDString(self.data[i][0])

    def ages(self):
        return [c.age() for c in self._chars]

    def blocks(self):
        return [c.block() for c in self._chars]

    def characters(self):
        return [c.character() for c in self._chars]

    def codepoints(self, decimal=False):
        return [c.codepoint(decimal) for c in self._chars]

    def in_set(self, uset):
        return [c.in_set(uset) for c in self._chars]

    def names(self):
        return [c.name() for c in self._chars]

    def scripts(self):
       return [c.script() for c in self._chars]

    def properties(self, property, short_name = False):
        return [c._get_property(property, short_name) for c in self._chars]



def unicode_data(text):
    """Display Unicode data for each character in string.

    Generate a table containing data on some Unicode character properties,
    including character codepoint and name, script character belongs to,

    Args:
        text (str): string to analyse.
    """
    data = UCDString(text).data
    console = _Console()
    table = _Table(
        show_header=True,
        header_style="light_slate_blue",
        title="Character properties",
        box=_box.SQUARE, 
        caption=f"String: {text}")
    table.add_column("char")
    table.add_column("cp")
    table.add_column("name")
    table.add_column("script")
    table.add_column("block")
    table.add_column("cat")
    table.add_column("bidi")
    table.add_column("cc")
    for datum in data:
        table.add_row(
            datum[0],
            datum[1],
            datum[2],
            datum[3],
            datum[4],
            datum[5],
            datum[6],
            str(datum[7]))
    # console.print(f"String: {text}")
    console.print(table)
    return None

udata = unicode_data

def casing_data(char: str):
    if len(char) > 1:
        raise(InvalidCharLengthException)
        print("Method takes a single character as a parameter.")
    char = UCD(char)
    upperc = (char.uppercase_mapping(), char.simple_uppercase_mapping())
    titlec = (char.titlecase_mapping(), char.simple_titlecase_mapping())
    lowerc = (char.lowercase_mapping(), char.simple_lowercase_mapping())
    cfolding = (char.case_folding(), char.simple_case_folding())
    console = _Console()
    table = _Table(
        show_header=True,
        header_style="light_slate_blue",
        title=f"Case mapping and folding",
        box=_box.SQUARE,
        caption=f"Character: {char.character()}")
    table.add_column("Operation")
    table.add_column("Full")
    table.add_column("Simple")
    table.add_row("Uppercase", upperc[0], upperc[1])
    table.add_row("Titlecase", titlec[0], titlec[1])
    table.add_row("Lowercase", lowerc[0], lowerc[1])
    table.add_row("Case folding", cfolding[0], cfolding[1])
    console.print(table)
    return None

def get_entities(char: str|int, exclude_ascii=False, as_char=False):
    '''
    Display codepoint values of character as binary, octal, decimal,
    and hexadecimal digits. Display HTML entities and HTML Numerical
    Character references for specified character.
    '''
    char = ord(char) if isinstance(char, int) else char
    if char.startswith('0b'):
        char = chr(int(char, 2))
    elif char.startswith('0o'):
        char = chr(int(char,8))
    elif char.startswith('0x'):
        char = chr(int(char, 16))
    if len(char) > 1:
        raise(InvalidCharLengthException)
        print("Method takes a single character as a parameter.")
    cdata = UCD(char)
    data = cdata.entities
    console = _Console()
    table = _Table(
        show_header=True,
        header_style="light_slate_blue",
        title=f"Numeric and entity values for Character",
        box=_box.SQUARE,
        caption=f"Character: {char.character()}")
    table.add_column("Character")
    table.add_column("Hexadecimal")
    table.add_column("Decimal")
    table.add_column("Octal")
    table.add_column("Binary")
    table.add_column("HTML ent")
    table.add_column("Dec. NCR")
    table.add_column("Hex. NCR")
    table.add_row(
        data[0],
        data[1],
        data[2],
        data[3],
        data[4],
        data[5],
        data[6],
        data[7]
    )
    # console.print(f"String: {text}")
    console.print(table)
    return None

def display_entities(text: str) -> None:
    data = UCDString(text).entities
    console = _Console()
    table = _Table(
        show_header=True,
        header_style="light_slate_blue",
        title=f"Numeric and entity values for Character",
        box=_box.SQUARE,
        caption=f"Character: {data.characters()}")
    table.add_column("Character")
    table.add_column("Hexadecimal")
    table.add_column("Decimal")
    table.add_column("Octal")
    table.add_column("Binary")
    table.add_column("HTML ent")
    table.add_column("Dec. NCR")
    table.add_column("Hex. NCR")
    for datum in data:
        table.add_row(
            datum[0],
            datum[1],
            datum[2],
            datum[3],
            datum[4],
            datum[5],
            datum[6],
            datum[7]
        )
    console.print(table)
    return None

entities = display_entities

def uset_to_list(notation:str) -> list[str]:
    uset = _icu.UnicodeSet(notation) 
    return list(uset)

def uset_to_pattern(notation: str) -> str:
    l = f'[{"".join(uset_to_list(notation))}]'
    return str(_icu.UnicodeSet(l).compact())

def uset_contains(chars:str, notation:str, mode:str='') -> bool:
    uset = _icu.UnicodeSet(notation)
    match mode.lower():
        case 'all':
            return uset.containsAll(chars)
        case "some":
            return uset.containsSome(chars)
        case "none":
            return uset.containsNone(chars)
        case _:
            return uset.contains(chars)

def count_unicode_for_method(fn) -> int:
    count = 0
    for i in range(0x10FFFF + 1):
        if fn(chr(i)):
            count += 1
    return count

def get_unicode_chars_for_method(fn, cp: bool = False) -> list[str]:
    chars = []
    for i in range(0x10FFFF + 1):
        if fn(chr(i)):
            chars.append(chr(i))
    if cp:
       return [f'{ord(ch):04X}' for ch in chars]
    return chars

def chars_to_codepoints(chars, decimal=False, enc='utf-8'):
    enc = enc.lower()
    result = []
    for char in chars:
        if ord(char) > 0xffff and enc == 'utf-16':
            result.extend(bytes(char, 'utf-16-be').hex(' ', bytes_per_sep=2).upper().split())
        else:
            result.append(f'{ord(char):04X}')
    if decimal:
        return [int(r, 16) for r in result]
    return result

# import el_data as eld
# s = 'abç 😊'
# eld.chars_to_codepoints(s)
# ['0061', '0062', '00E7', '0020', '1F60A']
# eld.chars_to_codepoints(s, True)
# [97, 98, 231, 32, 128522]
# eld.chars_to_codepoints(s, enc='utf-16')
# ['0061', '0062', '00E7', '0020', 'D83D', 'DE0A']
# eld.chars_to_codepoints(s, True, enc='utf-16')
# [97, 98, 231, 32, 55357, 56842]

def homogeneous_type(seq, typ):
    return all(isinstance(x, typ) for x in seq)
def codepoints_to_chars(codepoints, enc='utf-8'):
    enc = enc.lower()
    chars = [chr(c) for c in codepoints] if homogeneous_type(codepoints, int) else [chr(int(c, 16)) for c in codepoints]
    if enc == 'utf-16':
        return "".join(chars).encode('utf-16', 'surrogatepass').decode('utf-16')
    return "".join(chars)


# import el_data as eld
# eld.codepoints_to_chars(['0061', '0062', '00E7', '0020', '1F60A'])
# 'abç 😊'
# eld.codepoints_to_chars([97, 98, 231, 32, 128522])
# 'abç 😊'
# eld.codepoints_to_chars(['0061', '0062', '00E7', '0020', 'D83D', 'DE0A'], enc='utf-16')
# 'abç 😊'
# eld.codepoints_to_chars([97, 98, 231, 32, 55357, 56842], enc='utf-16')
# 'abç 😊'

def get_bytes(data, enc):
    byte_seq = []
    for char in data:
        try:
            byte_seq.append(char.encode(enc).hex(' ').upper())
        except UnicodeEncodeError:
            byte_seq.append('')
    return byte_seq

def display_byte_sequences(data: str, enc: str = 'utf-8') -> None:
    console = _Console()
    table = _Table(
        show_header=True,
        header_style="light_slate_blue",
        title="Byte representation of string",
        box=_box.SQUARE,
        caption=f"String: {data}\nEncoding: {enc}")
    table.add_column("Character")
    table.add_column("Bytes")
    byte_seq = get_bytes(data=data, enc=enc)
    for i, j in zip([*data], byte_seq):
        table.add_row(i, j)
    console.print(table)
    return None

# import el_data as eld
# eld.display_byte_sequences(input_chars, 'utf-8')
# eld.display_byte_sequences(input_chars, 'utf-16-be')
# eld.display_byte_sequences(input_chars, 'utf-32-be')
# eld.display_byte_sequences(input_chars, 'iso-8859-1')
# eld.display_byte_sequences(input_chars, 'iso-8859-19')
# eld.display_byte_sequences(input_chars, 'windows-1252')

def get_code_units(text: str, enc: str = 'utf-8', decimal: bool = False, structured=False) -> list[str|int|list[str|int]]:
    def is_structured(lst):
        return any(isinstance(i, list) for i in lst)
    if enc.lower() == 'utf-8':
        enc = enc.lower()
        bytes_per_sep = 1
    elif enc.lower() in ['utf-16', 'utf-16-be', 'utf-16-le']:
        enc = 'utf-16-be'
        bytes_per_sep = 2
    else:
        enc = 'utf-32-be'
        bytes_per_sep = 4
    if structured:
        result = [char.encode(enc).hex(' ', bytes_per_sep=bytes_per_sep).upper().split() for char in text]
    else:
        result = text.encode(enc).hex(' ', bytes_per_sep=bytes_per_sep).upper().split()
    if decimal:
        if is_structured(result):
            result = [[int(h, 16) for h in r] for r in result]
        else:
            result =  [int(r, 16) for r in result]
    return result

# import el_data as eld
# text = 'aéƒ'
# eld.get_code_units(text)
# ['61', 'c3', 'a9', 'c6', '92']
# eld.get_code_units(text, decimal=True)
# [97, 195, 169, 198, 146]
# eld.get_code_units(text, enc="utf-16")
# ['0061', '00e9', '0192']
# eld.get_code_units(text, enc="utf-16", decimal=True)
# [97, 233, 402]
# eld.get_code_units(text, enc="utf-32")
# ['00000061', '000000e9', '00000192']
# eld.get_code_units(text, enc="utf-32", decimal=True)
# [97, 233, 402]

def display_encoding_data(data, enc='utf-8', mode='codepoints_bytes'):
    match mode:
        case 'code_units':
            char_data = get_code_units(data, enc=enc, structured=True)
        case 'bytes':
            # char_data = [char.encode(enc).hex(' ').upper() for char in data]
            char_data = get_bytes(data=data, enc=enc)
        case _:
            char_data = [f'{ord(char):04X}' for char in data]
    console = _Console()
    table = _Table(
        show_header=False,
        title="Byte representation of string",
        box=_box.SQUARE,
        caption=f"String: {data}\nEncoding: {enc}",
        show_lines=True)
    for i in range(len(data)):
        table.add_column('', justify='center', vertical='middle')
    table.add_row(*data)
    table.add_row(*[" ".join(b) for b in char_data]) if mode == 'code_units' else table.add_row(*["".join(b) for b in char_data])
    if mode == 'codepoints_bytes':
        # byte_data = [char.encode(enc).hex(' ').upper() for char in data]
        byte_data = get_bytes(data=data, enc=enc)
        table.add_row(*["".join(b) for b in byte_data])
    console.print(table)
    return None

# import el_data as eld
# s = '€abç😊'
# eld.display_encoding_data(s)
# eld.display_encoding_data(s, mode='codepoints_bytes')
# eld.display_encoding_data(s, enc='windows-1252', mode='codepoints_bytes')
# eld.display_encoding_data(s, enc='latin-1', mode='codepoints_bytes')
# eld.display_encoding_data(s, mode='codepoints')
# eld.display_encoding_data(s, mode='code_units')
# eld.display_encoding_data(s, mode='bytes')

def analyse_bytes(data, encoding = 'utf-8'):
    if isinstance(data, str):
        data = data.encode(encoding)
    _hexdump(data)

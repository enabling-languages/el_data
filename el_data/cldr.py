import icu as _icu
import xml.etree.ElementTree as _ET
import requests as _requests

def get_exemplars(locale_id: str, use_sldr: bool = False) -> dict[str, str]:
    locale_id = locale_id.replace('-', '_')
    exemplar_data = dict()
    url = rf'https://raw.githubusercontent.com/unicode-org/cldr/main/common/main/{locale_id}.xml'
    if use_sldr:
        initial_letter = locale_id[0]
        url = rf'https://raw.githubusercontent.com/silnrsi/sldr/refs/heads/master/sldr/{initial_letter}/{locale_id}.xml'
    response = _requests.get(url)
    if response.status_code not in (404, 500):
        tree = _ET.fromstring(response.text)
        result = tree.findall('characters/exemplarCharacters')
        for element in result:
            type = element.attrib.get('type', 'main')
            if type not in ["numbers", "punctuation"]:
                if element.text and element.text != '↑↑↑':
                    exemplar_data[type] = _icu.UnicodeSet(rf'{element.text}')
        return exemplar_data
    return None

class CLDR():
    def __init__(self, locale_id:str, use_sldr: bool = False):
        self._locale_id = locale_id.replace('-', '_')
        self._use_sldr = use_sldr
        self._ldml = self._main_ldml()
        self._ld = _icu.LocaleData(self._locale_id)

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(locale_id={self._locale_id}, use_sldr={self._use_sldr})"

    def _main_ldml(self):
        url = rf'https://raw.githubusercontent.com/unicode-org/cldr/main/common/main/{self._locale_id}.xml'
        if self._use_sldr:
            initial_letter = self._locale_id[0]
            url = rf'https://raw.githubusercontent.com/silnrsi/sldr/refs/heads/master/sldr/{initial_letter}/{self._locale_id}.xml'
        response = _requests.get(url)
        if response.status_code not in (404, 500):
            tree = _ET.fromstring(response.text)
            return tree
        return None

    def _other_ldml(self, url):
        response = _requests.get(url)
        if response.status_code not in (404, 500):
            tree = _ET.fromstring(response.text)
            return tree
        return None

    def get_exemplars(self):
        exemplar_data = dict()
        tree = self._ldml
        if tree is not None:
            result = tree.findall('characters/exemplarCharacters')
            for element in result:
                type = element.attrib.get('type', 'main')
                if type not in ["numbers", "punctuation"]:
                    if element.text and element.text != '↑↑↑':
                        exemplar_data[type] = _icu.UnicodeSet(rf'{element.text}')
            return exemplar_data
        return None

    def get_main_exemplars(self, mode='uset'):
        tree = self._ldml
        if tree is not None:
            result = tree.findall('characters/exemplarCharacters')
            for element in result:
                type = element.attrib.get('type', 'main')
                if type == "main" and element.text and element.text != '↑↑↑':
                    data = _icu.UnicodeSet(rf'{element.text}')
                    match mode:
                        case 'list':
                            return list(data)
                        case 'pattern':
                            return data.toPattern()
                        case '_':
                            return data
        return None

import jprops
import os
import re

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class I18n:

    languages = {}
    supportedLanguages = ['de', 'en']

    class __I18n:
        def __init__(self):
            work_dir = os.path.join(os.path.dirname(__file__), '..', 'res', 'i18n')
            for lang in I18n.supportedLanguages:
                file = 'KortDB_'+lang+'.props'
                with open(os.path.join(work_dir, file)) as fp:
                    props = jprops.load_properties(fp)
                    I18n.languages[lang] = props

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not I18n.instance:
            I18n.instance = I18n.__I18n()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def match_language(self, lang):
        if lang in I18n.supportedLanguages:
            return lang
        else:
            part = lang.split('-')[0]
            if part in I18n.supportedLanguages:
                return part
        return 'en'

    def translate_list(self, lang, list_of_values):
        for index, item in enumerate(list_of_values):
            list_of_values[index] = self.translate(lang, list_of_values[index])
        return list_of_values

    def translate(self, lang, key):
        try:
            val = self.languages[lang][key]
            return val
        except KeyError:
            return key

    def translate_question(self, lang, question, txt1, txt2, txt3, txt4, txt5):
        translated_question = self.translate(lang, question)
        if not txt1 and '$1' not in translated_question:
            return translated_question
        else:
            rep = {'$1': self.translate_place(lang, txt1), '$2': self.translate(lang, txt2),
                   '$3': self.translate(lang, txt3), '$4': self.translate(lang, txt4),
                   '$5': self.translate(lang, txt5)}
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            return pattern.sub(lambda m: rep[re.escape(m.group(0))], translated_question)

    def translate_place(self, lang, place):
        name = self.translate(lang, place)
        if name:
            return name
        else:
            return self.translate(lang, 'this.place')

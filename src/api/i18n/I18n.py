import jprops
import os
import re

class I18n:

    languages = {}
    supportedLanguages = ['de', 'en']

    class __I18n:
        def __init__(self):
            dir = os.path.join(os.path.dirname(__file__),'..','..','..','i18n')
            for lang in I18n.supportedLanguages:

                with open(os.path.join(dir, 'KortDB_'+lang+'.props')) as fp:
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


    def matchLanguage(self, lang):
        if (lang in I18n.supportedLanguages):
            return lang
        else:
            part = lang.split('-')[0]
            if (part in I18n.supportedLanguages):
                return part
        return 'en'


    def translateList(self, lang, list):
        for index, item in enumerate(list):
            list[index] = self.translate(lang, list[index])
        return list


    def translate(self, lang, key):
        try:
            val = self.languages[lang][key]
            return val
        except KeyError:
            return key

    def translateQuestion(self, lang, question, txt1, txt2, txt3, txt4, txt5):
        translated_question = self.translate(lang, question)
        if (not txt1):
            return translated_question
        else:
            rep = {'$1' : self.translate(lang, txt1), '$2' : self.translate(lang, txt2),
                   '$3' : self.translate(lang, txt3), '$4' : self.translate(lang, txt4),
                   '$5' : self.translate(lang, txt5)}
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            return pattern.sub(lambda m: rep[re.escape(m.group(0))], translated_question)


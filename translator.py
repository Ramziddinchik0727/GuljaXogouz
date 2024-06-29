from translate import Translator

def translate_uz_to_ru(text):
    translator = Translator(from_lang="uz", to_lang="ru")
    translation = translator.translate(text=text)
    return translation

def translate_uz_to_en(text):
    translator = Translator(from_lang="uz", to_lang="en")
    translation = translator.translate(text=text)
    return translation

def translate_uz_to_zh(text):
    translator = Translator(from_lang="uz", to_lang="zh")
    translation = translator.translate(text=text)
    return translation

def translations(text):
    return [translate_uz_to_en(text), translate_uz_to_ru(text), translate_uz_to_zh(text)]

# def translate_ru_to_uz(text):
#     translator = Translator(from_lang='ru', to_lang='uz')
#     translation = translator.translate(text=text)
#     return translation
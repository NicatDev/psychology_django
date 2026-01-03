from modeltranslation.translator import translator, TranslationOptions
from .models import About, ContactInfo, Plan, Tag, Blog

class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'miniTitle', 'content')

class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('location',)

class PlanTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description')

class TagTranslationOptions(TranslationOptions):
    fields = ('name',)

class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

translator.register(About, AboutTranslationOptions)
translator.register(ContactInfo, ContactInfoTranslationOptions)
translator.register(Plan, PlanTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(Blog, BlogTranslationOptions)

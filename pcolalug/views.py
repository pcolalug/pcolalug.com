from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('pcolalug')

def my_view(request):
    return {'project':'pcolalug'}

import deform

class UNIForm(deform.Form):
    def __init__(self, *args, **kwargs):
        kwargs['css_class'] = 'uniForm'

        if not kwargs.get('buttons'):
            kwargs['buttons'] = ('submit', )

        super(UNIForm, self).__init__(*args, **kwargs)

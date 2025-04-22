# widgets.py
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True

    def format_value(self, value):
        # Return value from a list of files
        if value:
            return value
        return []
from wtforms import fields
from wtforms.compat import text_type


class ValueListField(fields.StringField):
    """
    List of values.

    For example, can be used to enumerate tags or scope for a REST API client.

    Parameters:
        label (str): The label of the field.
        separator (str): Separator character for values.
        coerce (callable): Callback to explicitly cast each value to the desired data type.
    """
    def __init__(self, label=None, separator=',', coerce=text_type, **kwargs):
        super().__init__(label, **kwargs)
        self.separator = separator
        self.coerce = coerce
        self.data = ()

    def _value(self):
        return self.separator.join(str(v) for v in self.data)

    def process_data(self, value):
        try:
            self.data = tuple(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = ()

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = tuple(self.coerce(v.strip()) for v in valuelist[0].split(self.separator))

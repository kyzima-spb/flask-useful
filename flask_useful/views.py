from flask import views
from flask import render_template

from .utils import camel_to_list


class MethodView(views.MethodView):
    """
    Arguments:
        template_name (:obj:`str`):
            The name of the template, can be passed to the :py:meth:`~flask.views.View.as_view` method.

    Attributes:
        template_name (:obj:`str`): The name of the template.
    """

    template_name = None

    def __init__(self, template_name=None):
        if template_name:
            self.template_name = template_name

    def get_template_name(self):
        """
        Returns the name of the template.

        If the template_name property is not set, the value will be generated automatically based on the class name.

        Example:
            >>> class MyEntityAction(MethodView): pass
            >>> view = MyEntityAction()
            >>> view.get_template_name()
            "my_entity/action.html"

        """
        if self.template_name is None:
            name = camel_to_list(self.__class__.__name__, lower=True)
            self.template_name = '{1}/{0}.html'.format(name.pop(), '_'.join(name))
        return self.template_name

    def render_template(self, **context):
        """Render a template with passed context."""
        return render_template(self.get_template_name(), **context)

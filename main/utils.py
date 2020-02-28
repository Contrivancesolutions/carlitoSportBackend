from django.contrib import messages
from django.views.generic.edit import FormView


class FormErrorsView(FormView):

    def form_invalid(self, form):
        errors = [item for sublist in form.errors.values() for item in sublist]
        if len(errors) != 1:
            form_msg = "<ul>"
            for error in errors:
                form_msg += f"<li>{error}</li>"
            form_msg += "</ul>"
        else:
            form_msg = errors[0]
        messages.error(self.request, form_msg)
        return super().form_invalid(form)

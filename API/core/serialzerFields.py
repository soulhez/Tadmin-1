from rest_framework.serializers import HiddenField,empty
class CurrentAdminUserHiddenField(HiddenField):
    """
    A hidden field does not take input from the user, or present any output,
    but it does populate a field in `validated_data`, based on its default
    value. This is particularly useful when we have a `unique_for_date`
    constraint on a pair of fields, as we need some way to include the date in
    the validated data.
    """
    def __init__(self, **kwargs):
        assert 'default' in kwargs, 'default is a required argument.'
        kwargs['write_only'] = True
        super(HiddenField, self).__init__(**kwargs)

    def get_value(self, dictionary):
        # We always use the default value for `HiddenField`.
        # User input is never provided or accepted.
        request=self.context['request']
        return request.user

    def to_internal_value(self, data):
        return data
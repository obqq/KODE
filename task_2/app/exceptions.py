class ValidationError(ValueError):
        def __init__(self, message='', *args, **kwargs):
            ValueError.__init__(self, message, *args, **kwargs)

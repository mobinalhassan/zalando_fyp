

class ServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        if not self._instance:
            self._instance = self.build(**kwargs)
        return self._instance

    def build(self, **kwargs):
        """override"""
        raise NotImplemented()


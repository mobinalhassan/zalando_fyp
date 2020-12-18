from snapthat.builder import ServiceBuilder


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)

        if isinstance(builder, ServiceBuilder):
            return builder.build(**kwargs)

        return builder(**kwargs)

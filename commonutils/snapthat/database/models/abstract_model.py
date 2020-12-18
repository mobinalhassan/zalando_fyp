from abc import ABC, abstractmethod
from snapthat.config import Printable
from snapthat.database.models.indexing import DatabaseIndex


class AbstractDBModel(ABC, Printable):
    def __init__(self):
        pass


    @abstractmethod
    def is_valid(self):
        """checks if the current model is in valid state
        Return:
            bool: valid or invalid
        """
        return False

    @abstractmethod
    def required(self):
        """return the list of required fields by the object
        Returns:
            list[str]: returns a list of required field names
        """
        return []

    @abstractmethod
    def indexes(self):
        """return the list of all indexes used in the model
        Returns:
            list[DatabaseIndex]: returns a list of indexes of type DatabaseIndex

        """
        return []

    # @abstractmethod
    # def unique(self):
    #     """return the list of unique fields in the model
    #     Returns:
    #         list[str]: returns a list of unique field names
    #     """
    #     return []

    @abstractmethod
    def ignore(self):
        """return the list of fields to be ignored for preprocessing
        Returns:
            list[str]: returns a list of field names that are ignored from pre processing
        """
        return []
    #
    # def get_fields(self):
    #     """Gathers different fields info and returns field objects
    #
    #     Returns:
    #         dict: returns dictionary mapping of field_name: Fields()
    #     """
    #
    #     field_mapping = {}
    #     original_fields = dict(self.__class__()).keys()
    #     model = dict(self)
    #     for field in original_fields:
    #         val = model.get(field, None)
    #         f = Field(val)
    #
    #         if val is not None:
    #             f.type = val.__class__
    #
    #         if field in self.required():
    #             f.required = True
    #
    #         if field in self.unique():
    #             f.unique = True
    #
    #         field_mapping[field] = f
    #
    #     return field_mapping

    @abstractmethod
    def preprocess(self):
        """preprocesses the fields value. example converting them to lowercase. trimming etc.
        Returns:
            None: modifies inplace
        """
        return None

    def update(self, obj):
        """updates the model using the provided object
        obj (dict): obj of type dictionary
        """
        obj = dict(obj)
        keys = dict(self).keys()
        for key in keys:
            val = obj.get(key, None)
            if val is not None:
                setattr(self, key, val)


        return self


    def validate_fields(self):
        model = dict(self)

        original = self.__class__
        original_obj = dict(original())

        error_messages = []

        for key, value in model.items():
            val_orig= original_obj.get(key, None)

            if val_orig is None:
                error_messages.append(f"Key `{key}` not found in original model")
                continue

            if not isinstance(value, val_orig.__class__):
                error_messages.append(f"Expected type `{val_orig.__class__}` got `{value.__class__}` for key `{key}`")
                continue

        if len(error_messages) > 0:
            error_message = "\n".join(error_messages)
            error_message = "There were some error(s) in your model : \n" + error_message

            raise Exception(error_message)

        return self


    def validate_required(self):
        model = dict(self)

        required_fields = self.required()
        assert isinstance(required_fields, list), \
            f"required fields must be a list but {type(required_fields)} given"

        original = self.__class__
        original_obj = dict(original())
        original_keys = original_obj.keys()

        error_messages = []

        for r_field in required_fields:
            if r_field not in original_keys:
                error_messages.append(f"`{r_field}` not in original model fields")
                continue

            value = model.get(r_field)
            if value == "" or value is None:
                error_messages.append(f"{r_field} is required, provided `{value}`")

        if len(error_messages) > 0:
            error_msg = "\n".join(error_messages)
            error_msg = "Required validation failed: \n" + error_msg
            raise Exception(error_msg)

        return self

    def _preprocess(self):
        model = dict(self)

        for k, v in model.items():
            if k in self.ignore():
                continue
            if isinstance(v, str):
                v = (v.encode('ascii', 'ignore')).decode("utf-8")
                v = v.strip(" ")
                v = v.lower()
                self.update({k: v})

        return self

    def validate(self):
        self.validate_fields()
        self.validate_required()

        if not self.is_valid():
            raise Exception(f"Model is not in a valid state. check custom validation rules")

        return self

    def preprocess_and_validate(self):
        self._preprocess()
        self.preprocess()
        self.validate()

        return self



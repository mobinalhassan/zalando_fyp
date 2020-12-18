from snapthat.database.models.abstract_model import AbstractDBModel
from datetime import datetime
from snapthat.networkrequests.networkutils import format_url
from snapthat.database.models.indexing import FieldIndex, CompositeIndex, IndexOrder


class BrandModel(AbstractDBModel):
    def __init__(self):
        super().__init__()

        self.brand_ref = ""
        self.brand_title = ""
        self.brand_representative = ""
        self.brand_name = ""
        self.brand_heading = ""
        self.brand_tagline = ""
        self.brand_description = ""
        self.brand_logo = ""
        self.brand_banner = ""
        self.brand_url = ""
        self.brand_keywords = []
        self.brand_unique_content = ""
        self.brand_seo_content = ""
        self.brand_philosophy = ""
        self.partnership_flag = False
        self.total_skus = 0
        self.password = ""
        self.email = ""
        self.accessToken = ""
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def check_list_of_strings(self, fields):
        model = dict(self)
        for field in fields:
            v = model[field]
            if isinstance(v, list):
                for item in v:
                    if not isinstance(item, str):
                        raise Exception(f"Field `{field}` with value {item} is not a string, given {type(item)}")

    def is_valid(self):
        self.check_list_of_strings(self.brand_keywords)

        return True

    def preprocess(self):
        self.brand_url = format_url(self.brand_url)
        self.brand_logo = format_url(self.brand_logo)
        self.brand_banner = format_url(self.brand_banner)
        return None

    def required(self):
        return ['brand_name']

    def indexes(self):
        email_pass_composite = CompositeIndex()
        email_pass_composite.add_field("email", IndexOrder.DESCENDING)
        email_pass_composite.add_field("password", IndexOrder.ASCENDING)

        created_updated_comp  = CompositeIndex()
        created_updated_comp.add_field("created_at", IndexOrder.DESCENDING)
        created_updated_comp.add_field("updated_at", IndexOrder.DESCENDING)

        return [FieldIndex("brand_name", unique=True), FieldIndex("accessToken"), email_pass_composite,
                FieldIndex("created_at"), FieldIndex("updated_at"), created_updated_comp]

    def ignore(self):
        return ["password", "email", "accessToken", "brand_url", "brand_tagline",
                "brand_heading", "brand_logo", "brand_banner", "brand_philosophy"]

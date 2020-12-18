from snapthat.database.models.abstract_model import AbstractDBModel
from datetime import datetime
from snapthat.networkrequests.networkutils import format_url
from snapthat.database.models.indexing import FieldIndex, CompositeIndex, IndexOrder


class BrandClothModel(AbstractDBModel):
    def __init__(self):
        super().__init__()
        self.brand_id = ""
        self.brand_name = ""
        self.designer = ""
        self.title = ""
        self.sku = ""
        self.description = ""
        self.price = -1
        self.currency = "default"
        self.quantity = 1  # TODO: change this to int, sync with backend
        self.prodId = ""
        self.source = ""
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.availability = False
        self.images_saved = False
        self.indexed = False
        self.thumbnail = ""
        self.frontpic = ""
        self.backpic = ""
        self.leftpic = ""
        self.rightpic = ""
        self.zoomedpics = []
        self.otherpics = []
        self.fabric = ""
        self.fabric_lining = ""
        self.fabric_care = ""
        self.material = ""
        self.stitched = True
        self.gender = ""
        self.agebracket = ""
        self.fittingtype = ""
        self.checkoutsource = ""  # buy link
        self.latitude = 0.0
        self.longitude = 0.0
        self.season = ""
        self.colors = []
        self.processed_colors = []
        self.wheretowear = ""
        self.dresstype = ""  # shirt, pant
        self.dresssubtype = ""  # shirt_type, pant_type
        self.fashionoutlook = ""  # example: sporty, chick , cool
        self.designPattern = ""  # example: circles, waves, checkered, lining, polkadots etc
        self.texture = ""  # might be a texture link
        self.dressattributes = []
        self.dressdecorations = []
        self.dresstags = []  # TODO: change this to a list, sync with backend
        self.processed_dresstags = []
        self.faceflags = []  # TODO: change this to a list, sync with backend
        self.facecolors = []
        self.haircolors = []
        self.processed_haircolors = []
        self.isscrapped = False
        self.sizes = []  # available sizes
        self.model_body_type = ""
        self.model_body_height = ""
        self.model_cloth_size = ""

    def check_list_of_strings(self, fields):
        model = dict(self)
        for field in fields:
            v = model[field]
            if isinstance(v, list):
                for item in v:
                    if not isinstance(item, str):
                        raise Exception(f"Field `{field}` with value {item} is not a string, given {type(item)}")

    def is_valid(self):
        if float(self.price) <= 0:
            raise Exception(f'Price must be greater than 0, given: {self.price} ')

        if int(self.quantity) < 0:
            raise Exception(f'Quantity must be greater than 0, given: {self.quantity} ')

        allowed_gender = ['male', 'female', 'unisex']
        if self.gender not in allowed_gender:
            raise Exception(f'Gender must be among {allowed_gender}, given {self.gender}')

        allowed_agebracket = ['', 'infants', 'kids', 'teens', 'young', 'adults', 'elders']

        if self.agebracket not in allowed_agebracket:
            raise Exception(f'Age bracket must be among {allowed_agebracket}, given `{self.agebracket}`')

        allowed_sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl']
        for size in self.sizes:
            if size not in allowed_sizes:
                raise Exception(f'Sizes must be among {allowed_sizes}, given {size}')

        self.check_list_of_strings(
            ['zoomedpics', 'otherpics', 'colors', 'processed_colors', 'dressattributes', 'dressdecorations',
             'dresstags', 'processed_dresstags', 'faceflags',
             'facecolors', 'haircolors', 'processed_haircolors'])

        return True

    def preprocess(self):
        if self.images_saved:
            return

        self.frontpic = format_url(self.frontpic)
        self.backpic = format_url(self.backpic)
        self.leftpic = format_url(self.leftpic)
        self.rightpic = format_url(self.rightpic)
        self.backpic = format_url(self.backpic)
        self.checkoutsource = format_url(self.checkoutsource)

        for i, val in enumerate(self.zoomedpics):
            self.zoomedpics[i] = format_url(val)

        for i, val in enumerate(self.otherpics):
            self.otherpics[i] = format_url(val)

        return None

    def required(self):
        return ['brand_id', 'gender', 'availability', 'price', 'title', 'thumbnail']

    def indexes(self):
        brand_prodid_composite = CompositeIndex(unique=True)
        brand_prodid_composite.add_field('brand_id', IndexOrder.DESCENDING)
        brand_prodid_composite.add_field('prodId', IndexOrder.DESCENDING)

        lat_lng_comp = CompositeIndex()
        lat_lng_comp.add_field('latitude', IndexOrder.DESCENDING)
        lat_lng_comp.add_field('longitude', IndexOrder.ASCENDING)

        created_updated_comp  = CompositeIndex()
        created_updated_comp.add_field("created_at", IndexOrder.DESCENDING)
        created_updated_comp.add_field("updated_at", IndexOrder.DESCENDING)

        return [FieldIndex("brand_id"), brand_prodid_composite, FieldIndex('title'),lat_lng_comp,
                FieldIndex("price"), FieldIndex("gender"), FieldIndex("quantity"), FieldIndex("season"),
                FieldIndex("availability"), FieldIndex("created_at"), FieldIndex("updated_at"),
                FieldIndex("images_saved"), FieldIndex("indexed"), created_updated_comp]

    def ignore(self):
        return ['currency', 'thumbnail', 'frontpic', 'backpic', 'leftpic', 'rightpic',
                'checkoutsource', 'zoomedpics', 'otherpics']

from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

class FidelityProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_link_in = MapCompose(lambda x: 'https://www.fidelity.co.uk' + x)
    Description_in = MapCompose(lambda x: x.replace("\"", "").replace("\xa0", "").strip())
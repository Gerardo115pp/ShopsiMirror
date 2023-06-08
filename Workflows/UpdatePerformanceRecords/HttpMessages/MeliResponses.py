from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MeliItemAttribute:
    id: str
    name: str
    attribute_value: str
    
    @staticmethod
    def fromDict(d: Dict) -> 'MeliItemAttribute':
        return MeliItemAttribute(id=d['id'], name=d['name'], attribute_value=d['value_name'])
    
@dataclass
class MeliItemData:
    
    id: str
    site_id: str
    title: str
    subtitle: str
    category_id: str
    price: float
    base_price: float
    original_price: float
    currency: str
    available_quantity: int
    buying_mode: str
    listing_type_id: str
    start_time: str
    stop_time: str
    condition: str
    permalink: str
    thumbnail: str
    secure_thumbnail: str
    accepts_mercadopago: bool
    has_free_shipping: bool
    seller_address: str
    status: str
    sub_status: str
    domain_id: str
    catalog_product_id: str
    date_created: str
    last_updated: str
    health: str
    tags: List[str]
    attributes: List[MeliItemAttribute]
    
    
    @staticmethod
    def fromDict(d: dict) -> 'MeliItemData':
        _has_free_shipping: bool = False
        _seller_address: str = ""
        _sub_status: str = ""
        _attrubutes: List[MeliItemAttribute] = []
        
        
        if d["status"] != "under_review":
            _has_free_shipping:bool = d.get('shipping', {}).get('free_shipping', False)
            _seller_address:str = f"{d.get('seller_address', {}).get('city', 'no_city')}, {d.get('seller_address', {}).get('state', 'no_state')}, {d.get('seller_address', {}).get('country', 'no_country')}"
            _sub_status:str = ""
        
            if len(d.get('sub_status', [])) > 0:
                _sub_status:str = d["sub_status"][0]
            
            _attrubutes:List[MeliItemAttribute] = [MeliItemAttribute.fromDict(a) for a in d.get('attributes', [])]

            
        return MeliItemData(
            id=d.get('id', ''),
            site_id=d.get('site_id', ''),
            title=d.get('title', ''),
            subtitle=d.get('subtitle', ''),
            category_id=d.get('category_id', ''),
            price=d.get('price', 0.0),
            base_price=d.get('base_price', 0.0),
            original_price=d.get('original_price', 0.0),
            currency=d.get('currency', ''),
            available_quantity=d.get('available_quantity', 0),
            buying_mode=d.get('buying_mode', ''),
            listing_type_id=d.get('listing_type_id', ''),
            start_time=d.get('start_time', ''),
            stop_time=d.get('stop_time', ''),
            condition=d.get('condition', ''),
            permalink=d.get('permalink', ''),
            thumbnail=d.get('thumbnail', ''),
            secure_thumbnail=d.get('secure_thumbnail', ''),
            accepts_mercadopago=d.get('accepts_mercadopago', False),
            has_free_shipping=_has_free_shipping,
            seller_address=_seller_address,
            status=d.get('status'),
            sub_status=_sub_status,
            domain_id=d.get('domain_id', ''),
            catalog_product_id=d.get('catalog_product_id', ''),
            date_created=d.get('date_created', ''),
            last_updated=d.get('last_updated', ''),
            health=d.get('health', ''),
            tags=d.get('tags', []),
            attributes=_attrubutes
        )
    
    
    
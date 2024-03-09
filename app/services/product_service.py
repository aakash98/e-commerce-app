from app.models import Product

class ProductService:

    @classmethod
    def get_all_products(cls, is_active=True):
        result = Product.objects()
        return result

    @classmethod
    def create_new_product(cls, data):
        product = Product(**data)
        product.save()
        return product

    @classmethod
    def get_by_id(cls, product_id):
        product = Product.objects(id=product_id).first()
        return product

    @classmethod
    def update_product(cls, product_id, **kwargs):
        kwargs.pop('_id', None)
        product = cls.get_by_id(product_id)
        if product:
            product.update(**kwargs)
            product.save()
            return product, True
        else:
            return None, False

    @classmethod
    def delete_product(cls, product_id):
        product = cls.get_by_id(product_id)
        if product:
            product.delete()
            return True
        return False
from .feature_builder import FeatureBuiler


PRODUCT_REQUESTS = FeatureBuiler(
    name="Product Requests",
    description="Allow users request products by sending emails",
    access_levels=['admin'],
    free_quota=10
)
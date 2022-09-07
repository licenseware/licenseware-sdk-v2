from licenseware.feature_builder.feature_builder import FeatureBuilder

PRODUCT_REQUESTS = FeatureBuilder(
    name="Product Requests",
    description="Allow users request products by sending emails",
    access_levels=["admin"],
    monthly_quota=10,
)

from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage

# Media files storage
class MediaStorage(GoogleCloudStorage):
    bucket_name = getattr(settings, "GS_BUCKET_NAME", None)
    location = "media"
    if getattr(settings, "GS_CREDENTIALS", None) is not None:
        credentials = settings.GS_CREDENTIALS
    default_acl = "publicRead"

# Static files storage
class StaticStorage(GoogleCloudStorage):
    bucket_name = getattr(settings, "GS_BUCKET_NAME", None)
    location = "static"
    if getattr(settings, "GS_CREDENTIALS", None) is not None:
        credentials = settings.GS_CREDENTIALS
    default_acl = "publicRead"
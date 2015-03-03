from django.contrib.staticfiles.storage import CachedFilesMixin

from pipeline.storage import PipelineMixin

from s3_folder_storage.s3 import StaticStorage


class S3PipelineStorage(PipelineMixin, CachedFilesMixin, StaticStorage):
    pass

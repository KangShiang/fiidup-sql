import utils
import urlparse
import blobsDownHandler
from google.appengine.ext.webapp import blobstore_handlers

class BlobsDown(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        blobsDownHandler.get_blobsDown(self, resource)

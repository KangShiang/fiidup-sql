import webapp2
import urllib
from google.appengine.ext import blobstore

def get_blobsDown(handler, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    handler.send_blob(blob_info)

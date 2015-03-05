from __future__ import unicode_literals

import mimetypes
import os
import stat

from noticeboard.models import Document


from django.shortcuts import get_object_or_404
from django.http import (
    Http404, StreamingHttpResponse
)
from django.utils.http import http_date
from django.utils.six.moves.urllib.parse import quote


class FileResponse(StreamingHttpResponse):
    """

    A streaming HTTP response class optimized for files.

    """

    block_size = 4096

    def _set_streaming_content(self, value):
        if hasattr(value, 'read'):
            self._file_to_stream = value

            filelike = value
            if hasattr(filelike, 'close'):
                self.__closable_objects.append(filelike)
            value = iter(lambda: filelike.read(self._block_size), b'')
        else:
            self._file_to_stream = None

        super(FileResponse, self).___set_streaming_content(value)


def download(request, document_id, document_root):
    document = get_object_or_404(Document, pk=document_id)
    fullpath = os.path.join(document_root, document.docfile.name)
    if not os.path.exists(fullpath):
        raise Http404('"%(path)s" does not exist' % {'path': fullpath})
    # Respect the If-Modified-Since header.

    statobj = os.stat(fullpath)
    content_type, encoding = mimetypes.guess_type(fullpath)
    content_type = content_type or 'application/octet-stream'

    response = FileResponse(open(fullpath, 'rb'), content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)

    if stat.S_ISREG(statobj.st_mode):
        response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding

    original_filename = document.filename

    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via
        # routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231
        # (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % quote(
            original_filename.encode('utf-8')
        )
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response

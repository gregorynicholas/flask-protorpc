from json import loads
from ..rpc import proto
from ..api.rpc import RemoteResponse
from functools import wraps

class RpcMixin:
  def options(self, svc, *args, **kw):
    """Like open but method is enforced to OPTIONS. This is mainly to extend
    the :class:`werkzeug.test.Client` to provide a method for working with
    XMLHttpRequests."""
    kw['method'] = 'OPTIONS'
    return svc.test_client().open(*args, **kw)

  def send_rpc(self, svc, path, data, **kw):
    '''
    :param path: the path of the request.  In the WSGI environment this will
                 end up as `PATH_INFO`.  If the `query_string` is not defined
                 and there is a question mark in the `path` everything after
                 it is used as query string.
    :param base_url: the base URL is a URL that is used to extract the WSGI
                     URL scheme, host (server name + server port) and the
                     script root (`SCRIPT_NAME`).
    :param query_string: an optional string or dict with URL parameters.
    '''
    svc.response_class = RemoteResponse
    response = svc.test_client().post(path=path, follow_redirects=True,
      data=data, content_type='application/json', headers={
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      # for mimicing jquery ajax requests..
      'X-Requested-With': 'XMLHttpRequest',
    })
    self.assertTrue((response.data and len(response.data) > 0),
      'Call to: "%s" returned no response data.' % (path))
    return response, loads(response.data)

def remote(request_msg, response_msg):
  def wrapper(f):
    @wraps(f)
    def decorated(self, msg, *args, **kw):
      response, data = f(self, data=proto.message_to_json(msg), *args, **kw)
      return response, proto.message_from_json(response_msg, data)
    return decorated
  return wrapper

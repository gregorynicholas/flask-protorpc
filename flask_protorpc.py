"""
  flask_protorpc
  ~~~~~~~~~~~~~~~~~

  An extremely thin Flask Extension to build remote clients.

  :copyright: (c) 2012 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
import logging
from json import dumps, loads
from flask import Response, request
from werkzeug import exceptions
from functools import wraps
from protorpc import messages
from protorpc import protojson
from protorpc.message_types import VoidMessage

__all__ = ['messages', 'message_to_json', 'message_to_json_str',
'message_from_json', 'protojson', 'OPTIONS', 'VoidMessage',
'RemoteResponse', 'remote', 'remote_request']


class RequestDataError(ValueError):
  pass

class ResponseDataError(ValueError):
  pass

class MimeTypeError(ValueError):
  pass

class ContentTypeError(ValueError):
  pass

class JsonValueError(ValueError):
  pass


def message_to_json(message):
  '''Returns an instance of an encoded json string.

    :param message: Instance of a response protorpc `Message`.
  '''
  if not isinstance(message, messages.Message):
    raise ValueError('Value must be an instance of messages.Message.')
  return protojson.encode_message(message)

def message_to_dict(message):
  '''Returns an instance of an encoded json string.

    :param message: Instance of a response protorpc `Message`.
  '''
  if not isinstance(message, messages.Message):
    raise ValueError('Value must be an instance of messages.Message.')
  return loads(protojson.encode_message(message))

def message_to_json_str(message):
  '''
    :param message: Instance of a response protorpc `Message`.
  '''
  if not isinstance(message, messages.Message):
    raise ValueError('Value must be an instance of messages.Message.')
  return dumps(message_to_json(message))

def message_from_json(message_type, value):
  '''Returns an instance of a protorpc `Message` class.

    :param message_type: Protorpc `Message` class.
    :param value: JSON string to decode to a `Message`.
  '''
  if isinstance(value, str):
    value = value
  elif isinstance(value, dict):
    value = dumps(value)
  else:
    raise JsonValueError('Value must be a json str or dict.')
  return protojson.decode_message(message_type, value)


OPTIONS = ['OPTIONS', 'HEAD', 'GET', 'POST', 'PUT']
MIMETYPE = 'application/json'
HEADERS = ['Accept', 'Content-Type', 'Origin', 'X-Requested-With']


class RemoteResponse(Response):
  '''Base class for remote service `Response` objects.'''
  default_mimetype = MIMETYPE
  def __init__(self, response=None, mimetype=None, *args, **kw):
    if mimetype is None:
      mimetype = self.default_mimetype
    Response.__init__(self, response=response, mimetype=mimetype, **kw)
    self._fixcors()

  def _fixcors(self):
    self.headers['Access-Control-Allow-Origin'] = '*'
    self.headers['Access-Control-Allow-Methods'] = ', '.join(OPTIONS)
    self.headers['Access-Control-Allow-Headers'] = ', '.join(HEADERS)


class ResponseMessage(messages.Message):
  msg = messages.StringField(1, default='ok')
  status = messages.IntegerField(2, default=200)


def remote_request(response_msg=None):
  '''Method decorator wraps a function that returns a `dict`, and returns a
  serialized response message.

    :param response_msg: Protorpc `Message` class of the func's return object.
  '''
  def wrapper(func):
    @wraps(func)
    def decorated(*args, **kw):
      value = func(*args, **kw)
      if isinstance(value, dict):
        value = message_from_json(response_msg, value)
      return value
    return decorated
  return wrapper

def remote(request_msg=None, response_msg=None, payload=False):
  '''Method decorator wraps a view function and returns a serialized json
  message.

    :param request_msg: Protorpc `Message` class of the view's request object.
    :param response_msg: Protorpc `Message` class of the view's response object.
    :param payload: Will attempt to parse the message from the request payload.
  '''
  def wrapper(remotemethod):
    @wraps(remotemethod)
    def decorated(*args, **kw):
      if request.method == 'OPTIONS':
        return RemoteResponse('', mimetype='text/plain')
      # try to parse the request message data..
      reqmsg = None
      resmsg = None
      try:
        reqmsg = _validate_msg(parse_request_msg(request_msg, payload=payload))
      except Exception, e:
        resmsg = ResponseMessage(
          status=400,
          msg="Error with rpc request: %s" % str(e).replace('"', '\"'))
        logging.error(repr(resmsg))
      # try to generate and parse the response data..
      if reqmsg:
        try:
          resmsg = remotemethod(msg=reqmsg, *args, **kw)
        # handle werkzeug.HTTPExceptions..
        except exceptions.HTTPException, e:
          resmsg = ResponseMessage(
            status=e.code,
            msg="Error with remote call: %s" % e.description.replace('"', '\"'))
          logging.exception(repr(resmsg))
        except Exception, e:
          resmsg = ResponseMessage(
            status=500,
            msg="Exception in remote call: %s" % str(e).replace('"', '\"'))
          logging.exception(repr(resmsg))
      return RemoteResponse(message_to_json(resmsg))
    return decorated
  return wrapper


def _validate_msg(msg):
  '''
    :param msg: Instance of a response protorpc `Message`.
  '''
  if not msg or not isinstance(msg, messages.Message):
    raise ResponseDataError(
      'Remote Method did not return a valid response message.')
  return msg

def parse_request_msg(message_type, payload=False):
  '''Parses the request parameters from either the querystring if the method
  is GET, or the request body if the method is POST..

    :param message_type: Protorpc `Message` class.
  '''
  # def _validate_request():
  #   if MIMETYPE not in request.accept_mimetypes:
  #     raise MimeTypeError(
  #       'Request did not accept json mimetype: %s' % (request.accept_mimetypes))
  # _validate_request()
  _value = None
  if request.method == 'GET':
    # parse request values from the querystring..
    _value = request.args.to_dict()
  elif request.method == 'POST':
    if payload:
      # todo: pretty hacky..
      _value = {'payload': loads(request.form.get('payload', '{}'))}
    # parse request values from form variables..
    elif 'application/x-www-form-urlencoded' in request.content_type:
      # logging.error('parsing request from x-www-form-urlencoded.')
      _value = request.form.to_dict()
    elif 'application/json' in request.content_type:
      # parse request values from request body (expects a json string)..
      # logging.error('parsing request from application/json request body.')
      if not request.data:
        raise RequestDataError('No data sent in the request body.')
      _value = request.data
    else:
      raise ValueError('Unknown content-type request header.')
  try:
    return message_from_json(message_type, _value)
  except (messages.ValidationError), e:
    raise RequestDataError('Error parsing the %s rpc request: "%s" from %s' % (
      request.method, e.message, request.url))
  except (AttributeError, ValueError), e:
    logging.error(
      'Exception serializing the request data: Error: %s\nData:\n%s', e, _value)
    raise RequestDataError('Error parsing the request to rpc: "%s"', _value)


from threading import RLock
from werkzeug.utils import cached_property
class cached(cached_property):
  """A decorator that converts a function into a lazy property.

  This class was ported from `Werkzeug`_ and adapted to provide threadsafety.
  """
  def __init__(self, *args, **kw):
    cached_property.__init__(self, *args, **kw)
    self.lock = RLock()

  def __get__(self, *args, **kw):
    with self.lock:
      return cached_property.__get__(self, *args, **kw)

import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

RETRY_CODES = (500, 503, 409)
REQUEST_TIMEOUT = 120
BACKOFF_FACTOR = 1
RETRY_TIMES = 3


class BaseAPITClient(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log_response(self, response, verbose=True):
        request_id = response.headers.get("x-request-id")
        self.logger.debug("Response request id: {}".format(request_id))
        self.logger.debug(f"Response status code: <{response.status_code}>")
        if verbose:
            self.logger.debug(f"Response content: {response.content}")

    def post(self, resource: str, api_key=None, api_id=None, verbose=True, **kwargs):
        headers = {}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        if api_id is not None:
            headers["X-API-ID"] = api_id
        if headers:
            if "headers" in kwargs:
                kwargs["headers"].update(headers)
            else:
                kwargs["headers"] = headers
        self.logger.debug("Making POST %s" % resource)
        response = self.requests_retry_session().post(
            resource, **kwargs, timeout=REQUEST_TIMEOUT
        )
        self.log_response(response, verbose)
        return response

    def get(self, resource: str, api_key=None, api_id=None, verbose=True, **kwargs):
        headers = {}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        if api_id is not None:
            headers["X-API-ID"] = api_id
        if headers:
            if "headers" in kwargs:
                kwargs["headers"].update(headers)
            else:
                kwargs["headers"] = headers
        self.logger.debug("Making GET %s" % resource)
        response = self.requests_retry_session().get(
            resource, **kwargs, timeout=REQUEST_TIMEOUT
        )
        self.log_response(response, verbose)
        return response

    def put(self, resource: str, api_key=None, api_id=None, verbose=True, **kwargs):
        headers = {}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        if api_id is not None:
            headers["X-API-ID"] = api_id
        if headers:
            if "headers" in kwargs:
                kwargs["headers"].update(headers)
            else:
                kwargs["headers"] = headers
        self.logger.debug("Making PUT %s" % resource)
        response = self.requests_retry_session().put(
            resource, **kwargs, timeout=REQUEST_TIMEOUT
        )
        self.log_response(response, verbose)
        return response

    def patch(self, resource: str, api_key=None, api_id=None, verbose=True, **kwargs):
        headers = {}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        if api_id is not None:
            headers["X-API-ID"] = api_id
        if headers:
            if "headers" in kwargs:
                kwargs["headers"].update(headers)
            else:
                kwargs["headers"] = headers
        self.logger.debug("Making PATCH %s" % resource)
        response = self.requests_retry_session().patch(
            resource, **kwargs, timeout=REQUEST_TIMEOUT
        )
        self.log_response(response, verbose)
        return response

    def delete(self, resource: str, api_key=None, api_id=None, verbose=True, **kwargs):
        headers = {}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        if api_id is not None:
            headers["X-API-ID"] = api_id
        if headers:
            if "headers" in kwargs:
                kwargs["headers"].update(headers)
            else:
                kwargs["headers"] = headers
        self.logger.debug("Making DELETE %s" % resource)
        response = self.requests_retry_session().delete(
            resource, **kwargs, timeout=REQUEST_TIMEOUT
        )
        self.log_response(response, verbose)
        return response

    def requests_retry_session(self):
        session = requests.Session()
        retries = Retry(
            total=RETRY_TIMES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=RETRY_CODES,
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
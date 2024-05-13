# Custom adapter for UN site 
# See https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled

import requests
import urllib3
import ssl

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """Transport adapter that allows us to use custom ssl_context."""

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)
        
def get_custom_un_session() -> requests.Session:
    session = requests.Session()
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4 # Downgrades ssl context
    session.mount('https://', CustomHttpAdapter(ctx))
    return session
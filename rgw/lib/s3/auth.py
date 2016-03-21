from boto.s3.connection import S3Connection
import boto.s3.connection
import boto.exception as exception
import utils.log as log
from utils.utils import Attribs


class Authenticate(object):

    def __init__(self, access_key, secret_key):
        self.ak = access_key
        self.sk = secret_key

    def do_auth(self):

        attribs = Attribs()

        try:
            log.info('got the credentials')
            conn = S3Connection(self.ak, self.sk)
            log.info('acess_key %s\n secret_key %s' % (self.ak, self.sk))

            attribs.conn = conn

            auth_stack = {'status': True,
                          'attribs': attribs}

            log.info('connection successful')

        except (boto.s3.connection.HostRequiredError, exception.AWSConnectionError), e:

            log.error('connection failed')
            log.error(e)

            auth_stack = {'status': False,
                          'msgs': e}


        return auth_stack


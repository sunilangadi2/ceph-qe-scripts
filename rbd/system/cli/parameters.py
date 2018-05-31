import sys
import itertools
sys.path.append("../../")
import utils.log as log
import utils.utils as rbd

pool_name = {'arg': '-p', 'val': {'pool1': 'test_rbd_pool',
                                  'pool2': 'test_rbd_pool2'}}

image_format = {'arg': '--image-format',
                'val': {None: None,
                        'image-format 1': '1',
                        'image-format 2': '2'}}

image_size = {'arg': '-s',
              'val': {'size_MB': '100M',
                      'size_GB': '10G',
                      'size_TB': '1T'}}

object_size = {'arg': '--object-size',
               'val': {None: None,
                       'size_B': '8192B',
                       'size_KB': '256K',
                       'size_MB': '32M'}}

image_feature = {'arg': '--image-feature',
                 'val': {None: None,
                         'layering': 'layering',
                         'striping': 'striping',
                         'exclusive-lock': 'exclusive-lock',
                         'journaling': 'exclusive-lock,journaling',
                         'deep-flatten': 'deep-flatten',
                         'object-map': 'exclusive-lock,object-map',
                         'fast-diff': 'exclusive-lock,object-map,fast-diff'}}

image_resize = {'arg': '-s',
                'val': {'expand_size_TB': '2T',
                        'shrink_size_GB': '512G --allow-shrink',
                        'shrink_size_MB': '1536M --allow-shrink'}}


io_size = {'arg': '--io-size', 'val': {None: None,
                                       'size_KB': '256K'}}

io_threads = {'arg': '--io-threads', 'val': {None: None,
                                             'val1': '20'}}

io_total = {'arg': '--io-total', 'val': {'size_MB': '50M'}}

io_pattern = {'arg': '--io-pattern', 'val': {None: None,
                                             'pattern_seq': 'seq',
                                             'pattern_rand': 'rand'}}

limit = {'arg': '--limit', 'val': {'val1': '10'}}

image_shared = {'arg': '', 'val': {None: None,
                                   'val1': '--image-shared'}}

whole_object = {'arg': '', 'val': {None: None,
                                   'val1': '--whole-object'}}


stripe_v2 = {'arg': ['--stripe-unit', '--stripe-count'],
             'val': {None: [None, None],
                     'size_B': ['2048', '16'],
                     'size_KB': ['65536', '16'],
                     'size_MB': ['16777216', '16']}}

stripe_v3 = {'arg': ['--stripe-unit', '--stripe-count'],
             'val': {None: [None, None],
                     'size_B': ['2048B', '16'],
                     'size_KB': ['64K', '16'],
                     'size_MB': ['16M', '16']}}

io_type_v2 = {'arg': '', 'val': {'write': 'write'}}

io_type_v3 = {'arg': ' --io-type', 'val': {'read': 'read',
                                           'write': 'write'}}


export_format_v2 = {'arg': None, 'val': {None: None}}

export_format_v3 = {'arg': '--export-format',
                    'val': {None: None,
                            'export-format 1': '1',
                            'export-format 2': '2'}}


class CliParams(object):

    def __init__(self):
        # Ceph version specific parameters list
        list = ['stripe', 'io_type', 'export_format']

        self.ceph_version = rbd.exec_cmd('ceph -v')
        if 'version 10' in self.ceph_version:
            self.ceph_version = 2
        elif 'version 12' in self.ceph_version:
            self.ceph_version = 3

        for param in list:
            globals()[param] = globals()['{}_v{}'.format(param,
                                                         self.ceph_version)]

    def search_param_val(self, param_arg, str_to_search):
            if str_to_search.find(param_arg) != -1:
                str_to_search = str_to_search.split()
                return str_to_search[int(str_to_search.index(param_arg)) + 1]
            else:
                return 0

    def get_byte_size(self, size):
        mul_dict = {'B': 1, 'K': 1024, 'M': 1024*1024}
        if mul_dict.get(str(size)[-1], None):
            return int(size[0:len(size)-1])*mul_dict[str(size)[-1]]
        return size

    def remove_duplicates(self, initial_list):
        final_list = []
        map(lambda val: final_list.append(val)
            if val not in final_list else False, initial_list)
        return final_list

    def generate_combinations(self, *parameter_list):
        param_list_all = []
        combined_param_list = []

        # Generate values for parameters & store in param_list_all in list type
        for param in parameter_list:
            param_list = []

            # Generate values for one parameter
            for key, val in globals()[param]['val'].iteritems():
                if key:
                    if type(val) is list:
                        string = ''
                        for x in xrange(0, len(val)):
                            string = string + globals()[param]['arg'][x] \
                                  + ' ' + val[x] + ' '
                        param_list.append(string)
                    else:
                        param_list.append(globals()[param]['arg'] + ' ' + val)
                else:
                    param_list.append('')
            param_list_all.append(param_list)

        # Generate and store all combinations of parameters in str type
        for param_list in itertools.product(*param_list_all):
            str = ''
            for index in xrange(0, len(param_list)):
                str = str + ' ' + param_list[index]
                combined_param_list.append(str)

        # Remove Extra Spaces
        combined_param_list = [val.strip() for val in combined_param_list]

        combined_param_list = self.remove_duplicates(combined_param_list)

        return combined_param_list
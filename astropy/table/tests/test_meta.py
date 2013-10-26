# These tests should be kept consistent with those for NDData as the two objects should have the same ``meta`` behavior.

import numpy as np

from ..table import Table
from ...utils.compat.odict import OrderedDict
from ...tests.helper import pytest, raises
from ...io import fits

class OrderedDictSubclass(OrderedDict):
    pass


@pytest.mark.parametrize(('meta'), ([dict([('a', 1)]), OrderedDict([('a', 1)]), OrderedDictSubclass([('a', 1)])]))
def test_mapping(meta):
    arr = Table([(1,2,3)], meta=meta)
    assert type(arr.meta) == type(meta)
    assert arr.meta['a'] == 1


@pytest.mark.parametrize(('meta'), (["ceci n'est pas un meta", 1.2, [1,2,3]]))
def test_non_mapping(meta):
    with pytest.raises(TypeError):
        d1 = Table([(1,2,3)], meta=meta)


def test_meta_fits_header():

    header = fits.header.Header()
    header.set('observer', 'Edwin Hubble')
    header.set('exptime', '3600')

    d1 = Table([(1,2,3)], meta=header)

    assert d1.meta['OBSERVER'] == 'Edwin Hubble'


def test_meta_set_disabled():
    d1 = Table([(1,2,3)])
    with pytest.raises(AttributeError):
        d1.meta = {'a':1}

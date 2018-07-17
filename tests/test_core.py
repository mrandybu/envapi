from apicore.core import EnvAPI
from apicore.core import Environment


def test_service():
    api = EnvAPI()
    ls = api.service('ls')
    assert isinstance(ls, Environment)


def test_api_read():
    api = EnvAPI()
    ls = api.service('ls')
    print(type(ls.run('/').read))
    assert 'bin' in ls.run('/').read


def test_api_buff():
    api = EnvAPI()
    ls = api.service('ls')
    assert ls.run('/').buff.__dict__['buff']


def test_api_set_pipe():
    api = EnvAPI()
    set_pipe = api.set_pipe('grep', 'bin')
    assert set_pipe['src'] and set_pipe['args']


def test_api_pipe():
    api = EnvAPI()
    ls = api.service('ls')
    buff = ls.run('/').buff
    set_pipe = api.set_pipe('grep', 'bin')
    pipe = buff.pipe(set_pipe)
    assert pipe.__dict__['read'] and pipe.__dict__['buff']

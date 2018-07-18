from apicore.core import EnvAPI
from apicore.core import Environment


class TestCore(object):
    def __init__(self):
        api = EnvAPI()
        self.ls = api.get_api('ls')
        self.grep = api.get_api('grep')

    def test_service(self):
        assert isinstance(self.ls, Environment)

    def test_api_run(self):
        assert isinstance(self.ls, Environment)

    def test_api_output(self):
        assert 'bin' in self.ls.run('/').to_list()

    def test_api_pipe(self):
        assert 'bin' in self.ls.run('/').pipe(self.grep.run('bin')).to_list()

    def test_recurrent_pipe(self):
        single_pipe = self.ls.run('/').pipe(self.grep.run('b'))
        assert 'bin' in single_pipe.pipe(self.grep.run('bin')).to_list()

    def run(self):
        self.test_service()
        self.test_api_run()
        self.test_api_output()
        self.test_api_pipe()
        self.test_recurrent_pipe()


if __name__ == "__main__":
    TestCore().run()

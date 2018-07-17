from subprocess import Popen, PIPE
import logging
import __root__


def get_logger(info):
    logging.basicConfig(filename=__root__.get_root_path('sysenvapi.log'),
                        filemode='w',
                        level=logging.INFO)
    logging.info(info)


class Service:
    def __init__(self, buff):
        self.buff = buff

    def __pipe_run(self):
        return Popen([self.src, self.args], stdin=self.buff, stdout=PIPE)

    def __read(self):
        return self.__pipe_run().stdout.read().decode()

    def __buff(self):
        object.__setattr__(self, 'buff', self.__pipe_run().stdout)
        return self

    def pipe(self, set_pipe):
        setattr(self, 'src', set_pipe['src'])
        setattr(self, 'args', set_pipe['args'])
        setattr(Service.pipe, 'read', self.__read())
        setattr(Service.pipe, 'buff', self.__buff())
        return self.pipe


class Environment(object):
    def __init__(self, src=None):
        self.src = src

    def __run(self, args):
        return Popen([self.src, args], stdout=PIPE)

    def __read(self):
        return self.__run(self.args).stdout.read().decode()

    def __buff(self):
        return Service(self.__run(self.args).stdout)

    def run(self, args):
        setattr(self, 'args', args)
        setattr(Environment.run, 'read', self.__read())
        setattr(Environment.run, 'buff', self.__buff())
        return self.run


class EnvAPI(object):
    __env_attr = {}

    def __get_env(self):
        return Popen([self.__env_attr['src']], stdout=PIPE, stderr=PIPE)

    def __allowed_src(self, src):
        self.__env_attr['src'] = src
        return self.__get_env()

    def __check_service(self):
        try:
            self.__allowed_src(self._bin_name)
        except:
            return False
        return True

    def service(self, bin_name):
        setattr(self, '_bin_name', bin_name)
        if not self.__check_service():
            raise AttributeError
        return Environment(bin_name)

    def set_pipe(self, bin_name, args):
        setattr(self, '_bin_name', bin_name)
        if not self.__check_service():
            raise AttributeError
        return {'src': bin_name, 'args': args}

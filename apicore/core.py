from subprocess import Popen, PIPE
import logging
import __root__


def get_logger(info):
    logging.basicConfig(filename=__root__.get_root_path('sysenvapi.log'),
                        filemode='w',
                        level=logging.INFO)
    logging.info(info)


class Service:
    def __init__(self, _buff_):
        self._buff_ = _buff_

    def __pipe_run(self):
        return Popen([self.service, self.args], stdin=self._buff_, stdout=PIPE)

    def __read(self):
        return self.__pipe_run().stdout.read().decode()

    def __buff(self):
        setattr(self, 'buff', self.__pipe_run().stdout)
        return self

    def pipe(self, set_pipe):
        setattr(self, 'service', set_pipe['service'])
        setattr(self, 'args', set_pipe['args'])
        setattr(Service.pipe, 'read', self.__read())
        setattr(Service.pipe, 'buff', self.__buff())
        return self.pipe


class Environment(object):
    def __init__(self, _service=None):
        self._service = _service

    def __run(self, args):
        return Popen([self._service, args], stdout=PIPE)

    def __read(self):
        return self.__run(self.args).stdout.read().decode()

    def __buff(self):
        buff_ = self.__run(self.args).stdout
        return Service(buff_)

    def run(self, args):
        setattr(self, 'args', args)
        setattr(Environment.run, 'read', self.__read())
        setattr(Environment.run, 'buff', self.__buff())
        return self.run


class EnvAPI(object):
    __env_attr = {}

    def __get_env(self):
        return Popen([self.__env_attr['service']], stdout=PIPE, stderr=PIPE)

    def __allow_service(self):
        self.__env_attr['service'] = self._service
        return self.__get_env()

    def __check_service(self):
        try:
            self.__allow_service()
        except:
            return False
        return True

    def get_api(self, service):
        setattr(self, '_service', service)
        if not self.__check_service():
            raise AttributeError
        return Environment(service)

    def set_pipe(self, service, args):
        setattr(self, '_service', service)
        if not self.__check_service():
            raise AttributeError
        return {'service': service, 'args': args}

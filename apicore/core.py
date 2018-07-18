from subprocess import Popen, PIPE
import logging
import __root__


def get_logger(info):
    logging.basicConfig(filename=__root__.get_root_path('sysenvapi.log'),
                        filemode='w',
                        level=logging.INFO)
    logging.info(info)


class Service(object):
    def __init__(self, buff=None, service=None, args=None):
        self.__buff = buff
        self.__service = service
        self.__args = args

    def __str__(self):
        return self.__buff.read().decode()

    def pipe(self, st):
        return Service(Popen([st.__service, st.__args], stdin=self.__buff, stdout=PIPE).stdout)

    def to_list(self):
        return self.__str__()


class Environment(object):
    def __init__(self, _service=None):
        self._service = _service

    def __run(self, args):
        return Popen([self._service, args], stdout=PIPE)

    def __buff(self):
        return self.__run(self.args).stdout

    def run(self, args):
        setattr(self, 'args', args)
        return Service(self.__buff(), self._service, self.args)


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

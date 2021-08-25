from core.singleton import Singleton


class BaseURL(metaclass=Singleton):
    def __init__(self, root_url: str = None):
        if root_url is None:
            raise TypeError("root_url can't be None")
        self.url = root_url

    def __str__(self):
        return self.url

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"

    def __add__(self, other):
        return self.url.__add__(other)


class URL:
    def __init__(self, href: str):
        self.base_url: BaseURL = BaseURL()
        self.__path = '/' + href.removeprefix(str(self.base_url)).lstrip('/')

    def __str__(self):
        return self.base_url + self.__path

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    @property
    def path(self):
        return self.__path

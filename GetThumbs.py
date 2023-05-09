from threading import Thread
from urllib.request import urlretrieve
import sys


class GetThumb(Thread):
        def __init__(self, url, id):
            Thread.__init__(self)
            self.url:str = url
            self.id:int = id
            self.fileName:str = str()
            self.temp_name = f"thumbs/thumb{self.id}.jpg"

        def run(self) -> str:
            try:
                urlretrieve(self.url, self.temp_name)
                self.fileName = self.temp_name
                return self.fileName
            except:
                erro = sys.exc_info()
                print("Ocorreu um erro:", erro)
                self.fileName = "notFound.jpg"
                return self.fileName
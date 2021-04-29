import hashlib
import logging
import os

from .file_service import FileService
from ..config import DEFAULT_ENCODING
from ..utils import get_sig_name
from ..exception import SignatureException


class SignedFileService(FileService):

    def create(self, path: str, name: str, content: str) -> str:
        file = super().create(path, name, content)

        sig_file_name = get_sig_name(name)
        try:
            file_path = os.path.join(path, sig_file_name)
            with open(file_path, "w") as f:
                f.write(self.calculate_sig(path, name))

            logging.info("Created signature: {}".format(file_path))
        except Exception as e:
            logging.error(e)

        return file

    def delete(self, path: str, filename: str) -> bool:
        result = super().delete(path, filename)

        if result:
            try:
                os.remove(os.path.join(path, get_sig_name(filename)))
            except Exception as e:
                logging.error(e)

        return result

    def read(self, path, filename) -> str:
        try:
            with open(get_sig_name(filename), 'r') as sf:
                if sf.read() != self.calculate_sig(path, filename):
                    raise SignatureException(f"Checksums does not match for file {filename}")
        except OSError:
            logging.warning(f"Can`t verify signature for file {filename}")

        return super().read(path, filename)

    def calculate_sig(self, path, file_name) -> str:
        return hashlib.sha512(
            (super().read(path, file_name) +
             super().print_metadata(path, file_name)).encode(DEFAULT_ENCODING)).hexdigest()

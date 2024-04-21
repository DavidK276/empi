from django.db import models


class SeparatedBinaryField(models.BinaryField):
    """
    Stores a list of binary blobs in a single field using byte stuffing.
    """

    __BORDER_BYTE = 0x7E
    __STUFF_BYTE = 0x7D
    __PROHIBITED_BYTES = (__BORDER_BYTE, __STUFF_BYTE)

    def stuff_byte(self, byte: int) -> bytes:
        """
        :param byte: the byte that will be stuffed
        :return: the same byte if it's not a prohibited byte, otherwise a sequence of: 0x7d, byte XOR 0x20
        """
        if byte in self.__PROHIBITED_BYTES:
            return bytes((self.__STUFF_BYTE, byte ^ 0x20))
        return bytes((byte,))

    def stuff_bytes(self, value: bytes) -> bytes:
        return b"".join(self.stuff_byte(byte) for byte in value)

    def unstuff_bytes(self, value: bytes):
        result = []
        i = 0
        curr_value = b""
        while i < len(value):
            if value[i] == self.__STUFF_BYTE:
                curr_value += bytes((value[i + 1] ^ 0x20,))
                i += 1
            elif value[i] == self.__BORDER_BYTE:
                result.append(curr_value)
                curr_value = b""
            else:
                curr_value += bytes((value[i],))
            i += 1
        result.append(curr_value)
        return result

    def to_python(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            return value
        if value is None:
            return None
        return self.unstuff_bytes(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return self.unstuff_bytes(value)

    def get_prep_value(self, value):
        return bytes((self.__BORDER_BYTE,)).join(self.stuff_bytes(v) for v in value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

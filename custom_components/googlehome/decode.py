import io
import struct


class Reader:
    def __init__(self, buf: io.IOBase):
        self.buf = buf
        self.len = buf.seek(0, io.SEEK_END)
        self.pos = buf.seek(0)
    
    def _read_exact(self, length):
        if length == 0:
            return b''
        val = self.buf.read(length)
        if len(val) == 0:
            raise EOFError
        if len(val) < length:
            print("Read too less")
            raise EOFError
        return val

    def varint(self): # int32, int64, uint32, bool, enum, etc
        shift = 0
        result = 0
        while True:
            self.pos += 1
            if self.pos > self.len:
                raise EOFError
            i = ord(self._read_exact(1))
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break
        return result

    def fixed64(self, signed=False): # fixed64, sfixed64, double
        self.pos += 8
        if self.pos >= self.len:
            raise EOFError
        return struct.unpack('<q' if signed else '<Q', self._read_exact(8))
    
    def fixed32(self): # fixed32, sfixed32, float
        self.pos += 4
        if self.pos >= self.len:
            raise EOFError
        return struct.unpack('<f', self._read_exact(4))

    def byteseq(self): # string, bytes, sub-message
        length = self.varint()
        start = self.pos
        end = start + length

        if end > self.len:
            raise EOFError
        
        self.pos += length
        return self._read_exact(length)
    
    def skip(self, length=None):
        if length:
            self.pos += length
            if self.pos >= self.len:
                raise EOFError
            self._read_exact(length)
        else:
            self.varint()

    def done(self):
        self.pos == self.len


def get_data(buf: io.IOBase):
    f = Reader(buf)
    out = []
    while not f.done():
        try:
            tag = f.varint()
        except EOFError:
            break
        id = abs(tag >> 3)
        wiretype = tag & 7
        def bytes_helper(f):
            buf = f.byteseq()
            try:
                data = get_data(io.BytesIO(buf))
                return data
            except (KeyError, EOFError):
                if any(b < 32 for b in buf):
                    return buf
                else:
                    return buf.decode("utf-8")
       
        def skip_type(f, wiretype):
            def _skip_start_group(f):
                while True:
                    wiretype = f.varint() & 7
                    if wiretype == 4:
                        break
                    skip_type(f, wiretype)

            {
                0: lambda: f.skip(),
                1: lambda: f.skip(8),
                2: lambda: f.skip(f.varint()),
                3: lambda: _skip_start_group(f),
                5: lambda: f.skip(4),
            }[wiretype]()

        def _append(id, out, func):
            d = {}
            d[str(id)] = func()
            out.append(d)
        append = lambda func: _append(id, out, func)

        {
            0: lambda: append(lambda: f.varint()),
            1: lambda: append(lambda: f.fixed64()),
            2: lambda: append(lambda: bytes_helper(f)),
            3: lambda: skip_type(f, wiretype),
            5: lambda: append(lambda: f.fixed32()),
        }[wiretype]()
    return out


def decode_proto(buf: io.IOBase):
    data = get_data(buf)

    def _get_obj_by_key(l, key):
        return next(filter(lambda v: key in v, l))

    tokens = {}
    for val in data:
        try:
            if isinstance(val['2'], list):
                for val2 in val['2']:
                    try:
                        if isinstance(val2['7'], list):
                            device = next(iter(_get_obj_by_key(val2['7'], '18')['18'][0].values()))
                            token = _get_obj_by_key(val2['7'], '28')['28']
                            tokens[device] = token
                    except Exception as e:
                        # print(e)
                        pass
        except Exception as e:
            #print(e)
            pass
    return tokens

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) <= 1:
        print("Please provide a file as an argument")
    
    data = decode_proto(io.FileIO(sys.argv[1]))
    print(data)

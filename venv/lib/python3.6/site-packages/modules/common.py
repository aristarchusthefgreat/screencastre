from modules import dialog


class Point:
    # X Coordinate Value
    X = 0
    # Y Coordinate Value
    Y = 0

    # CONSTRUCTOR
    def __init__(self):
        self.X = 0
        self.Y = 0

    # CONSTRUCTOR - with the values to give it
    def __init__(self, nX, nY):
        self.X = nX
        self.Y = nY

    # So we can set both values at the same time
    def Set(self, nX, nY):
        self.X = nX
        self.Y = nY


class Save:
    FILE = ""
    CONTENTS = dict()

    def __init__(self, file, contents):
        import struct

        self.FILE = file

        if not self.FILE.endswith('.scr'):
            self.FILE += '.scr'

        self.CONTENTS = list(bytes(str(contents), 'utf-8'))

        if not self.CONTENTS == [91, 93]:
            with open(self.FILE, "wb+") as f:
                for char in self.CONTENTS:
                    f.write(struct.pack('h', char))
                f.close()
        else:
            dialog.ErrorMsg("There is no data to save!")


class Open:
    FILE = ""
    Contents = ""

    def __init__(self, file):
        self.FILE = file
        self.byte_list = list()
        self.load_contents()

    def load_contents(self):
        import ast, struct
        if self.FILE.endswith('.scr'):
            with open(self.FILE, 'rb') as f:
                self.Contents = f.read()
                f.close()

            fmt = '>'+str(len(self.Contents))+'c'

            self.Contents = struct.unpack(fmt, self.Contents)
            for char in self.Contents:
                tmp = char.decode('utf-8')
                if tmp != '\x00':
                    self.byte_list.append(tmp)

            self.Contents = ''.join(self.byte_list)
            self.Contents = ast.literal_eval(self.Contents)
        else:
            dialog.ErrorMsg('Unrecognised File Extension.')

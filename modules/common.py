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

    def __init__(self, file, obj, s=1):

        self.FILE = file
        self.CONTENTS = obj

        if s:
            self.save()

    def save(self):
        import pickle

        if self.CONTENTS:

            if not self.FILE.endswith('.scr'):
                self.FILE += '.scr'

            with open(self.FILE, 'wb+') as f:
                pickle.dump(self.CONTENTS, f, pickle.HIGHEST_PROTOCOL)

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
        import pickle
        if self.FILE.endswith('.scr'):
            with open(self.FILE, 'rb') as f:
                local_test = pickle.load(f)
            self.Contents = local_test
        else:
            dialog.ErrorMsg('Unrecognised File Extension.')


class Audio:

    AVAILABLE_DEVICES = list()

    def __init__(self):
        self.getAvailableDevices()
    
    def getAvailableDevices(self):
        import os

        devices = os.popen("arecord -l")
        device_string = devices.read()
        device_string = device_string.split("\n")
        for line in device_string:
                if(line.find("card") != -1):
                   self.AVAILABLE_DEVICES.append(line)
    
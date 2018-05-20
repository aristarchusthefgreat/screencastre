import os, time, glob, traceback
from modules import dialog
from _constants import *


class ffmpegVideo:
    AUDIO = False
    pipe = None

    def __init__(self, audio=None, driver='', device='', fps='30'):
        global TMP_DIR, DISPLAY, EXT

        self.isRunning = False

        if audio:
            self.AUDIO = True

        self.video_filename = self.unique_filename()

        if self.AUDIO:
            self.command = [FFMPEG_BIN,
                            '-video_size', os.environ['Width']+'x'+os.environ['Height'],
                            '-framerate', fps,
                            '-f', 'x11grab',
                            '-i', DISPLAY,
                            '-f', driver,
                            '-ac', '2',
                            '-ar', '24000',
                            '-i', device,
                            '-acodec', 'aac',
                            '-vcodec', 'libx264',
                            '-qp', '0',
                            '-preset', 'ultrafast',
                            '-y', os.path.join(TMP_DIR, self.video_filename)
                            ]
        else:
            self.command = [FFMPEG_BIN,
                            '-video_size', os.environ['Width'] + 'x' + os.environ['Height'],
                            '-framerate', fps,
                            '-f', 'x11grab',
                            '-i', DISPLAY,
                            '-vcodec', 'libx264',
                            '-qp', '0',
                            '-preset', 'ultrafast',
                            '-y', os.path.join(TMP_DIR, self.video_filename)
                            ]
        print(self.command)

    def start(self):
        import threading as th

        thread = th.Thread(target=self.record)
        thread.start()

    def record(self):
        import subprocess as sp

        try:
            self.isRunning = True
            self.pipe = sp.Popen(self.command, stderr=sp.PIPE)
        except (sp.CalledProcessError, Exception) as e:
            self.isRunning = False
            dialog.ErrorMsg(repr(e))

    def stop(self):
        try:
            self.pipe.terminate()
        except:
            e = traceback.format_exc()
            self.pipe = None
            dialog.ErrorMsg(repr(e))

        self.isRunning = False

    def unique_filename(self):
        global TMP_DIR, EXT

        i = 0

        while os.path.exists((os.path.join(TMP_DIR, 'tmp_%s.%s') % (i, EXT['Video']))):
            i += 1

        return 'tmp_%s.%s' % (i, EXT['Video'])


class AV_COMPILE(ffmpegVideo):

    def __init__(self, audio=True, driver='alsa', device='', fps='30'):

        if device != 'default':
            device = "hw:" + device[device.find("card") + 5] + "," + \
                     device[device.find("device") + 7]

        self.ex = None
        super().__init__(audio, driver, device, fps)

    def compile(self):
        self.compile_av()

    def compile_av(self):
        time.sleep(1)

        import subprocess as sp

        save_dir = SETTINGS.settings_list['save_dir']

        try:
            vd_in = max(glob.iglob(os.path.join(TMP_DIR, '*.mp4')), key=os.path.getctime)
        except Exception as e:
            dialog.ErrorMsg(repr(e))

        try:
            os.environ["File"]
            out = os.path.join(save_dir, os.environ['File'] + '.' + SETTINGS.settings_list['ext'])
        except KeyError:
            os.environ["File"] = "new_output" + '.' + SETTINGS.settings_list['ext']
        finally:
            if os.environ['File'] != '':
                out = os.path.join(save_dir, os.environ['File'] + '.' + SETTINGS.settings_list['ext'])
            else:
                out = os.path.join(save_dir, 'new_output' + '.' + SETTINGS.settings_list['ext'])


        print(out)

        if os.path.isfile(out):

            question = dialog.QuestionDialog('This File exists. Are you sure you wish to overwrite it?')

            if question.clickedButton() == question.yes:
                self.ex = '%s -i %s -codec copy -y %s' % (FFMPEG_BIN, vd_in, out)
                sp.call(self.ex, shell=True, stderr=sp.PIPE)
            else:
                pass
        else:
            print("Execute")
            self.ex = 'ffmpeg -i %s -codec copy -y %s' % (vd_in, out)
            sp.call(self.ex, shell=True, stderr=sp.PIPE)

        if ('question' in locals() and question.clickedButton() == question.yes) or ('question' not in locals()):
            os.remove(vd_in)
            if os.path.isfile(out):
                os.environ['LastFile'] = out
            else:
                print("No file.")
        else:
            os.environ['LastFile'] = vd_in

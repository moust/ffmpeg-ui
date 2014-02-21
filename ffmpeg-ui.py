#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import ttk
from tkFileDialog import askopenfilename, asksaveasfilename
import tkMessageBox
import subprocess
import fcntl
import select
import os
import re


class Application(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent

        self.vcodecs = [
            u"libtheora",
            u"libvpx",
            u"libwebp",
            u"libx264",
            u"libx264rgb",
            u"libxvid",
            u"png",
            u"ProRes"
        ]

        self.acodecs = [
            u"aac",
            u"ac3",
            u"ac3_fixed",
            u"libfaac"
            u"libfdk_aac",
            u"libmp3lame",
            u"libopencore-amrnb",
            u"libshine",
            u"libtwolame",
            u"libvo-aacenc",
            u"libvo-amrwbenc",
            u"libopus",
            u"libvorbis",
            u"libwavpack",
            u"wavpack"
        ]

        self.formats = [
            u"null",
            u"mov",
            u"ismv",
            u"mp3",
            u"ogg",
            u"aiff",
            u"crc",
            u"framecrc",
            u"md5",
            u"framemd5",
            u"gif",
            u"hls",
            u"ico",
            u"image2",
            u"matroska",
            u"mpegts"
        ]

        self.pixfmts = [
            u"yuv420p",
            u"yuv422p",
            u"yuv444p",
            u"yuv422",
            u"yuv410p",
            u"yuv411p",
            u"yuvj420p",
            u"yuvj422p",
            u"yuvj444p",
            u"rgb24",
            u"bgr24",
            u"rgba32",
            u"rgb565",
            u"rgb555",
            u"gray",
            u"monow",
            u"monob",
            u"pal8",
        ]

        self.presets = {
            'H.264 720p': {
                'vcodec':        'libx264',
                'vb':            '3500k',
                'width':         1280,
                'height':        720,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'aac',
                'ar':            44100,
                'ab':            '128k',
                'format':        'mp4',
                'extraOptions':  '-movflags faststart'
            },
            'H.264 576p': {
                'vcodec':        'libx264',
                'vb':            '2000k',
                'width':         1024,
                'height':        576,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'aac',
                'ar':            44100,
                'ab':            '128k',
                'format':        'mp4',
                'extraOptions':  '-movflags faststart'
            },
            'H.264 360p': {
                'vcodec':        'libx264',
                'vb':            '1000k',
                'width':         640,
                'height':        360,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'aac',
                'ar':            44100,
                'ab':            '128k',
                'format':        'mp4',
                'extraOptions':  '-movflags faststart -maxrate 1500k -bufsize 3000k'
            },
            'WebM 720p': {
                'vcodec':        'libvpx',
                'vb':            '3500k',
                'width':         1280,
                'height':        720,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'libvorbis',
                'ar':            44100,
                'ab':            '128k',
                'format':        'webm',
                'extraOptions':  '-quality good'
            },
            'WebM 576p': {
                'vcodec':        'libvpx',
                'vb':            '2000k',
                'width':         1024,
                'height':        576,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'libvorbis',
                'ar':            44100,
                'ab':            '128k',
                'format':        'webm',
                'extraOptions':  '-quality good'
            },
            'WebM 360p': {
                'vcodec':        'libvpx',
                'vb':            '1500k',
                'width':         640,
                'height':        360,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'libvorbis',
                'ar':            44100,
                'ab':            '128k',
                'format':        'webm',
                'extraOptions':  '-quality good'
            },
        }

        self.initialize()

        self.inputFiles = [];

    def initialize(self):
        # width = 800
        # height = 600
        # xoffset = (self.winfo_screenwidth()-width)/2
        # yoffset = (self.winfo_screenheight()-height)/2
        # print "%dx%d%+d%+d" % (width, height, xoffset, yoffset)
        # self.geometry("%dx%d%+d%+d" % (width, height, xoffset, yoffset))
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.grid()
        self.widgets()

    def widgets(self):

        # Source frame

        source = Tkinter.LabelFrame(self, text=u"Source file")
        source.grid(row=0, columnspan=2, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


        inputFileLbl = Tkinter.Label(source, text="Select File:")
        inputFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.inputFileVar = Tkinter.StringVar()

        inputFileTxt = Tkinter.Entry(source, textvariable=self.inputFileVar, width="50")
        inputFileTxt.grid(row=0, column=1, sticky="WE", pady=3)

        inputFileBtn = Tkinter.Button(source, text="Browse ...", command=self.OnInputBrowseClick)
        inputFileBtn.grid(row=0, column=2, sticky='W', padx=5, pady=2)



        # Output frame

        output = Tkinter.LabelFrame(self, text=u"Output details")
        output.grid(row=1, columnspan=2, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


        outputFileLbl = Tkinter.Label(output, text="Save File to:")
        outputFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.outputFileVar = Tkinter.StringVar()

        outputFileTxt = Tkinter.Entry(output, textvariable=self.outputFileVar, width="50")
        outputFileTxt.grid(row=0, column=1, sticky="WE", pady=3)

        outputFileBtn = Tkinter.Button(output, text="Browse ...", command=self.OnOutputBrowseClick)
        outputFileBtn.grid(row=0, column=2, sticky='W', padx=5, pady=2)



        # Preset

        preset = Tkinter.LabelFrame(self, text=u"Preset")
        preset.grid(row=2, columnspan=2, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


        # presets list

        presetsLbl = Tkinter.Label(preset, text=u"Use a preset")
        presetsLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        presets = []
        for presetName, presetOptions in self.presets.iteritems():
            presets.append(presetName)

        self.presetsVar = Tkinter.StringVar()
        self.presetsVar.trace("w", self.OnPresetSelected)
        self.presetsList = Tkinter.OptionMenu(preset, self.presetsVar, *presets)
        self.presetsList.grid(row=0, column=1, sticky="w", padx=5, pady=2)



        # Video options

        video = Tkinter.LabelFrame(self, text=u"Video options")
        video.grid(row=3, column=0, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)


        # video codec

        vcodecLbl = Tkinter.Label(video, text=u"Video codec")
        vcodecLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.vcodecVar = Tkinter.StringVar()
        self.vcodecList = Tkinter.OptionMenu(video, self.vcodecVar, *self.vcodecs)
        self.vcodecList.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Video bitrate

        vbLbl = Tkinter.Label(video, text=u"Video bitrate")
        vbLbl.grid(row=1, column=0, sticky="E", padx=5, pady=2)

        self.vbVar = Tkinter.StringVar()
        self.vbVar.set(0)
        self.vb = Tkinter.Entry(video,textvariable=self.vbVar)
        self.vb.grid(row=1, column=1, sticky="W", padx=5, pady=2)

        # Video width

        widthLbl = Tkinter.Label(video, text=u"Video width")
        widthLbl.grid(row=2, column=0, sticky="E", padx=5, pady=2)

        self.widthVar = Tkinter.IntVar()
        self.width = Tkinter.Entry(video,textvariable=self.widthVar)
        self.width.grid(row=2, column=1, sticky="W", padx=5, pady=2)

        # Video height

        heightLbl = Tkinter.Label(video, text=u"Video height")
        heightLbl.grid(row=3, column=0, sticky="E", padx=5, pady=2)

        self.heightVar = Tkinter.IntVar()
        self.height = Tkinter.Entry(video,textvariable=self.heightVar)
        self.height.grid(row=3, column=1, sticky="W", padx=5, pady=2)

        # pixel format

        pixfmtLbl = Tkinter.Label(video, text=u"Pixel format")
        pixfmtLbl.grid(row=4, column=0, sticky='E', padx=5, pady=2)

        self.pixfmtVar = Tkinter.StringVar()
        self.pixfmtList = Tkinter.OptionMenu(video, self.pixfmtVar, *self.pixfmts)
        self.pixfmtList.grid(row=4, column=1, sticky="W", padx=5, pady=2)

        # frame rate

        fpsLbl = Tkinter.Label(video, text=u"Frame rate")
        fpsLbl.grid(row=5, column=0, sticky='E', padx=5, pady=2)

        self.fpsVar = Tkinter.IntVar()
        self.fps = Tkinter.Entry(video, textvariable=self.fpsVar)
        self.fps.grid(row=5, column=1, sticky="W", padx=5, pady=2)

        # min quality

        self.qmin = Tkinter.Scale(video, from_=-1, to=69, orient=Tkinter.HORIZONTAL, label=u"Minimum quality")
        self.qmin.grid(row=6, column=0, columnspan=2, sticky="WE", padx=5, pady=2)
        self.qmin.set(2)

        # max quality

        self.qmax = Tkinter.Scale(video, from_=-1, to=1024, orient=Tkinter.HORIZONTAL, label=u"Maximum quality")
        self.qmax.grid(row=7, column=0, columnspan=2, sticky="WE", padx=5, pady=2)
        self.qmax.set(31)



        # Audio options

        audio = Tkinter.LabelFrame(self, text=u"Audio options")
        audio.grid(row=3, column=1, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        # audio codec

        vcodecLbl = Tkinter.Label(audio, text=u"Audio codec")
        vcodecLbl.grid(row=0, column=0, sticky="E", padx=5, pady=2)

        self.acodecVar = Tkinter.StringVar()
        self.acodecList = Tkinter.OptionMenu(audio, self.acodecVar, *self.acodecs)
        self.acodecList.grid(row=0, column=1, sticky="W", padx=5, pady=2)

        # Audio frequency

        arLbl = Tkinter.Label(audio, text=u"Audio frequency")
        arLbl.grid(row=1, column=0, sticky="E", padx=5, pady=2)

        self.arVar = Tkinter.IntVar()
        self.ar = Tkinter.Entry(audio,textvariable=self.arVar)
        self.ar.grid(row=1, column=1, sticky="W", pady=2)

        # Audio bitrate

        abLbl = Tkinter.Label(audio, text=u"Audio bitrate")
        abLbl.grid(row=2, column=0, sticky="E", padx=5, pady=2)

        self.abVar = Tkinter.StringVar()
        self.abVar.set(0)
        self.ab = Tkinter.Entry(audio, textvariable=self.abVar)
        self.ab.grid(row=2, column=1, sticky="W", padx=5, pady=2)



        # Options

        options = Tkinter.LabelFrame(self, text=u"Options")
        options.grid(row=4, columnspan=2, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


        # Format

        formatLbl = Tkinter.Label(options, text=u"Format")
        formatLbl.grid(row=0, column=0, sticky="E", padx=5, pady=2)

        self.formatVar = Tkinter.StringVar()
        self.formatList = Tkinter.OptionMenu(options, self.formatVar, *self.formats)
        self.formatList.grid(row=0, column=1, sticky="W", padx=5, pady=2)

        # Format options

        extraOptionsLbl = Tkinter.Label(options, text="Extra options")
        extraOptionsLbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)

        self.extraOptionsVar = Tkinter.StringVar()
        extraOptionsTxt = Tkinter.Entry(options, textvariable=self.extraOptionsVar, width="65")
        extraOptionsTxt.grid(row=1, column=1, sticky="WE", pady=3)



        # Encode button

        encodeButton = Tkinter.Button(self, text=u"Encode", command=self.OnEncodeClick)
        encodeButton.grid(row=5, column=0, sticky='NWES', padx=5, pady=2)

        # Progress bar

        self.progress = ttk.Progressbar(self, orient='horizontal', mode="determinate")
        self.progress.grid(row=5, column=1, sticky="WE", padx=5, pady=3)



    def OnInputBrowseClick(self):
        self.inputFiles = askopenfilename(multiple=True)
        self.inputFileVar.set(self.inputFiles)

    def OnOutputBrowseClick(self):
        options = {}
        options['parent'] = self

        inputFilename = self.inputFileVar.get()
        if inputFilename:
            options['initialfile'] = inputFilename

        self.outputFile = asksaveasfilename()

        self.outputFileVar.set(self.outputFile)

    def OnPresetSelected(self, *argv):
        preset = self.presetsVar.get()
        if self.presets[preset]:
            preset = self.presets[preset]
            self.vcodecVar.set(preset['vcodec'])
            self.vbVar.set(preset['vb'])
            self.widthVar.set(preset['width'])
            self.heightVar.set(preset['height'])
            self.qmax.set(preset['qmax'])
            self.qmin.set(preset['qmin'])
            self.pixfmtVar.set(preset['pix_fmt'])
            self.acodecVar.set(preset['acodec'])
            self.arVar.set(preset['ar'])
            self.abVar.set(preset['ab'])
            self.formatVar.set(preset['format'])
            self.extraOptionsVar.set(preset['extraOptions'])

    def OnEncodeClick(self):
        if self.inputFiles:
            files = self.splitlist(self.inputFiles)
            for filename in files:
                self.encodeFile(filename)
        else:
            tkMessageBox.showwarning(u"No source selected", u"You must define at least one file to encode")


    def encodeFile(self, filename):
        output = self.outputFileVar.get()
        format = self.formatVar.get()
        vcodec = self.vcodecVar.get()
        vb = self.vbVar.get()
        fps = self.fpsVar.get()
        qmax = self.qmax.get()
        qmin = self.qmin.get()
        pixfmt = self.pixfmtVar.get()
        width = self.widthVar.get()
        height = self.heightVar.get()
        acodec = self.acodecVar.get()
        ar = self.arVar.get()
        ab = self.abVar.get()
        extraOptions = self.extraOptionsVar.get()

        cmd = 'ffmpeg -i {0} -y {1} -f {2}'.format(filename, output, format)
        video = '-vcodec {0} -vb {1} -qmax {2} -qmin {3} -pix_fmt {4}'.format(vcodec, vb, qmax, qmin, pixfmt)
        if fps:
            video += ' -r {}'.format(fps)
        scale = '-vf "scale=iw*min({0}/iw\,{1}/ih):ih*min({0}/iw\,{1}/ih),pad={0}:{1}:({0}-iw)/2:({1}-ih)/2"'.format(width, height)
        audio = '-acodec {0} -ar {1} -ab {2}'.format(acodec, ar, ab)
        options = '-strict experimental -threads 0' + ' ' + extraOptions
        cmd = cmd + ' ' + video + ' ' + scale + ' ' + audio + ' ' + options
        # print cmd

        cmd = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        fcntl.fcntl(
            cmd.stderr.fileno(),
            fcntl.F_SETFL,
            fcntl.fcntl(
                cmd.stderr.fileno(),
                fcntl.F_GETFL
            ) | os.O_NONBLOCK,
        )

        duration = None
        header = ""
        progress_regex = re.compile(
            "frame=.*time=([0-9\:\.]+)",
            flags=re.IGNORECASE
        )
        header_received = False

        while True:
            progressline = select.select([cmd.stderr.fileno()], [], [])[0]
            if progressline:
                line = cmd.stderr.read()
                if line == "":
                    self.complete_callback()
                    break
                progress_match = progress_regex.match(line)
                if progress_match:
                    if not header_received:
                        header_received = True

                        if re.search(
                            ".*command\snot\sfound",
                            header,
                            flags=re.IGNORECASE
                        ):
                            tkMessageBox.showerror(u"Command error", u"Command not found")

                        if re.search(
                            "Unknown format",
                            header,
                            flags=re.IGNORECASE
                        ):
                            tkMessageBox.showerror(u"Unknown format", u"Unknown format")

                        if re.search(
                            "Duration: N\/A",
                            header,
                            flags=re.IGNORECASE | re.MULTILINE
                        ):
                            tkMessageBox.showerror(u"Unreadable file", u"Unreadable file")

                        raw_duration = re.search(
                            "Duration:\s*([0-9\:\.]+),",
                            header
                        )
                        if raw_duration:
                            units = raw_duration.group(1).split(":")
                            duration = (int(units[0]) * 60 * 60 * 1000) + (int(units[1]) * 60 * 1000) + int(float(units[2]) * 1000)

                    if duration:
                        units = progress_match.group(1).split(":")
                        progress = (int(units[0]) * 60 * 60 * 1000) + (int(units[1]) * 60 * 1000) + int(float(units[2]) * 1000)
                        self.progress_callback(progress, duration)

                else:
                    header += line

    def progress_callback(self, progress, duration):
        # percent = float(float(progress) / float(duration)) * 100
        # print "{0}%".format(int(percent))
        self.progress["maximum"] = duration
        self.progress["value"] = progress
        self.progress.update()

    def complete_callback(self):
        tkMessageBox.showinfo(u"Encoding complete", u"Encoding complete")


def main():
    app = Application(None)
    app.title("FFmpeg")
    app.mainloop()

if __name__ == "__main__":
    main()

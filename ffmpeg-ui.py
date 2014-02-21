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

        self.vcodecs = [u"libx264"]
        self.acodecs = [u"aac"]
        self.formats = [u"null", u"mov", u"ismv", u"mp3", u"ogg", u"aiff", u"crc", u"framecrc", u"md5", u"framemd5", u"gif", u"hls", u"ico", u"image2", u"matroska", u"mpegts"]

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



        # Video options

        video = Tkinter.LabelFrame(self, text=u"Video options")
        video.grid(row=2, column=0, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)


        # video codec

        vcodecLbl = Tkinter.Label(video, text=u"Video codec")
        vcodecLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.vcodecVar = Tkinter.StringVar()
        self.vcodecVar.set(self.vcodecs[0])
        self.vcodecList = Tkinter.OptionMenu(video, self.vcodecVar, *self.vcodecs)
        self.vcodecList.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Video bitrate

        vbLbl = Tkinter.Label(video, text=u"Video bitrate")
        vbLbl.grid(row=1, column=0, sticky="E", padx=5, pady=2)

        self.vbVar = Tkinter.StringVar()
        self.vbVar.set(u"3500k")
        self.vb = Tkinter.Entry(video,textvariable=self.vbVar)
        self.vb.grid(row=1, column=1, sticky="W", padx=5, pady=2)

        # Video width

        widthLbl = Tkinter.Label(video, text=u"Video width")
        widthLbl.grid(row=2, column=0, sticky="E", padx=5, pady=2)

        self.widthVar = Tkinter.IntVar()
        self.widthVar.set(u"1280")
        self.width = Tkinter.Entry(video,textvariable=self.widthVar)
        self.width.grid(row=2, column=1, sticky="W", padx=5, pady=2)

        # Video height

        heightLbl = Tkinter.Label(video, text=u"Video height")
        heightLbl.grid(row=3, column=0, sticky="E", padx=5, pady=2)

        self.heightVar = Tkinter.IntVar()
        self.heightVar.set(u"720")
        self.height = Tkinter.Entry(video,textvariable=self.heightVar)
        self.height.grid(row=3, column=1, sticky="W", padx=5, pady=2)



        # Audio options

        audio = Tkinter.LabelFrame(self, text=u"Audio options")
        audio.grid(row=2, column=1, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        # audio codec

        vcodecLbl = Tkinter.Label(audio, text=u"Audio codec")
        vcodecLbl.grid(row=0, column=0, sticky="E", padx=5, pady=2)

        self.acodecVar = Tkinter.StringVar()
        self.acodecVar.set(self.acodecs[0])
        self.acodecList = Tkinter.OptionMenu(audio, self.acodecVar, *self.acodecs)
        self.acodecList.grid(row=0, column=1, sticky="W", padx=5, pady=2)

        # Audio frequency

        arLbl = Tkinter.Label(audio, text=u"Audio frequency")
        arLbl.grid(row=1, column=0, sticky="E", padx=5, pady=2)

        self.arVar = Tkinter.IntVar()
        self.arVar.set(u"44100")
        self.ar = Tkinter.Entry(audio,textvariable=self.arVar)
        self.ar.grid(row=1, column=1, sticky="W", padx=5, pady=2)

        # Audio bitrate

        abLbl = Tkinter.Label(audio, text=u"Audio bitrate")
        abLbl.grid(row=2, column=0, sticky="E", padx=5, pady=2)

        self.abVar = Tkinter.StringVar()
        self.abVar.set(u"128k")
        self.ab = Tkinter.Entry(audio, textvariable=self.abVar)
        self.ab.grid(row=2, column=1, sticky="W", padx=5, pady=2)



        # Options

        options = Tkinter.LabelFrame(self, text=u"Options")
        options.grid(row=3, columnspan=2, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


        # Format

        formatLbl = Tkinter.Label(options, text=u"Format")
        formatLbl.grid(row=0, column=0, sticky="E", padx=5, pady=2)

        self.formatVar = Tkinter.StringVar()
        self.formatVar.set(self.formats[0])
        self.formatList = Tkinter.OptionMenu(options, self.formatVar, *self.formats)
        self.formatList.grid(row=0, column=1, sticky="W", padx=5, pady=2)

        # Format options

        formatOptionsLbl = Tkinter.Label(options, text="Format options")
        formatOptionsLbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)

        self.formatOptionsVar = Tkinter.StringVar()
        self.formatOptionsVar.set(u"-movflags faststart");
        formatOptionsTxt = Tkinter.Entry(options, textvariable=self.formatOptionsVar, width="50")
        formatOptionsTxt.grid(row=1, column=1, sticky="WE", pady=3)

        # Format options

        extraOptionsLbl = Tkinter.Label(options, text="Extra options")
        extraOptionsLbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)

        self.extraOptionsVar = Tkinter.StringVar()
        extraOptionsTxt = Tkinter.Entry(options, textvariable=self.extraOptionsVar, width="50")
        extraOptionsTxt.grid(row=2, column=1, sticky="WE", pady=3)



        # Encode button

        encodeButton = Tkinter.Button(self, text=u"Encode", command=self.OnEncodeClick)
        encodeButton.grid(row=4, column=0, sticky='NWES', padx=5, pady=2)

        # Progress bar

        self.progress = ttk.Progressbar(self, orient='horizontal', mode="determinate", length=100)
        self.progress.grid(row=4, column=1, sticky="WE", pady=3)



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
        formatOptions = self.formatOptionsVar.get()
        vcodec = self.vcodecVar.get()
        vb = self.vbVar.get()
        qmax = 51
        qmin = 11
        width = self.widthVar.get()
        height = self.heightVar.get()
        acodec = self.acodecVar.get()
        ar = self.arVar.get()
        ab = self.abVar.get()
        extraOptions = self.extraOptionsVar.get()

        cmd = 'ffmpeg -i {0} -y {1} -f {2} {3}'.format(filename, output, format, formatOptions)
        video = '-vcodec {0} -vb {1} -qmax {2} -qmin {3} -pix_fmt yuv420p -vf "scale=iw*min({4}/iw\,{5}/ih):ih*min({4}/iw\,{5}/ih),pad={4}:{5}:({4}-iw)/2:({5}-ih)/2"'.format(vcodec, vb, qmax, qmin, width, height)
        audio = '-acodec {0} -ar {1} -ab {2}'.format(acodec, ar, ab)
        options = '-strict experimental -threads 0'
        cmd = cmd + ' ' + video + ' ' + audio + ' ' + options + ' ' + extraOptions
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

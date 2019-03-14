# import os
# from os.path import join
from time import sleep
import random

# from streamparse import Spout
import storm

# Define some sentences
SENTENCES = """
the cow jumped over the moon
an apple a day keeps the doctor away
four score and seven years ago
snow white and the seven dwarfs
i am at two with nature
""".strip().split('\n')


class FileReaderSpout(storm.Spout):

    def initialize(self, conf, context):
        self._conf = conf
        self._context = context

        storm.logInfo("Spout instance starting...")

        # TODO:
        # Task: Initialize the file reader

        try:
            f = open(conf['mp4.datafile'], 'r')
            self._f = f
        except Exception as e:
            storm.logInfo("Except: %s" % e)

        # file automatically closed when f goes out of scope

    def nextTuple(self):
        # TODO:
        # Task 1: read the next line and emit a tuple for it
        # Task 2: don't forget to sleep for 1 second when the file is
        #         entirely read to prevent a busy-loop

        line = self._f.readline()

        if line:
            storm.logInfo("Emiting %s" % line)
            storm.emit([line])
        else:
            sleep(1)


FileReaderSpout().run()

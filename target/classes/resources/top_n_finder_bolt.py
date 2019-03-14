import time
import heapq
from collections import Counter

import storm


class WordCountTuple:

    def __init__(self, word, count):
        self.word = word
        self.count = count

    def __cmp__(self, o):
        return self.count > o.count


class TopNFinderBolt(storm.BasicBolt):
    outputs = ['top-N']

    def initialize(self, conf, context):
        self._top_words = Counter()
        self._N = conf.get("mp4.N", 10)
        self._top_N_map = {}
        self._top_N_heap = []

    def process(self, tup):
        # TODO:
        # Task: keep track of the top N words

        word = tup.values[0]
        count = int(tup.values[1])

        new_word_count = WordCountTuple(word, count)

        if word in self._top_N_map:
            if count > self._top_N_map[word].count:
                self._top_N_map[word].count = count
                heapq.heapify(self._top_N_heap)
                storm.logInfo("Update word: %s, count: %d" % (word, count))
        elif len(self._top_N_heap) < self._N:
            self._top_N_map[word] = new_word_count
            heapq.heappush(self._top_N_heap, new_word_count)
            storm.logInfo("Add word: %s, count: %d" % (word, count))
        else:
            smallest_word_count = self._top_N_heap[0]
            storm.logInfo("Current smallest word: %s, count: %d" % (smallest_word_count.word, smallest_word_count.count))

            if count > smallest_word_count.count:
                del(self._top_N_map[smallest_word_count.word])
                self._top_N_map[word] = new_word_count
                heapq.heapreplace(self._top_N_heap, new_word_count)
                storm.logInfo("Add word: %s, count: %d" % (word, count))

        storm.logInfo("Top N: %s" % self.report())
        storm.emit(["top-N", self.report()])

    def report(self):
        words = [word_count.word for word_count in self._top_N_heap]

        return ", ".join(words)


# Start the bolt when it's invoked
TopNFinderBolt().run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2012 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import video_rexps
import re
import logging

log = logging.getLogger("guessit.transfo.guess_video_rexps")


DEPENDS = []
PROVIDES = []


def guess_video_rexps(string):
    for rexp, confidence, span_adjust in video_rexps:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            # is this the better place to put it? (maybe, as it is at least the soonest that we can catch it)
            if 'cdNumberTotal' in metadata and metadata['cdNumberTotal'] is None:
                del metadata['cdNumberTotal']
            return (Guess(metadata, confidence = confidence),
                    (match.start() + span_adjust[0],
                     match.end() + span_adjust[1]))

    return None, None


def process(mtree):
    SingleNodeGuesser(guess_video_rexps, None, log).process(mtree)
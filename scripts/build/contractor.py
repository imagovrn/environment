#!/usr/bin/python2.7
# -*- coding:utf8 -*-

import sys
import re
import argparse

COLOR_RE = r"\x1B\[[0-9;]+m"
NINJA_PROGRESS_RE = r"\[[ 0-9]+%\]"
FILENAME_RE = r'[a-zA-Z0-9_.-]+'
PATH_RE = r'[a-zA-Z0-9_.-\/]+'
STOP_COLOR = '\x1B[0m'

CXX_MATCH = re.compile(
    r'(?P<color>%s)%s.*Building (?:C|CXX) object' % (COLOR_RE, NINJA_PROGRESS_RE))
LINKING_MATCH = re.compile(
    r'(?P<color>%s)%s.*(?P<color_linker>%s)Linking (?:C|CXX) (?:executable|shared library|static library) %s\/('
    r'?P<name>%s)' % (COLOR_RE, NINJA_PROGRESS_RE, COLOR_RE, PATH_RE, FILENAME_RE))
MISC_MATCH = re.compile(
    r'(?P<color>%s)%s.*(Generating|Automatic moc|Creating library symlink)' % (
        COLOR_RE, NINJA_PROGRESS_RE))
WARNING_MATCH = re.compile(r'(?P<color>%s)\s*[Ww]arning:' % COLOR_RE)
NINJA_MATCH = re.compile(r'^(?P<color>%s)%s' % (COLOR_RE, NINJA_PROGRESS_RE))
ICECC_MATCH = re.compile(r'(?P<color>%s)ICECC' % COLOR_RE)
LDPRELOAD_SHIT = re.compile(
    r"from LD_PRELOAD cannot be preloaded \(cannot open shared object file\): ignored\.")

CONTRACTION_STOP_MATCH = re.compile(r'[^a-zA-Z0-9_]?([Ee]rror[:\s]|FAILED|ERROR)[^a-zA-Z0-9_’‘]')
ANY_MATCH = re.compile(r'^')

IGNORE_MATCHES = [ICECC_MATCH, LDPRELOAD_SHIT]


def write(colored, stream=sys.stdout):
    try:
        stream.write(colored)
        stream.flush()

    except IOError:
        try:
            stream.close()
        except IOError:
            pass


def map_write(stream_in, stream_out, function, *args):
    while True:
        try:
            item = stream_in.readline()
        except UnicodeDecodeError:
            continue
        except KeyboardInterrupt:
            break
        if not item:
            break
        write(function(item, *args), stream_out)


class OutputContractor(object):
    def __init__(self, options):
        self._need_newline = False
        self._stop_contracting = False
        self._actions = [
            (WARNING_MATCH, options.warnings, lambda g: g['color'] + "W" + STOP_COLOR),
            (CXX_MATCH, False, lambda g: g['color'] + '.' + STOP_COLOR),
            (MISC_MATCH, False, lambda g: g['color'] + 'M' + STOP_COLOR),
            (LINKING_MATCH, options.linking,
             lambda g: g['color'] + "." + g['color_linker'] + g['name'] + " " + STOP_COLOR),
            (NINJA_MATCH, options.ninja, lambda g: g['color'] + "?" + STOP_COLOR),
            (ICECC_MATCH, False, lambda g: g['color'] + "I" + STOP_COLOR),
            (ANY_MATCH, options.gcc, lambda g: "")
        ]

    def _pass_through(self, s):
        result = ('\n' if self._need_newline else "") + s
        self._need_newline = False
        return result

    def __call__(self, s):
        self._stop_contracting = self._stop_contracting or (
            not any([m.search(s) for m in IGNORE_MATCHES]) and CONTRACTION_STOP_MATCH.search(s))
        if self._stop_contracting:
            return self._pass_through(s)

        for expression, option, result in self._actions:
            match = expression.search(s)
            if match:
                if option:
                    return self._pass_through(s)
                self._need_newline = True
                return result(match.groupdict())
        return self._pass_through(s)


def pass_through(s):
    return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', dest='verbose')
    parser.add_argument('--none', action='store_true', dest='none')

    parser.add_argument('--warnings', action='store_true', dest='warnings')
    parser.add_argument('--linking', action='store_true', dest='linking')
    parser.add_argument('--gcc', action='store_true', dest='gcc')
    parser.add_argument('--ninja', action='store_true', dest='ninja')
    args = parser.parse_args()

    if args.none:
        args.warnings = False
        args.linking = False
        args.gcc = False
        args.ninja = False

    if args.verbose:
        func = pass_through
    else:
        func = OutputContractor(args)
    args = []
    map_write(sys.stdin, sys.stdout, func, *args)

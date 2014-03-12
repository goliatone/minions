#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import zipfile
import re
from os import path
import shutil
import os
from sys import platform
from subprocess import Popen, PIPE, call
from scaffolder.vcs import VCS

#TODO: Shoule we remove Utils and have static methods?
#TODO: Utils.is_binary should be tested!!!
class Utils():
    @classmethod
    def is_binary(cls, path):
        if platform.startswith('win'):
            return cls.is_binary_win(path)
        return cls.is_binary_unx(path)

    @classmethod
    def is_binary_win(cls, path):
        chrs = [7, 8, 9, 10, 12, 13, 27] + range(0x20, 0x100)
        text_chars = ''.join(map(chr, chrs))
        b = open(path).read(1024)
        return bool(b.translate(None, text_chars))

    @classmethod
    def is_binary_unx(cls, path):
        args = ["file", path]
        o = Popen(args, stdout=PIPE).stdout.read()
        return re.search(r'text', o) is None

    @classmethod
    def normalize_path(cls, file_path, mkdir=False):
        file_path = path.realpath(path.expanduser(file_path))
        if mkdir and not path.isdir(file_path):
            os.makedirs(file_path)
        return file_path

def lower_keys(x):
    if isinstance(x, list):
        return [lower_keys(v) for v in x]
    if isinstance(x, dict):
        return dict((k.lower(), lower_keys(v)) for k, v in x.iteritems())
    return x

def import_class(class_path):
    """
    Imports a class from a string.
    @param class_path:
    @return: @raise Exception:
    """
    segments = class_path.split('.')
    module = '.'.join(segments[:-1])
    class_name = segments[-1]
    try:
        module = __import__(module, {}, {}, [class_name])
    except ImportError, err:
        msg = "There was problem while trying to import class. "\
            "Original error was:\n%s" % err
        raise Exception(msg)
    Class = getattr(module, class_name)

    return Class

def clone_url(src, tgt=None):
    if not ".git" in src:
        return src, tgt

    if not tgt:
        tgt = tempfile.mkdtemp()

    vcs = VCS(src)
    vcs.clone(target_dir=tgt)

    return src, tgt

def extract_directory(src, tgt=None, remove=False):
    if not ".zip" in src:
        return src, tgt

    if not tgt:
        tgt = tempfile.mkdtemp()

    with zipfile.ZipFile(src, "r") as z:
        z.extractall(tgt)

    junk = os.path.join(tgt, '__MACOSX/')
    if os.path.isdir(junk):
        shutil.rmtree(junk)

    if remove:
        try:
            file = os.path.join(tgt, os.path.basename(src))
            print "SRC {}".format(src)
            print "TGT {}".format(tgt)
            print "REMOVING FILE {}".format(file)
            os.remove(file)
        except OSError, e:
            print e
            pass

    return src, tgt

def cp_recursive(source, target):
    call(["cp", "-R", source, target])

def commonprefix(l):
    # this unlike the os.path.commonprefix version
    # always returns path prefixes as it compares
    # path component wise
    cp = []
    ls = [p.split('/') for p in l]
    ml = min( len(p) for p in ls )

    for i in range(ml):

        s = set( p[i] for p in ls )
        if len(s) != 1:
            break

        cp.append(s.pop())

    return '/'.join(cp)

def assert_path(path, exception, message):
    if not os.path.isdir(path):
        raise exception(message)

def get_value_or(value, default):
    if not value:
        return default
    return value



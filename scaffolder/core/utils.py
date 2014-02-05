#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import zipfile
import re
from os import path
import os
from sys import platform
from subprocess import Popen, PIPE
from scaffolder.vcs import VCS


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
        args = ["file", '-i', '-b', path]
        o = Popen(args, stdout=PIPE).stdout.read()
        return re.search(r'text', o) is None

    @classmethod
    def normalize_path(cls, file_path, mkdir=False):
        file_path = path.realpath(path.expanduser(file_path))
        if mkdir and not path.isdir(file_path):
            os.makedirs(file_path)
        return file_path



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

def clone_url(src_path, tgt_path=None):
    if not ".git" in src_path:
        return src_path, tgt_path

    if not tgt_path:
        tgt_path = tempfile.mkdtemp()

    vcs = VCS()
    vcs.clone(url=src_path, target_dir=tgt_path)

    return src_path, tgt_path

def extract_directory(src_path, tgt_path=None):
    if not ".zip" in src_path:
        return src_path, tgt_path

    if not tgt_path:
        tgt_path = tempfile.mkdtemp()

    with zipfile.ZipFile(src_path, "r") as z:
        z.extractall(tgt_path)

    return src_path, tgt_path
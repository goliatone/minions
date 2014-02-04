#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import zipfile
from scaffolder.vcs import VCS


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
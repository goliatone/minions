
def import_class(class_path):
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
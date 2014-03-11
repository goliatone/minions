#!/usr/bin/env python
# -*- coding: utf-8 -*-
from promptly import Form, console
import yaml, json, os, sys


def run():
     # Build our form
    form = Form()

    filename = os.path.join(os.path.dirname(__file__), 'form.yaml')

    with open(filename, 'r') as file:
        metadata = yaml.load(file.read())

    prefix = metadata.pop('prefix', '[configure] ')
    getattr(form.add, 'notification')(metadata.pop('notification', 'Configure:'))

    for field, value in metadata.iteritems():
        type = value.pop('type', 'string')
        prompt = value.pop('prompt', 'Value for %s' % field)
        getattr(form.add, type)(field, prompt, **value)

    console.run(form, prefix=prefix)

    return dict(form)


def output(content, output_name='output.json'):
    filename = os.path.join(os.path.dirname(__file__), output_name)

    with open(filename, 'w') as file:
        json.dump(content, file)

    print(content)


def main():
    if len(sys.argv) > 1:
        output_name = sys.argv[1]

    data = run()
    output(data, output_name=output_name)

if __name__ == '__main__':
    main()

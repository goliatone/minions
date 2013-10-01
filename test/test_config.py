from nose.tools import assert_equals
from nose.tools import raises
import os
# We need to include the core library...
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
##

from bootstrapper import Config


CONFIG = [('autor', 'goliatone'),
          ('email', 'hello@goliatone.com'),
          ('github', 'goliatone')]


class TestConfig():
    def setUp(self):
        self.config = self.create_config_fixture()
        pass

    def create_config_fixture(self):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'fixtures/.tmplater')
        self.fixture_path = path
        f = open(path, 'r')
        out = f.read()
        f.close()
        return out

    def test_load_config(self):
        assert_equals(1, 1)

    def test_no_context_file(self):
        pass

    def test_edit(self):
        pass

    def test_list(self):
        self.config = Config(self.fixture_path)
        assert_equals(self.config.list(), CONFIG)

    def test_dump(self):
        pass

    def test_read(self):
        pass

    def test_load(self):
        pass

    def test_merge(self):
        pass

""" Test suite for the core._config module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from yaml import dump

import pytest
from pyapp.core.config import *  # tests __all__


class YamlConfigTest(object):
    """ Test suite for the YamlConfig class.

    """
    @classmethod
    @pytest.fixture
    def files(cls, tmp_path):
        """ Write config files for testing.

        """
        configs = (
            (tmp_path / "empty.yml", None),
            (tmp_path / "conf1.yml", {"global": "%x1;", "%x1;": "%x1;"}),
            (tmp_path / "conf2.yml", {"global": "%x2;", "%x2;": "%x2;"}),
        )
        for path, values in configs:
            path.write_text(dump(values))
        return tuple(path for path, _ in configs)

    def test_item(self):
        """ Test item access.

        """
        config = YamlConfig()
        config["root"] = {}
        config["root"]["key"] = "value"
        assert config["root"]["key"] == "value"
        return

    def test_attr(self):
        """ Test attribute access.

        """
        config = YamlConfig()
        config.root = {}
        config.root.key = "value"
        assert config.root.key == "value"
        return

    @pytest.mark.parametrize("root", (None, "root"))
    def test_init(self, files, root):
        """ Test the __init__() method for loading a file.
        
        """
        merged = {"global": "conf2", "conf1": "conf1", "conf2": "conf2"}
        macros = {"x1": "conf1", "x2": "conf2"}
        config = YamlConfig(files, root, macros)
        if root:
            assert config == {root: merged}
        else:
            assert config == merged
        return

    @pytest.mark.parametrize("root", (None, "root"))
    def test_load(self, files, root):
        """ Test the load() method.

        """
        merged = {"global": "conf2", "conf1": "conf1", "conf2": "conf2"}
        macros = {"x1": "conf1", "x2": "conf2"}
        config = YamlConfig()
        config.load(files, root, macros)
        if root:
            assert config == {root: merged}
        else:
            assert config == merged
        return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

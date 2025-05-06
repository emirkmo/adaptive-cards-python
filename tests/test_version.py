"""Check that basic version functionality works"""
from adaptive_cards_python import __version__ as package_version

def test_package_version():
    assert package_version != ""
    assert isinstance(package_version, str)
    assert package_version.count(".")==2

if __name__ == "__main__":
    test_package_version()

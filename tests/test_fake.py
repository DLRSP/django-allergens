"""Backward-compatible smoke tests (package import + version)."""

import allergens as pkg


def test_import_package():
    assert pkg.__title__ == "allergens"


def test_version_is_semver_like():
    assert pkg.__version__
    assert pkg.__version__.count(".") >= 2
    assert pkg.VERSION == pkg.__version_info__

from pytest import raises
from pytest_mock import MockerFixture

from logikal_browser.install import install_all


def test_install_all(mocker: MockerFixture) -> None:
    versions = {'chrome': 'chrome_test', 'edge': 'edge_test'}
    browsers = mocker.patch('logikal_browser.install.InstalledBrowser.BROWSERS')
    install_all(versions=versions)
    browser_version = browsers.__getitem__.return_value.version_class
    browser_version.assert_any_call(version=versions['edge'], install=True)
    browser_version.assert_any_call(version=versions['chrome'], install=True)


def test_install_all_errors() -> None:
    with raises(RuntimeError, match='specify at least one browser version'):
        install_all(versions={})

    invalid = 'invalid-browser-name'
    with raises(RuntimeError, match=f'"{invalid}" .* not supported'):
        install_all(versions={invalid: 'version'})

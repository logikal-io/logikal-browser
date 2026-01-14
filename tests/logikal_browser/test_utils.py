from pathlib import Path

from PIL import Image
from pytest import raises
from pytest_mock import MockerFixture

from logikal_browser import utils


def test_expected_not_found(tmp_path: Path, mocker: MockerFixture) -> None:
    tty = mocker.patch('logikal_browser.utils.sys.stdin.isatty')
    run = mocker.patch('logikal_browser.utils.run')
    input_keys = mocker.patch('logikal_browser.utils.input')

    # Non-interactive
    tty.return_value = False
    with raises(AssertionError, match='file does not exist'):
        utils.assert_image_equal(b'', tmp_path / 'non_interactive', image_tmp_path=tmp_path)
    assert (tmp_path / 'actual.png').is_file()

    # Interactive
    tty.return_value = True
    expected = tmp_path / 'interactive.png'

    input_keys.side_effect = 'c'  # opening canceled
    with raises(AssertionError, match='canceled'):
        utils.assert_image_equal(b'', expected, image_tmp_path=tmp_path)
    assert not run.called
    assert not expected.is_file()

    input_keys.side_effect = ['s', '']  # opening skipped, rejected
    with raises(AssertionError, match='rejected'):
        utils.assert_image_equal(b'', expected, image_tmp_path=tmp_path)
    assert not run.called
    assert not expected.is_file()

    input_keys.side_effect = ['', 'accept']  # opened and accepted
    utils.assert_image_equal(b'', expected, image_tmp_path=tmp_path)
    assert expected.is_file()
    assert run.called


def test_difference(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch('logikal_browser.utils.sys.stdin.isatty', return_value=False)
    screenshots = Path(__file__).parent / 'screenshots'

    actual = screenshots / 'test_check_perennrose_desktop_en-us_chrome.png'
    expected = screenshots / 'test_check_nincs-ido_desktop_en-us_chrome.png'
    with raises(AssertionError, match='differs'):
        utils.assert_image_equal(actual.read_bytes(), expected, image_tmp_path=tmp_path)

    actual = tmp_path / 'diff.png'
    expected = screenshots / 'difference.png'
    with Image.open(actual) as actual_image, Image.open(expected) as expected_image:
        assert actual_image == expected_image, '\n'.join([
            'Incorrect difference', f'  Actual: file://{actual}', f'  Expected: file://{expected}',
        ])


def test_no_opener(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch('logikal_browser.utils.Path.exists', return_value=False)
    mocker.patch('logikal_browser.utils.sys.stdin.isatty', return_value=True)
    mocker.patch('logikal_browser.utils.input', return_value='reject')
    with raises(AssertionError, match='rejected'):
        utils.save_image_prompt(message='Test message', source=tmp_path, destination=tmp_path)

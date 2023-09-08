"""Module to get localisated data, especially text data"""
from pathlib import Path
import logging
import yaml

from . import __settings as settings

_logger = logging.getLogger(__name__)


_project_folder = Path(__file__).parent
_language_file = Path(_project_folder, "languages", settings.LANGUAGE).with_suffix(
    ".yaml"
)

with _language_file.open("r", encoding="UTF-8") as file:
    _data = yaml.load(file, Loader=yaml.CLoader)
    _language_name = _data["language"]
    _language_original_name = _data["language-origin"]
    _missing_language_message = _data["missing-local"]
    _texts = _data["texts"]


def get_text(*args):
    """
    Method to get localized text from the corresponding text file in the folder languages
    following the internal path of ``args``

    :param args: the path of the textfile in the languages files found in the folder languages
    :return: A string of the localized version of the references text.
    """
    current = _texts
    try:
        for arg in args:
            current = current[arg]
    except KeyError as _:
        _logger.error("Missing Localization for name %s found!", args)
        return _missing_language_message
    if isinstance(current, str):
        return current

    _logger.error("Missing Localization for name %s found!", args)
    return _missing_language_message

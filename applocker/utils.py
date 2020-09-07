import sys

from xml.etree.ElementTree import tostring, fromstring
from applocker.conditions import FilePublisherCondition, FilePathCondition, FileHashCondition
from applocker.rules import FilePublisherRule, FilePathRule, FileHashRule
from applocker.policy import AppLockerPolicy


def dump(element, stream):
    stream.write(dumps(element))


def dumps(element):
    return tostring(element).decode('utf-8')


def load(stream):
    return loads(stream.read())


def loads(string):
    element = fromstring(string)
    return getattr(sys.modules[__name__], element.tag).from_element(element)

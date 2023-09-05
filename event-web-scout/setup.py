from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="event_web_scout",
    version='{{VERSION_PLACEHOLDER}}',
    author="Aleksandr Klimov",
    author_email="2767789+geeeezmo@users.noreply.github.com",
    description="Extendable package for collecting events from the web and adding them to Google calendars",
    url = "https://github.com/geeeezmo/event-web-scout",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
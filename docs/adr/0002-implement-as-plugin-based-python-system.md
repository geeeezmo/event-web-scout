# 2. Implement as plugin based Python system

Date: 2024-04-05

## Status

Accepted

## Context

List of tracked event sources can be very different from installation to installation.
It would be convenient to be able to easily configure where the events are collected from.

## Decision

Implement the system as a Python package that has minimal code at its core, and all the different parsers/scrapers are installed separately as plugins and discovered automatically.
Use Python's [entry points](https://packaging.python.org/en/latest/specifications/entry-points/) for plugin discovery (a [good article](https://dev.to/demianbrecht/entry-points-in-python-34i3) about entry points).
Provide simple extendable classes as bases for plugins out-of-the-box (e.g. "HTML page scraper" or "ICalendar parser").

## Consequences

As a result of reducing the amount of core source code, the package will be smaller in size.
The plugin architecture will simplify adding new features (related to event sources, e.g. new source type), as they can be implemented independently from the core.

# 3. Publish core and plugin examples as packages to PyPi

Date: 2024-04-05

## Status

Accepted

## Context

The core package, as well as the plugin examples, must be available for installing via Python package managers.

## Decision

Publish the core and plugin examples (as separate packages) to PyPi.
Use GitHub Actions to do so (publish when a Git tag is created).

## Consequences

Once set up, the publishing process [hopefully] never has to be revisited.

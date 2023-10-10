# Changelog
All notable changes to this project from version 0.4.0 upwards are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.6.0] – 2023-10-10

### Added
- Support for Python 3.11 and 3.12
- Classes to track issues (ported from Kolasu)

### Changed
- Updated ANTLR runtime to 4.11.1

### Fixed
- `internal_field` on Python 3.10+

## [0.5.0] – 2023-09-06

### Added
- AST transformers, aligned with the latest Kolasu 1.5.x version
- `assert_asts_are_equal` function to support writing assertions in a test suite
- documentation generation (published on https://pylasu.readthedocs.io)
- export more symbols

### Changed
- Alignment with Kolasu:
  - `PropertyDescriptor` renamed to `PropertyDescription` 
  - `Node.properties` generates `PropertyDescription` instances rather than tuples

### Fixed
- `PossiblyNamed` implementation
- `Concept.node_properties`

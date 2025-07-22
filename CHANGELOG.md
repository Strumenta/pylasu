# Changelog
All notable changes to this project from version 0.4.0 upwards are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.9.0] – Not yet released

### Added
- `PylasuANTLRParser` class modeled after the Kolasu equivalent

## [0.8.1] – 2025-02-21

### Added
- More reflection to support PEP-0563 in a Cython environment

## [0.8.0] – 2025-02-20

### Added
- Support for string-encoded types (PEP-0563)

## [0.7.3] – 2025-01-13

### Changed
- More type-safe signature for `find_ancestor_of_type`

### Fixed
- `provides_nodes` for optional and union types

## [0.7.2] – 2024-11-07

### Added
- Case-insensitive symbol lookup

### Changed
- Improved performance of `Concept.is_node_property` 

### Fixed
- inheritance of internal properties

## [0.7.1] – 2024-05-16

### Fixed
- `ParserRuleContext.to_position` extension method when the input stream is empty

## [0.7.0] – 2023-11-21

### Added
- `Point.isBefore` method as in Kolasu

### Fixed
- Bug in the deserialization of Result

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

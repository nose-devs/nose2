# Change Log
All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## [0.6.0] - 2016-14-02
### Added
- Junit XML report support properties (64b78ff627b45870c623c1a8344fbdfb30a3b747)
- Improve test coverage
- Improve CI 
- Add a `createdTestSuite` event, fired after test loading (b9e91a6846ee2dab05ebf6d0e8291ed5c3c897d4)

### Fixed
- junit-xml plugin fixed on windows (f35c04886cac91c70e5d637fc4042042111f3ec9)
- ensure tests are importable before trying to load them (5df9a70fe7089b49f42e5ac38a88847b0ba48473)
- fail test instead of skipping it, when setup fails (1459515d2237c01b8e5eab3bf0f3d75c001d4e3c)
- when test loading fails, provide the origin traceback (a83d780c836692e51e93a4699b50097ae66770ff)
- make the collect plugin work with layers (61fc6bc84eac94d737b96ccc9e815638a8bd143b)
- fix coverage plugin to take import-time coverage into account (268371d815fb319bda4489da9756843204354eab)

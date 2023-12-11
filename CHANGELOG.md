# CHANGELOG



## v0.19.3 (2023-12-11)

### Ci

* ci: fix docker image p3.12 issue (#32)

* ci: pin docker py version due to napalm py3.12 issue

* ci: remove unnecessary dependency ([`737be8a`](https://github.com/adamkirchberger/nectl/commit/737be8a205eca6b0ea047a60d69cbb63e7312da1))

### Fix

* fix: update poetry (#33) ([`ac53ded`](https://github.com/adamkirchberger/nectl/commit/ac53dedbddc9166e35c2e56e108e28853345464d))


## v0.19.2 (2023-12-11)

### Fix

* fix: Allow pydantic2 versions and version fix (#31)

* fix: allow newer pydantic versions

* chore: update gitignore

* ci: version bump fix ([`dfb2fd4`](https://github.com/adamkirchberger/nectl/commit/dfb2fd4d9e70681f535f74ac5ab66823b71dd568))


## v0.19.1 (2023-11-21)

### Fix

* fix: broken release due to missing dependency (#29)

* fix: semantic release variable bumping

* chore: update dependencies

* feat: run validation checks on hosts using pytest

* test: add test for api get hosts

* fix: disable pytest warnings on checks

* test: show test output when assert fails

* fix: checks list order

* fix: broken release due to missing dependency

---------

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`45f381f`](https://github.com/adamkirchberger/nectl/commit/45f381fdc2876134c4a7e61eba7cd0e4c046bb2d))


## v0.19.0 (2023-11-21)

### Feature

* feat: add checks feature (#28)

* fix: semantic release variable bumping

* chore: update dependencies

* feat: run validation checks on hosts using pytest

* test: add test for api get hosts

* fix: disable pytest warnings on checks

* test: show test output when assert fails

* fix: checks list order

---------

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`3389c6c`](https://github.com/adamkirchberger/nectl/commit/3389c6c018e5348f91ea5bee863df03963fd057c))


## v0.18.3 (2023-11-14)

### Fix

* fix: cli total diff to count created diff files (#27)

* fix: cli total diff to count created diff files

* fix: remove blank homepage ([`af82f86`](https://github.com/adamkirchberger/nectl/commit/af82f866d624431c175e50463c62aca1b44c2e99))


## v0.18.2 (2023-10-30)

### Fix

* fix: use pydantic v1 settings when v2 installed (#26) ([`7c16bc1`](https://github.com/adamkirchberger/nectl/commit/7c16bc125d8dbe121b4407d763dee1080fdebd69))


## v0.18.1 (2023-10-30)

### Fix

* fix(deps): bump cryptography from 41.0.3 to 41.0.4 (#20)

Bumps [cryptography](https://github.com/pyca/cryptography) from 41.0.3 to 41.0.4.
- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pyca/cryptography/compare/41.0.3...41.0.4)

---
updated-dependencies:
- dependency-name: cryptography
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: Adam Kirchberger &lt;24639394+adamkirchberger@users.noreply.github.com&gt; ([`8c6d0b6`](https://github.com/adamkirchberger/nectl/commit/8c6d0b6231bfaf19a41807627c1e0537a2d540ab))


## v0.18.0 (2023-10-30)

### Feature

* feat: discovered hosts returned as dict (#25)

* feat: discovered hosts returned as dict ([`62ef067`](https://github.com/adamkirchberger/nectl/commit/62ef067ae25f23a41a34eb0556572dcd8caed6b3))


## v0.17.1 (2023-10-24)

### Fix

* fix: configs get command not fetching backups (#24) ([`eee07fc`](https://github.com/adamkirchberger/nectl/commit/eee07fc8c80474fd8bc0d4a75e4f6d65013835d6))


## v0.17.0 (2023-10-24)

### Feature

* feat: add external api and ssh key argument (#23)

* feat: add nectl api to allow integration into other tools

* fix: add ssh private key argument

* refactor: types and docstrings

* chore: remove eol python3.7 and update lock deps

* fix: dpath and pydantic new version changes ([`1107ac4`](https://github.com/adamkirchberger/nectl/commit/1107ac4caf5e76fc584490da7943179ccaf05d4f))


## v0.16.3 (2023-08-26)

### Chore

* chore(deps): bump requests from 2.28.1 to 2.31.0 (#16)

Bumps [requests](https://github.com/psf/requests) from 2.28.1 to 2.31.0.
- [Release notes](https://github.com/psf/requests/releases)
- [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
- [Commits](https://github.com/psf/requests/compare/v2.28.1...v2.31.0)

---
updated-dependencies:
- dependency-name: requests
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: Adam Kirchberger &lt;24639394+adamkirchberger@users.noreply.github.com&gt; ([`43a3f13`](https://github.com/adamkirchberger/nectl/commit/43a3f134945557f9bf45c12a943ad40b5b337c00))

### Fix

* fix(deps): bump cryptography from 37.0.2 to 41.0.3 (#17)

Bumps [cryptography](https://github.com/pyca/cryptography) from 37.0.2 to 41.0.3.
- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pyca/cryptography/compare/37.0.2...41.0.3)

---
updated-dependencies:
- dependency-name: cryptography
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: Adam Kirchberger &lt;24639394+adamkirchberger@users.noreply.github.com&gt; ([`e053c23`](https://github.com/adamkirchberger/nectl/commit/e053c231b16b207dbec1fe2d7ebf6a537d6fdf85))


## v0.16.2 (2023-08-26)

### Chore

* chore(deps): bump certifi from 2022.12.7 to 2023.7.22

Bumps [certifi](https://github.com/certifi/python-certifi) from 2022.12.7 to 2023.7.22.
- [Commits](https://github.com/certifi/python-certifi/compare/2022.12.07...2023.07.22)

---
updated-dependencies:
- dependency-name: certifi
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`276c638`](https://github.com/adamkirchberger/nectl/commit/276c6388092928f2cdf902ed5b08112b99b8d985))

* chore(deps): bump certifi from 2022.6.15 to 2022.12.7

Bumps [certifi](https://github.com/certifi/python-certifi) from 2022.6.15 to 2022.12.7.
- [Release notes](https://github.com/certifi/python-certifi/releases)
- [Commits](https://github.com/certifi/python-certifi/compare/2022.06.15...2022.12.07)

---
updated-dependencies:
- dependency-name: certifi
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`63a44de`](https://github.com/adamkirchberger/nectl/commit/63a44de2d520209c14be4ca3cfb2e00746bbb619))

### Ci

* ci: update release ([`135527e`](https://github.com/adamkirchberger/nectl/commit/135527e9cfda4c04c7d02f07e232f5ada1fab447))

* ci: update workflows ([`bd7d7bc`](https://github.com/adamkirchberger/nectl/commit/bd7d7bc0fe27dabf9f64c7e02352e67438df758e))

### Documentation

* docs: correct kit config file name ([`fd8345a`](https://github.com/adamkirchberger/nectl/commit/fd8345aeb04f95d9aa9c1f4e86259ed82fe58147))

* docs: add mention of napalm driver ([`42a5deb`](https://github.com/adamkirchberger/nectl/commit/42a5deb1f2750415b569739cf455590893d7aa94))

### Fix

* fix(deps): bump future from 0.18.2 to 0.18.3 (#18)

Bumps [future](https://github.com/PythonCharmers/python-future) from 0.18.2 to 0.18.3.
- [Release notes](https://github.com/PythonCharmers/python-future/releases)
- [Changelog](https://github.com/PythonCharmers/python-future/blob/master/docs/changelog.rst)
- [Commits](https://github.com/PythonCharmers/python-future/compare/v0.18.2...v0.18.3)

---
updated-dependencies:
- dependency-name: future
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: Adam Kirchberger &lt;24639394+adamkirchberger@users.noreply.github.com&gt; ([`8d92db3`](https://github.com/adamkirchberger/nectl/commit/8d92db31e700b323d308ee828a9cfdff0eb7c2a1))


## v0.16.1 (2022-10-18)

### Chore

* chore(deps): bump lxml from 4.9.0 to 4.9.1 (#7)

Bumps [lxml](https://github.com/lxml/lxml) from 4.9.0 to 4.9.1.
- [Release notes](https://github.com/lxml/lxml/releases)
- [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt)
- [Commits](https://github.com/lxml/lxml/compare/lxml-4.9.0...lxml-4.9.1)

---
updated-dependencies:
- dependency-name: lxml
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`ab6db69`](https://github.com/adamkirchberger/nectl/commit/ab6db69d866d87f0913beb38b3c986d1fd5eac45))

### Ci

* ci: fix wheel package build ([`37b7c40`](https://github.com/adamkirchberger/nectl/commit/37b7c40645a1434d044070ce337630ca8925b9c5))

### Documentation

* docs: fix broken link to example kit ([`7214df8`](https://github.com/adamkirchberger/nectl/commit/7214df8457e1756d83cdcf4b7566fbcd418ec932))

### Fix

* fix: configs file extension setting not being used ([`3c83c0a`](https://github.com/adamkirchberger/nectl/commit/3c83c0a5ed2a1dbe942b318e247f89a20e4bd294))

### Unknown

* 0.16.1

Automatically generated by python-semantic-release ([`aa1c644`](https://github.com/adamkirchberger/nectl/commit/aa1c644350c9ebc61f5d60422c123084f817cd1b))


## v0.16.0 (2022-07-17)

### Feature

* feat: Add napalm driver integration (#8)

* feat: add format and sanitize options for active config

* feat: add napalm driver

* refactor: replace junos driver with napalm driver

* feat: add driver support for arista eos using napalm

* feat: add option to use default driver

* refactor: trim log line to fit line length

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`792ca97`](https://github.com/adamkirchberger/nectl/commit/792ca978c99edd3077095551c32ecb3b3af6fd5f))

### Unknown

* 0.16.0

Automatically generated by python-semantic-release ([`ef4d82b`](https://github.com/adamkirchberger/nectl/commit/ef4d82bb68bb97f845e370236aa244a5ec2d1408))


## v0.15.6 (2022-06-20)

### Documentation

* docs: add contact form (#5)

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`949af88`](https://github.com/adamkirchberger/nectl/commit/949af88c6847c51742c28168e1ca65117b3e2164))

### Fix

* fix: custom types being ignored if not in list or dict (#6)

* fix: custom types being ignored if not in list or dict

* fix: update dependencies

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`9f72e9c`](https://github.com/adamkirchberger/nectl/commit/9f72e9cfa9b14de00afcc9a762fdc52b7af28359))

### Unknown

* 0.15.6

Automatically generated by python-semantic-release ([`f23ea22`](https://github.com/adamkirchberger/nectl/commit/f23ea228cd1d674ba083a83dd0df47da01d2d2ae))


## v0.15.5 (2022-05-01)

### Documentation

* docs: fix bad character ([`36f2370`](https://github.com/adamkirchberger/nectl/commit/36f237039d7020b72ada6233dc3cdd630ed41655))

* docs: fix changelog (#3)

* docs: add next version placeholder

* docs: replace commit links

* docs: reformat changelog

* docs: fix link to changelog

* docs: add missing changes

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`5cab1be`](https://github.com/adamkirchberger/nectl/commit/5cab1bec4c23af4420b195e23a22cd805341087d))

### Fix

* fix: update dependencies (#4)

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`320583d`](https://github.com/adamkirchberger/nectl/commit/320583d0a1cb39afa8c5911bd6a86411785b29d9))

### Unknown

* 0.15.5

Automatically generated by python-semantic-release ([`4146f0a`](https://github.com/adamkirchberger/nectl/commit/4146f0ae19a34e7796191c335c1357afd4c7dec9))


## v0.15.4 (2022-04-24)

### Documentation

* docs: update example readme ([`4624cad`](https://github.com/adamkirchberger/nectl/commit/4624cad39fcce9fc923c65e7d05d7789b79e3dd5))

### Fix

* fix: readme image ([`680d264`](https://github.com/adamkirchberger/nectl/commit/680d264518dc44be57e04ea6e39795883f587e19))

### Unknown

* 0.15.4

Automatically generated by python-semantic-release ([`bc53e0d`](https://github.com/adamkirchberger/nectl/commit/bc53e0d7af84b72d71df82d38e9ad95a62121862))


## v0.15.3 (2022-04-24)

### Fix

* fix: update broken links and img ([`b8df020`](https://github.com/adamkirchberger/nectl/commit/b8df020b32b42617af16cd1bbd55d11c163c53d9))

### Unknown

* 0.15.3

Automatically generated by python-semantic-release ([`dd385a2`](https://github.com/adamkirchberger/nectl/commit/dd385a246a458a03595d6dd2aa834bce2f43b83f))


## v0.15.2 (2022-04-24)

### Fix

* fix: package documentation link ([`a4bf460`](https://github.com/adamkirchberger/nectl/commit/a4bf460eab17ff34584abe0a20c7fa741e4db0d0))

### Unknown

* 0.15.2

Automatically generated by python-semantic-release ([`15991c5`](https://github.com/adamkirchberger/nectl/commit/15991c50846581c7c69e50727b6551533b557e8f))


## v0.15.1 (2022-04-24)

### Fix

* fix: update readme and docs favicon (#2)

* ci: add github actions config

* fix: update settings version and description

* fix: update readme and project metadata

* docs: add favicon

* ci: remove unused release file

* fix: pyproject conflict mistake

* test: cli version

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`6dbc6ed`](https://github.com/adamkirchberger/nectl/commit/6dbc6ed22a384e5f191686d1a4955859e82f27ae))

### Unknown

* 0.15.1

Automatically generated by python-semantic-release ([`3251a2e`](https://github.com/adamkirchberger/nectl/commit/3251a2e6cb24872c6c6a5a46c6e23ff9805e5a07))


## v0.15.0 (2022-04-24)

### Ci

* ci: add github actions config (#1)

Co-authored-by: Adam Kirchberger &lt;adamkirchberger@users.noreply.github.com&gt; ([`9ddf6b3`](https://github.com/adamkirchberger/nectl/commit/9ddf6b3c52fb02b097dd52697d1a832d87c1da57))

* ci: add dockerfile ([`a60a582`](https://github.com/adamkirchberger/nectl/commit/a60a582d07b98701bf6ad0725c3afd722f0a1b51))

* ci: remove gitlab config ([`a8dddb2`](https://github.com/adamkirchberger/nectl/commit/a8dddb2f83e3033f530278a97351eb998fcea775))

### Documentation

* docs: update docs ([`23a930e`](https://github.com/adamkirchberger/nectl/commit/23a930e4cd6c5c3c371079fcc04b75b3890812c0))

* docs: add docs to repo ([`1c9a7eb`](https://github.com/adamkirchberger/nectl/commit/1c9a7eb0319f5d8f86ad34182eb2cbf023e27448))

* docs: update readme ([`38055f9`](https://github.com/adamkirchberger/nectl/commit/38055f9dd2bfc95221e095cca3639293f64d20fc))

### Feature

* feat: add example demo-kit1 ([`b55e6b0`](https://github.com/adamkirchberger/nectl/commit/b55e6b0304798e99fd2772a6cce6e90b0c3e5437))

### Fix

* fix: host discovery regex ([`7ff0f1a`](https://github.com/adamkirchberger/nectl/commit/7ff0f1ac0e31daacaf6420f42513639405ad731e))

* fix: log attempts to modify frozen facts ([`9f26e13`](https://github.com/adamkirchberger/nectl/commit/9f26e13ec95edb59e671b30696ce5a17b4efa6a0))

* fix: show matched hosts when applying ([`c9bf83b`](https://github.com/adamkirchberger/nectl/commit/c9bf83b44dc5ed7d90aeb1a67f82797d7b08ea46))

* fix: rename test to checks ([`afacfd6`](https://github.com/adamkirchberger/nectl/commit/afacfd62f58b859aa1a4f3354dac3a6e57e9576d))

### Refactor

* refactor: error handling when loading datatree facts ([`07b6147`](https://github.com/adamkirchberger/nectl/commit/07b6147c78608a9fbc6f513560af1252e12fc539))

* refactor: use consistent log message format ([`e17094d`](https://github.com/adamkirchberger/nectl/commit/e17094d519c0a8b71d43db5b6bc5701813dc52cf))

### Unknown

* 0.15.0

Automatically generated by python-semantic-release ([`cfe4b07`](https://github.com/adamkirchberger/nectl/commit/cfe4b073ded7832ae556f285f01c5131b3e06fd9))


## v0.14.0 (2022-04-17)

### Chore

* chore(release): 0.14.0

# [0.14.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.13.1...0.14.0) (2022-04-17)

### Features

* add deployment groups ([417abd4](https://gitlab.com/adamkirchberger/nectl-dev/commit/417abd41b7e3d666ad511974da22adb8c6bd8dfc)) ([`df1b05d`](https://github.com/adamkirchberger/nectl/commit/df1b05da4152f4076cafc81244b5646d5c81bb89))

### Documentation

* docs: add readme ([`950926e`](https://github.com/adamkirchberger/nectl/commit/950926e94f0957f224fc67b4d2a08cbc60fa62b8))

### Feature

* feat: add deployment groups ([`417abd4`](https://github.com/adamkirchberger/nectl/commit/417abd41b7e3d666ad511974da22adb8c6bd8dfc))

### Refactor

* refactor: make test check host values ([`94c0499`](https://github.com/adamkirchberger/nectl/commit/94c04990013c2cb12a75b60d8b41898ab16f61d3))

* refactor: add comments ([`83a5cb6`](https://github.com/adamkirchberger/nectl/commit/83a5cb6cbb997e43b91257baa29c2fd8685d5887))

* refactor: optimize host filtering ([`9297b28`](https://github.com/adamkirchberger/nectl/commit/9297b280b9af787037ba4f73900b059bb1528777))

* refactor: update docstrings ([`60019c0`](https://github.com/adamkirchberger/nectl/commit/60019c0a3098638505fb507bae2b554d655ee4c2))


## v0.13.1 (2022-04-09)

### Chore

* chore(release): 0.13.1

## [0.13.1](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.13.0...0.13.1) (2022-04-09)

### Bug Fixes

* datatree list-hosts json output ([b578a6e](https://gitlab.com/adamkirchberger/nectl-dev/commit/b578a6e9da6b11bb7f1794317193b7c13146fac6)) ([`32f338a`](https://github.com/adamkirchberger/nectl/commit/32f338aabff8adedbf4eebf45cc4b3981a6a2fe6))

### Fix

* fix: datatree list-hosts json output ([`b578a6e`](https://github.com/adamkirchberger/nectl/commit/b578a6e9da6b11bb7f1794317193b7c13146fac6))

### Refactor

* refactor: remove unused imports ([`b371be3`](https://github.com/adamkirchberger/nectl/commit/b371be3dbc4e790c3afe2dfe4670010ef4c7375b))

### Test

* test: add test for driver method invalid host skip ([`c9cf932`](https://github.com/adamkirchberger/nectl/commit/c9cf9329393d80dab50add838dc7c8ed72f8e16d))


## v0.13.0 (2022-04-09)

### Chore

* chore(release): 0.13.0

# [0.13.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.12.0...0.13.0) (2022-04-09)

### Bug Fixes

* add optional user and pass args for config diff ([478b1e4](https://gitlab.com/adamkirchberger/nectl-dev/commit/478b1e49f085bca4d6c59514287201b923105209))
* fetch user and pass from datatree if no args supplied ([20fdd27](https://gitlab.com/adamkirchberger/nectl-dev/commit/20fdd27d36031cede5e1bf4c776ebb6d642e3028))
* skip driver calls when os_name or mgmt_ip missing ([f7bef73](https://gitlab.com/adamkirchberger/nectl-dev/commit/f7bef736e18625a24f07dae611484a3c0517206d))

### Features

* add assume yes flag to config apply cli action ([462f5a8](https://gitlab.com/adamkirchberger/nectl-dev/commit/462f5a8aa07a1f13f0de58b1cc82c723c599eff3))
* add cli facts check only action ([ae4316b](https://gitlab.com/adamkirchberger/nectl-dev/commit/ae4316b8d34f1dcdf86847127212de82d3284111))
* rename data to datatree ([055ae4f](https://gitlab.com/adamkirchberger/nectl-dev/commit/055ae4f759f79ffa9a0ee4e2099534ed22fa3b3e)) ([`b7c18e3`](https://github.com/adamkirchberger/nectl/commit/b7c18e353ee8d3ea104138faf7b912959b76ab48))

* chore: update dependencies ([`273c964`](https://github.com/adamkirchberger/nectl/commit/273c964b4a49c602dbdd8c2c926e56e74042c27f))

### Feature

* feat: add assume yes flag to config apply cli action ([`462f5a8`](https://github.com/adamkirchberger/nectl/commit/462f5a8aa07a1f13f0de58b1cc82c723c599eff3))

* feat: add cli facts check only action ([`ae4316b`](https://github.com/adamkirchberger/nectl/commit/ae4316b8d34f1dcdf86847127212de82d3284111))

* feat: rename data to datatree ([`055ae4f`](https://github.com/adamkirchberger/nectl/commit/055ae4f759f79ffa9a0ee4e2099534ed22fa3b3e))

### Fix

* fix: skip driver calls when os_name or mgmt_ip missing ([`f7bef73`](https://github.com/adamkirchberger/nectl/commit/f7bef736e18625a24f07dae611484a3c0517206d))

* fix: fetch user and pass from datatree if no args supplied ([`20fdd27`](https://github.com/adamkirchberger/nectl/commit/20fdd27d36031cede5e1bf4c776ebb6d642e3028))

* fix: add optional user and pass args for config diff ([`478b1e4`](https://github.com/adamkirchberger/nectl/commit/478b1e49f085bca4d6c59514287201b923105209))

### Refactor

* refactor: update render skip msg to warning ([`dda6bab`](https://github.com/adamkirchberger/nectl/commit/dda6bab955811fb9df3870886234fef04ce0f512))


## v0.12.0 (2022-03-28)

### Chore

* chore(release): 0.12.0

# [0.12.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.11.0...0.12.0) (2022-03-28)

### Bug Fixes

* add Host object to module public attributes ([ea39a4c](https://gitlab.com/adamkirchberger/nectl-dev/commit/ea39a4cded32ef78a3a0d5773f4242f0316b5ec5))
* remove unnecessary compare config parameter ([ccd013f](https://gitlab.com/adamkirchberger/nectl-dev/commit/ccd013f48094c848a82da2189882cabfa4e33ee2))
* update app description ([3f10f84](https://gitlab.com/adamkirchberger/nectl-dev/commit/3f10f84c4abc8375bf9c424a9f331f654d5229e4))
* use IPv4Address type for host mgmt_ip ([9fd76e2](https://gitlab.com/adamkirchberger/nectl-dev/commit/9fd76e228b95be2a4532e3bf73d7c560aaa3a4fa))

### Features

* add action to get active config from host ([89f9334](https://gitlab.com/adamkirchberger/nectl-dev/commit/89f93347ef86081ac4c568ca7a8d0990ab387cdf))
* rename config replace to apply ([dbaae00](https://gitlab.com/adamkirchberger/nectl-dev/commit/dbaae00ada707a807c8d6302d18912f63083ccd7))
* rename default datatree dirname to datatree ([ccbc90d](https://gitlab.com/adamkirchberger/nectl-dev/commit/ccbc90da18bedb0023970d59e4c155dea8f27b7f))
* username and password are host core facts ([720750e](https://gitlab.com/adamkirchberger/nectl-dev/commit/720750e64bbc398fda9a88b410afc0600bce3f9e)) ([`9e8efaf`](https://github.com/adamkirchberger/nectl/commit/9e8efaf4426d17d6d1d0b8bf5fd4460b0891cb62))

* chore: update dependencies ([`9f39db0`](https://github.com/adamkirchberger/nectl/commit/9f39db0a5db8ebd0215d291dd52faf231f7e3d78))

### Feature

* feat: add action to get active config from host ([`89f9334`](https://github.com/adamkirchberger/nectl/commit/89f93347ef86081ac4c568ca7a8d0990ab387cdf))

* feat: username and password are host core facts

Username and password can be host specific or inherited like other facts. ([`720750e`](https://github.com/adamkirchberger/nectl/commit/720750e64bbc398fda9a88b410afc0600bce3f9e))

* feat: rename default datatree dirname to datatree ([`ccbc90d`](https://github.com/adamkirchberger/nectl/commit/ccbc90da18bedb0023970d59e4c155dea8f27b7f))

* feat: rename config replace to apply ([`dbaae00`](https://github.com/adamkirchberger/nectl/commit/dbaae00ada707a807c8d6302d18912f63083ccd7))

### Fix

* fix: update app description ([`3f10f84`](https://github.com/adamkirchberger/nectl/commit/3f10f84c4abc8375bf9c424a9f331f654d5229e4))

* fix: remove unnecessary compare config parameter ([`ccd013f`](https://github.com/adamkirchberger/nectl/commit/ccd013f48094c848a82da2189882cabfa4e33ee2))

* fix: use IPv4Address type for host mgmt_ip ([`9fd76e2`](https://github.com/adamkirchberger/nectl/commit/9fd76e228b95be2a4532e3bf73d7c560aaa3a4fa))

* fix: add Host object to module public attributes ([`ea39a4c`](https://github.com/adamkirchberger/nectl/commit/ea39a4cded32ef78a3a0d5773f4242f0316b5ec5))

### Refactor

* refactor: fix lint ([`b332361`](https://github.com/adamkirchberger/nectl/commit/b332361417458393416ef06d07767f70ac2c33cf))

* refactor: fix lint ([`089a446`](https://github.com/adamkirchberger/nectl/commit/089a446d3cdccb4d30b883a353bf3e05f164da63))

* refactor: use consistent log messages ([`42692b7`](https://github.com/adamkirchberger/nectl/commit/42692b792f20707e9ad07494e27e8d1a721ff4ee))

* refactor: use consistent log messages ([`202714c`](https://github.com/adamkirchberger/nectl/commit/202714c6a64e20359fa4bd284f1a5cc59f4b0ccb))

* refactor: remove unused import ([`889b617`](https://github.com/adamkirchberger/nectl/commit/889b617dc5cf6fe04286b9864c0d5d22b08b2458))

* refactor: update settings filename in test ([`d1c7f13`](https://github.com/adamkirchberger/nectl/commit/d1c7f1307134b8042d90b1eb9ac00dcf8561c69a))

### Test

* test: update pylintrc ([`bab24a8`](https://github.com/adamkirchberger/nectl/commit/bab24a877023b536958fe7e69918d60cc54ec857))

* test: remove description test ([`dabd0e1`](https://github.com/adamkirchberger/nectl/commit/dabd0e11dcf009e58cf78820c98e8c4bb9e02ca0))


## v0.11.0 (2022-03-15)

### Chore

* chore(release): 0.11.0

# [0.11.0](https://git-us-east1-d.ci-gateway.int.gprd.gitlab.net:8989/adamkirchberger/nectl-dev/compare/0.10.2...0.11.0) (2022-03-15)

### Bug Fixes

* add encoding to generated config files ([5ed9ab5](https://git-us-east1-d.ci-gateway.int.gprd.gitlab.net:8989/adamkirchberger/nectl-dev/commit/5ed9ab5c8d235d6d83d3cd20217e1854709aaa0e))
* test kit settings filename ([f215702](https://git-us-east1-d.ci-gateway.int.gprd.gitlab.net:8989/adamkirchberger/nectl-dev/commit/f2157021ad6546a99217f0db5fc4012c7c328e06))

### Features

* add config compare and replace cli actions ([c0f2aed](https://git-us-east1-d.ci-gateway.int.gprd.gitlab.net:8989/adamkirchberger/nectl-dev/commit/c0f2aed2648588d2d2fdfe9778b13e5054bf4d44))
* add kit custom drivers ([d6d9806](https://git-us-east1-d.ci-gateway.int.gprd.gitlab.net:8989/adamkirchberger/nectl-dev/commit/d6d980689e25a74043b6cf26855177565c0896c2)) ([`a070608`](https://github.com/adamkirchberger/nectl/commit/a070608ef7fbc58ecf9b6c61ec40ff9a8f8a36b2))

### Feature

* feat: add kit custom drivers ([`d6d9806`](https://github.com/adamkirchberger/nectl/commit/d6d980689e25a74043b6cf26855177565c0896c2))

* feat: add config compare and replace cli actions ([`c0f2aed`](https://github.com/adamkirchberger/nectl/commit/c0f2aed2648588d2d2fdfe9778b13e5054bf4d44))

### Fix

* fix: add encoding to generated config files ([`5ed9ab5`](https://github.com/adamkirchberger/nectl/commit/5ed9ab5c8d235d6d83d3cd20217e1854709aaa0e))

* fix: test kit settings filename ([`f215702`](https://github.com/adamkirchberger/nectl/commit/f2157021ad6546a99217f0db5fc4012c7c328e06))


## v0.10.2 (2022-03-06)

### Chore

* chore(release): 0.10.2

## [0.10.2](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.10.1...0.10.2) (2022-03-06)

### Bug Fixes

* python for kit settings instead of yaml ([9e2f1a4](https://gitlab.com/adamkirchberger/nectl-dev/commit/9e2f1a4ffd89351f3d2aafb91666b4227a41223c))
* use default fact action from settings ([09302df](https://gitlab.com/adamkirchberger/nectl-dev/commit/09302dfbe139e75721d4e205366e877ddd63b698)) ([`b60d458`](https://github.com/adamkirchberger/nectl/commit/b60d4583c357be017e4ef7b40293b4b88f1bfbb6))

### Fix

* fix: python for kit settings instead of yaml ([`9e2f1a4`](https://github.com/adamkirchberger/nectl/commit/9e2f1a4ffd89351f3d2aafb91666b4227a41223c))

* fix: use default fact action from settings ([`09302df`](https://github.com/adamkirchberger/nectl/commit/09302dfbe139e75721d4e205366e877ddd63b698))


## v0.10.1 (2022-02-19)

### Chore

* chore(release): 0.10.1

## [0.10.1](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.10.0...0.10.1) (2022-02-19)

### Bug Fixes

* ensure only funcs are used as template sections ([e8fc620](https://gitlab.com/adamkirchberger/nectl-dev/commit/e8fc620730d39fa0953510c9f4770bb1bfd915f7))
* linting issues ([e8ad624](https://gitlab.com/adamkirchberger/nectl-dev/commit/e8ad624c32acd2b984c8fd06b8caadc760e335d8)) ([`d226daf`](https://github.com/adamkirchberger/nectl/commit/d226daf82c00c545d957a138d5af8725c732112d))

### Ci

* ci: add test jobs for different python versions ([`8b1da97`](https://github.com/adamkirchberger/nectl/commit/8b1da978ef2ea42c49f1170e13503db13f1da240))

### Fix

* fix: linting issues ([`e8ad624`](https://github.com/adamkirchberger/nectl/commit/e8ad624c32acd2b984c8fd06b8caadc760e335d8))

* fix: ensure only funcs are used as template sections ([`e8fc620`](https://github.com/adamkirchberger/nectl/commit/e8fc620730d39fa0953510c9f4770bb1bfd915f7))

### Refactor

* refactor: rename config module to settings ([`595969f`](https://github.com/adamkirchberger/nectl/commit/595969fd0ebea63e9f44afc690b8db5e86c14274))

* refactor: rename host id format used in logs ([`0a4b2c6`](https://github.com/adamkirchberger/nectl/commit/0a4b2c6261d4e527517a7ad932a706aa50fb03a2))


## v0.10.0 (2022-02-19)

### Chore

* chore(release): 0.10.0

# [0.10.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.9.0...0.10.0) (2022-02-19)

### Bug Fixes

* facts not being loaded from directories ([0611555](https://gitlab.com/adamkirchberger/nectl-dev/commit/0611555fd28656e635a15762c336f54b7b5cc359))
* incorrect import for importlib ([b4a10e3](https://gitlab.com/adamkirchberger/nectl-dev/commit/b4a10e3de0b0076979484457462944b4136763f8))
* linting issues ([548ac9e](https://gitlab.com/adamkirchberger/nectl-dev/commit/548ac9ed0ce82e5ccca6ed1e330fc27d2fc28798))
* log file path missing slash ([d364d1a](https://gitlab.com/adamkirchberger/nectl-dev/commit/d364d1ac7b74233d44c576aade0a1c8ab6fb840f))
* make mgmt_ip a core fact ([b3f1315](https://gitlab.com/adamkirchberger/nectl-dev/commit/b3f131579597b80653553d2482d22e510dd113c9))
* set default data tree action to replace ([08c9300](https://gitlab.com/adamkirchberger/nectl-dev/commit/08c9300c7cede28fa558d14df1f15dc0d459d20c))
* update logging setup methods and docstring ([5cc0f59](https://gitlab.com/adamkirchberger/nectl-dev/commit/5cc0f594c2b1db1904c7d535705a683f34da8ea9))
* update writer to skip blank configs and return total ([eb31d90](https://gitlab.com/adamkirchberger/nectl-dev/commit/eb31d90bdc1343e35b4edc8d915c113dc2527032))

### Features

* add host drivers ([0100f39](https://gitlab.com/adamkirchberger/nectl-dev/commit/0100f39cae4317a4846e7dd6792686eda95a05e9))
* add junos driver ([d0a81ea](https://gitlab.com/adamkirchberger/nectl-dev/commit/d0a81ea5a1173f7241450a40daac4b011f26a192))
* add junos-eznc dependency ([77a08ed](https://gitlab.com/adamkirchberger/nectl-dev/commit/77a08ed2650b12f039599b0a04cf7a6434b99f22))
* file and console logs include other loggers ([e1b3a52](https://gitlab.com/adamkirchberger/nectl-dev/commit/e1b3a52265b168f8ddcaadaec4fd4ee037f3ce03))
* update public methods ([1c1bcee](https://gitlab.com/adamkirchberger/nectl-dev/commit/1c1bceebba767f92bd35b23691a8cbea7a9bd46c)) ([`4a5e61b`](https://github.com/adamkirchberger/nectl/commit/4a5e61b0026a52aea55eb0ce57cb51e154844033))

* chore: update dependencies ([`867eae0`](https://github.com/adamkirchberger/nectl/commit/867eae074554c7a5aedfdf3d9d8e843fb4a5d8da))

### Feature

* feat: add junos-eznc dependency ([`77a08ed`](https://github.com/adamkirchberger/nectl/commit/77a08ed2650b12f039599b0a04cf7a6434b99f22))

* feat: add junos driver ([`d0a81ea`](https://github.com/adamkirchberger/nectl/commit/d0a81ea5a1173f7241450a40daac4b011f26a192))

* feat: add host drivers ([`0100f39`](https://github.com/adamkirchberger/nectl/commit/0100f39cae4317a4846e7dd6792686eda95a05e9))

* feat: update public methods ([`1c1bcee`](https://github.com/adamkirchberger/nectl/commit/1c1bceebba767f92bd35b23691a8cbea7a9bd46c))

* feat: file and console logs include other loggers ([`e1b3a52`](https://github.com/adamkirchberger/nectl/commit/e1b3a52265b168f8ddcaadaec4fd4ee037f3ce03))

### Fix

* fix: incorrect import for importlib ([`b4a10e3`](https://github.com/adamkirchberger/nectl/commit/b4a10e3de0b0076979484457462944b4136763f8))

* fix: set default data tree action to replace ([`08c9300`](https://github.com/adamkirchberger/nectl/commit/08c9300c7cede28fa558d14df1f15dc0d459d20c))

* fix: linting issues ([`548ac9e`](https://github.com/adamkirchberger/nectl/commit/548ac9ed0ce82e5ccca6ed1e330fc27d2fc28798))

* fix: update logging setup methods and docstring ([`5cc0f59`](https://github.com/adamkirchberger/nectl/commit/5cc0f594c2b1db1904c7d535705a683f34da8ea9))

* fix: update writer to skip blank configs and return total ([`eb31d90`](https://github.com/adamkirchberger/nectl/commit/eb31d90bdc1343e35b4edc8d915c113dc2527032))

* fix: facts not being loaded from directories ([`0611555`](https://github.com/adamkirchberger/nectl/commit/0611555fd28656e635a15762c336f54b7b5cc359))

* fix: make mgmt_ip a core fact ([`b3f1315`](https://github.com/adamkirchberger/nectl/commit/b3f131579597b80653553d2482d22e510dd113c9))

* fix: log file path missing slash ([`d364d1a`](https://github.com/adamkirchberger/nectl/commit/d364d1ac7b74233d44c576aade0a1c8ab6fb840f))

### Refactor

* refactor: fix style ([`df4baf0`](https://github.com/adamkirchberger/nectl/commit/df4baf03f39c739774ec816f774d1af1ee6a27f8))

* refactor: remove unnused import ([`8993f15`](https://github.com/adamkirchberger/nectl/commit/8993f15ccc6afb2468f1a0116682b79e287e931d))

### Test

* test: drivers ([`1a21978`](https://github.com/adamkirchberger/nectl/commit/1a2197867124bcb718ca1ebe2acd0e3384659b79))


## v0.9.0 (2022-01-27)

### Chore

* chore(release): 0.9.0

# [0.9.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.8.0...0.9.0) (2022-01-27)

### Bug Fixes

* host directory facts loading ([f380f23](https://gitlab.com/adamkirchberger/nectl-dev/commit/f380f239ef70ac160ff1a00bb8fd29d1a0ffe72e))

### Features

* support host core facts in datatree lookup paths ([d097019](https://gitlab.com/adamkirchberger/nectl-dev/commit/d0970198eb08f36b9965911182fad6d0928f55de)) ([`f224eb8`](https://github.com/adamkirchberger/nectl/commit/f224eb8a05d6a4a14485414bef5ea343cae4e4e5))

### Feature

* feat: support host core facts in datatree lookup paths ([`d097019`](https://github.com/adamkirchberger/nectl/commit/d0970198eb08f36b9965911182fad6d0928f55de))

### Fix

* fix: host directory facts loading ([`f380f23`](https://github.com/adamkirchberger/nectl/commit/f380f239ef70ac160ff1a00bb8fd29d1a0ffe72e))

### Refactor

* refactor: update docstring ([`61fa277`](https://github.com/adamkirchberger/nectl/commit/61fa2772da30694bd59844655400ad6b80713be0))

* refactor: update docstring ([`39efb0d`](https://github.com/adamkirchberger/nectl/commit/39efb0db0795deb0d9fda84d3e84bcf89d642c31))

### Test

* test: cleanup ([`25e5f31`](https://github.com/adamkirchberger/nectl/commit/25e5f31711100c518a1a16f58a1e5f6cb25b5171))

* test: add test for non directory hosts ([`a9b81eb`](https://github.com/adamkirchberger/nectl/commit/a9b81eb1d0c096a2f894cb758a3c86d3baf10b63))


## v0.8.0 (2022-01-26)

### Chore

* chore(release): 0.8.0

# [0.8.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.7.0...0.8.0) (2022-01-26)

### Features

* add mgmt_ip core host fact. ([b6028cd](https://gitlab.com/adamkirchberger/nectl-dev/commit/b6028cdaac53bcde975d6bf1a4c3b2d2f298cc2e))
* facts can be files or directories of files ([775cfbb](https://gitlab.com/adamkirchberger/nectl-dev/commit/775cfbb697dde439d6efb38bbb9def84074829dd))
* log to console and file in kit ([c057f69](https://gitlab.com/adamkirchberger/nectl-dev/commit/c057f69bd5d58acd8bd6ea1249d98130a2e4a2fa)) ([`a369b8e`](https://github.com/adamkirchberger/nectl/commit/a369b8eb44cac0338bc222f7dd3d7e7ead9dd7d6))

### Feature

* feat: facts can be files or directories of files ([`775cfbb`](https://github.com/adamkirchberger/nectl/commit/775cfbb697dde439d6efb38bbb9def84074829dd))

* feat: log to console and file in kit ([`c057f69`](https://github.com/adamkirchberger/nectl/commit/c057f69bd5d58acd8bd6ea1249d98130a2e4a2fa))

* feat: add mgmt_ip core host fact. ([`b6028cd`](https://github.com/adamkirchberger/nectl/commit/b6028cdaac53bcde975d6bf1a4c3b2d2f298cc2e))

### Refactor

* refactor: use tuples for parametrized tests ([`fba43f6`](https://github.com/adamkirchberger/nectl/commit/fba43f6b3dd917d532ba607fb704ba30595bbb88))


## v0.7.0 (2022-01-15)

### Chore

* chore(release): 0.7.0

# [0.7.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.6.0...0.7.0) (2022-01-15)

### Bug Fixes

* remove templates list cmd ([5e7a6b7](https://gitlab.com/adamkirchberger/nectl-dev/commit/5e7a6b764e256ed00104752be88b6aebf77aea32))
* set default  file path to current directory ([2fce693](https://gitlab.com/adamkirchberger/nectl-dev/commit/2fce693151dbf1ecec62ac06a5d6436857ced97c))
* site discovery issue ([771fea8](https://gitlab.com/adamkirchberger/nectl-dev/commit/771fea88928dc8d0462663cae731136619e8cd7f))
* skip empty render sections ([aaa4cf5](https://gitlab.com/adamkirchberger/nectl-dev/commit/aaa4cf52330f4fda8279962d489e989807e9e04f))
* update error for failed sub template import ([f443628](https://gitlab.com/adamkirchberger/nectl-dev/commit/f443628978ff0031d01c700e7f50f95298b4b058))

### Features

* add single site datatree support ([85b9468](https://gitlab.com/adamkirchberger/nectl-dev/commit/85b946846a097e64ff5dee5a2e057a9f84fc3914))
* write configs to staged directory ([2a35d1f](https://gitlab.com/adamkirchberger/nectl-dev/commit/2a35d1f3ac32cfef5879278156a3fc46b687b27d)) ([`adc4af7`](https://github.com/adamkirchberger/nectl/commit/adc4af799340f9e63e3f3fae99ac5622cb27aedd))

* chore(release): 0.6.0

# [0.6.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.5.0...0.6.0) (2022-01-11)

### Bug Fixes

* host types ([3535e92](https://gitlab.com/adamkirchberger/nectl-dev/commit/3535e927add7060e8ae06a929066958ce4e22f02))
* increase log severity for hosts missing os vars ([472920b](https://gitlab.com/adamkirchberger/nectl-dev/commit/472920b81d4c4c5104f42231bfb553660db600fc))
* issue related to frozen and merge data actions ([6eceace](https://gitlab.com/adamkirchberger/nectl-dev/commit/6eceacebb008d1efb7888873af846cc633415db5))
* rename config var for readability ([c0eb13e](https://gitlab.com/adamkirchberger/nectl-dev/commit/c0eb13e24c03c43d4b617e5a09bcf06767bd8e2b))
* separate render context functions ([1032403](https://gitlab.com/adamkirchberger/nectl-dev/commit/10324033c0ecdf3a538ecbc2b475211492c8402f))
* unset config env var during tests ([a48133f](https://gitlab.com/adamkirchberger/nectl-dev/commit/a48133ff61b93b3d4c8858dc2f0748d8e3d2b1c0))

### Features

* add dict deep merging ([bace069](https://gitlab.com/adamkirchberger/nectl-dev/commit/bace069b08a49a73497dfcf01cb1646916d31186)) ([`f152cde`](https://github.com/adamkirchberger/nectl/commit/f152cde708272aa55a79ef47de1b3b8d8cc1464b))

* chore(release): 0.5.0

# [0.5.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.4.0...0.5.0) (2022-01-03)

### Bug Fixes

* log and raise any template import errors ([ced65f4](https://gitlab.com/adamkirchberger/nectl-dev/commit/ced65f494a67e5e093c7e3753e86431027211690))
* make get_config return same config every time ([0b65de2](https://gitlab.com/adamkirchberger/nectl-dev/commit/0b65de24a6e15c5637764f3ec452da0d2af07c2d))
* move render context out of try block ([71776e1](https://gitlab.com/adamkirchberger/nectl-dev/commit/71776e1680f89b28d45ff7d4b939c679d69ca39b))
* raise error for issues during discovery ([f310cf8](https://gitlab.com/adamkirchberger/nectl-dev/commit/f310cf8cde59674e9d1bb3383a88bc5cc147c290))
* raise render error only after all errors found ([7fdaf43](https://gitlab.com/adamkirchberger/nectl-dev/commit/7fdaf433d5b83c323292bc2038a8b89e51873063))
* remove unused imports and comments ([a2f0434](https://gitlab.com/adamkirchberger/nectl-dev/commit/a2f043459cf4ee9b6eaa51b30c4eddfaec73dd4b))
* replace additional calls for single dict iter ([d396d9f](https://gitlab.com/adamkirchberger/nectl-dev/commit/d396d9fe126fa06cfdda5eccba3d55ffdde5b3a4))
* resolve type issues ([508465e](https://gitlab.com/adamkirchberger/nectl-dev/commit/508465e7895a5ff19d66cd51709e199275bbd836))
* return None if host attr not found in facts ([9863fe3](https://gitlab.com/adamkirchberger/nectl-dev/commit/9863fe30cfd4b16ed56fa2ad303fe9430b7c96a3))
* rewrite block to catch multiple exceptions ([1e8bccc](https://gitlab.com/adamkirchberger/nectl-dev/commit/1e8bccc7339dab07e667bff9743d317d8e3b808f))
* set host customer value to optional ([fb14a55](https://gitlab.com/adamkirchberger/nectl-dev/commit/fb14a55778e406b7503bef4b1d246490f019c2fe))
* set logger level ([0fbeffa](https://gitlab.com/adamkirchberger/nectl-dev/commit/0fbeffaeee3981f016f1dfdd7b456143b353ffb5))
* templates render based on order of definition ([05b62dc](https://gitlab.com/adamkirchberger/nectl-dev/commit/05b62dc4939a61f28c8309a318cafd8e394fb021))

### Features

* add render context ([4881af1](https://gitlab.com/adamkirchberger/nectl-dev/commit/4881af1eb187bb7d84c49a1a8c1656c51aa35040))
* templates are determined based on os_name ([296267b](https://gitlab.com/adamkirchberger/nectl-dev/commit/296267b5ae31435bcf3c6581160a7879da6fbf83))
* templates use functions with print methods ([a5a8a54](https://gitlab.com/adamkirchberger/nectl-dev/commit/a5a8a54e77666191110cfeb3e9ba681cb0b33853))
* update dependencies ([e69edd5](https://gitlab.com/adamkirchberger/nectl-dev/commit/e69edd505c6ea22cb416fe22f0dd6a82da765918)) ([`6a0d2a4`](https://github.com/adamkirchberger/nectl/commit/6a0d2a44b883b64d1076c7ee0bbdd85ff8ba7331))

* chore: add pytest-click dev dependency ([`8649b5f`](https://github.com/adamkirchberger/nectl/commit/8649b5f9c3b5f374ce73772a369b9f281a01deea))

* chore: add tests ([`d1ab6c5`](https://github.com/adamkirchberger/nectl/commit/d1ab6c51542fe355594ca5c8e428cc5ed789a5e4))

* chore(release): 0.4.0

# [0.4.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.3.0...0.4.0) (2021-12-19)

### Bug Fixes

* add git ignore for coverage files ([ee4d3fa](https://gitlab.com/adamkirchberger/nectl-dev/commit/ee4d3fa8d2c5715a46508e122f058a7e93289926))
* compile regex from string to avoid errors ([ab2e99c](https://gitlab.com/adamkirchberger/nectl-dev/commit/ab2e99c08dd275eeb2d16958d5a89ca2da8e4053))
* ignore protected variables ([99323f3](https://gitlab.com/adamkirchberger/nectl-dev/commit/99323f356701bf1b6cd0f94f2be3723b370e6b68))

### Features

* add support for single tenant data tree ([19e0e4a](https://gitlab.com/adamkirchberger/nectl-dev/commit/19e0e4a05868e4d430cbf2b863c94f0798f3baf2)) ([`75ebdb4`](https://github.com/adamkirchberger/nectl/commit/75ebdb4511b46f47b09775edb8295f863898569b))

* chore(release): 0.3.0

# [0.3.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.2.0...0.3.0) (2021-09-26)

### Bug Fixes

* catch errors from invalid fact files ([94fa23d](https://gitlab.com/adamkirchberger/nectl-dev/commit/94fa23d13543644797f21f6476fa9a3816a7d7d2))
* default config get logic ([f7b8489](https://gitlab.com/adamkirchberger/nectl-dev/commit/f7b8489e65acf41cc077643dd19dc8558764992b))
* rename generate to render ([9afe8cd](https://gitlab.com/adamkirchberger/nectl-dev/commit/9afe8cdf61901453fc16beb0e2cd4b01a7a80125))
* rename host os to os_name for readability ([3b7ac9f](https://gitlab.com/adamkirchberger/nectl-dev/commit/3b7ac9f941de51947ae5c0f91395099b7600192a))
* rename os to os_name missed in prev commit ([6bb9a20](https://gitlab.com/adamkirchberger/nectl-dev/commit/6bb9a208bd5ed2fc30c8cac8bfc8a37f37248e82))
* rename os_regex to os_name_regex ([b5c2aac](https://gitlab.com/adamkirchberger/nectl-dev/commit/b5c2aac1745d9652916caf2e6e193545cdc8b0db))
* update arg order ([24758df](https://gitlab.com/adamkirchberger/nectl-dev/commit/24758df98ad633527b7c81db9c8bdb7f2bdace6d))
* update default logging level to error ([bb369fc](https://gitlab.com/adamkirchberger/nectl-dev/commit/bb369fc266a0cf188b3296872740bc9497bf487c))
* update template handling ([addff3d](https://gitlab.com/adamkirchberger/nectl-dev/commit/addff3d867cbaacc76a045d0cbc30ba18b1549c2))

### Features

* merge cli groups for templates and configs ([7dc9071](https://gitlab.com/adamkirchberger/nectl-dev/commit/7dc9071ea2c7cd78dacf6da725fd23c94c46fa2c))
* rename blueprints to templates ([b59b170](https://gitlab.com/adamkirchberger/nectl-dev/commit/b59b170ecd0cebde5dccd8d0c9e11d56e8cd4942)) ([`721a52d`](https://github.com/adamkirchberger/nectl/commit/721a52d6dbe0210e160491ac86bbb579796fcf61))

* chore(release): 0.2.0

# [0.2.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.1.0...0.2.0) (2021-09-09)

### Bug Fixes

* logging config issue ([ac44793](https://gitlab.com/adamkirchberger/nectl-dev/commit/ac44793705696f20a1130c28af6c78e3b02d48ec))
* set default to none for optional fields ([d864229](https://gitlab.com/adamkirchberger/nectl-dev/commit/d864229b26705b3f40d35fcda81e0247ff3ca1b0))
* use consistent logging format ([3ab3f01](https://gitlab.com/adamkirchberger/nectl-dev/commit/3ab3f011118c57b16fe31319d7a20ca9f53184e1))

### Features

* add template rendering using blueprints ([ba8f8c5](https://gitlab.com/adamkirchberger/nectl-dev/commit/ba8f8c53bc83df787ac8364ed26a75327b234bfc)) ([`c1eb193`](https://github.com/adamkirchberger/nectl/commit/c1eb1933324e778de64c0afa96e8d60f37ddc536))

* chore: add pipeline ([`98a22f1`](https://github.com/adamkirchberger/nectl/commit/98a22f195f301b40395099999ccf4fb92231ff5f))

### Ci

* ci: update node version ([`ff183d6`](https://github.com/adamkirchberger/nectl/commit/ff183d667594a1a0f7b3fbd3baff0f5120d5b15f))

* ci: add release config file ([`f162a7c`](https://github.com/adamkirchberger/nectl/commit/f162a7c16f53bb2dd6a1ed8506a2baeac3c3bed4))

### Documentation

* docs: add missing full stops ([`88441d2`](https://github.com/adamkirchberger/nectl/commit/88441d2ab74fd33b13e7c9490d429b23cbc0af51))

* docs: update types ([`f9ff9f5`](https://github.com/adamkirchberger/nectl/commit/f9ff9f5f7b5da13930e80ac82d049fa44dbe85c1))

* docs: rename docstring ([`2af69f2`](https://github.com/adamkirchberger/nectl/commit/2af69f27b263a05a9cea5b6316eecc3db7ddd9a5))

### Feature

* feat: add single site datatree support ([`85b9468`](https://github.com/adamkirchberger/nectl/commit/85b946846a097e64ff5dee5a2e057a9f84fc3914))

* feat: write configs to staged directory ([`2a35d1f`](https://github.com/adamkirchberger/nectl/commit/2a35d1f3ac32cfef5879278156a3fc46b687b27d))

* feat: add dict deep merging ([`8a16336`](https://github.com/adamkirchberger/nectl/commit/8a16336a0cd047549360b8a3effac4a992710db1))

* feat: update dependencies ([`ff72873`](https://github.com/adamkirchberger/nectl/commit/ff72873389bd2ff5d0368cbd8a9c5d331d748065))

* feat: templates are determined based on os_name ([`1611e6d`](https://github.com/adamkirchberger/nectl/commit/1611e6d6b4409f59b99868d656f8ea728948d59d))

* feat: add render context ([`6849f0f`](https://github.com/adamkirchberger/nectl/commit/6849f0f898e402c8030377d342123222d9cfec21))

* feat: templates use functions with print methods ([`c591c6f`](https://github.com/adamkirchberger/nectl/commit/c591c6fc552b9b1ea90d3d87190d1739122e0549))

* feat: add support for single tenant data tree ([`aeb5081`](https://github.com/adamkirchberger/nectl/commit/aeb5081966d4b3933fea3291c6aa68b6f75d1976))

* feat: merge cli groups for templates and configs ([`914c3f4`](https://github.com/adamkirchberger/nectl/commit/914c3f4b18cef25f03cafe9e4cb662b219617cf6))

* feat: rename blueprints to templates ([`faec0bf`](https://github.com/adamkirchberger/nectl/commit/faec0bf82440f5cce7229864970147b732711e18))

* feat: add template rendering using blueprints ([`25a003f`](https://github.com/adamkirchberger/nectl/commit/25a003f0c0cd32c7770a83ec681fcd13162e91cb))

### Fix

* fix: site discovery issue ([`771fea8`](https://github.com/adamkirchberger/nectl/commit/771fea88928dc8d0462663cae731136619e8cd7f))

* fix: update error for failed sub template import ([`f443628`](https://github.com/adamkirchberger/nectl/commit/f443628978ff0031d01c700e7f50f95298b4b058))

* fix: skip empty render sections ([`aaa4cf5`](https://github.com/adamkirchberger/nectl/commit/aaa4cf52330f4fda8279962d489e989807e9e04f))

* fix: remove templates list cmd ([`5e7a6b7`](https://github.com/adamkirchberger/nectl/commit/5e7a6b764e256ed00104752be88b6aebf77aea32))

* fix: set default  file path to current directory ([`2fce693`](https://github.com/adamkirchberger/nectl/commit/2fce693151dbf1ecec62ac06a5d6436857ced97c))

* fix: increase log severity for hosts missing os vars ([`1e31b28`](https://github.com/adamkirchberger/nectl/commit/1e31b283f2c6bc54a32d68ea7209384445e6dd5f))

* fix: host types ([`7a05b4c`](https://github.com/adamkirchberger/nectl/commit/7a05b4cca76e395549fc45ae58b4bcc513a212e9))

* fix: issue related to frozen and merge data actions ([`82a61bf`](https://github.com/adamkirchberger/nectl/commit/82a61bf824a27f20b7eedba062b39ea0d7a1e3aa))

* fix: separate render context functions ([`3799b1a`](https://github.com/adamkirchberger/nectl/commit/3799b1a93ebb99a04bf15bd5b4cbe073e2652020))

* fix: rename config var for readability ([`932617d`](https://github.com/adamkirchberger/nectl/commit/932617d7fe3a3a7087866213f799f6833375e0d9))

* fix: unset config env var during tests ([`bfe58e8`](https://github.com/adamkirchberger/nectl/commit/bfe58e8c1b831a623107ba2b9d4044eb706caa58))

* fix: return None if host attr not found in facts ([`6e70105`](https://github.com/adamkirchberger/nectl/commit/6e70105e3149a2671a7c8cb6bd11e9cd2ea6432a))

* fix: raise error for issues during discovery ([`f5cdf7f`](https://github.com/adamkirchberger/nectl/commit/f5cdf7f24626c14f6f7985b626bc2e7394aafb5f))

* fix: set host customer value to optional ([`61a372f`](https://github.com/adamkirchberger/nectl/commit/61a372f2aa0e98a568ff114c5ad5a0daf473f2fc))

* fix: log and raise any template import errors ([`57977a7`](https://github.com/adamkirchberger/nectl/commit/57977a775977df2ee49712b0ee1bd2cc05717426))

* fix: raise render error only after all errors found ([`4270855`](https://github.com/adamkirchberger/nectl/commit/42708559fcf5f9762d84386472d41f3f0413fc83))

* fix: move render context out of try block ([`05542a9`](https://github.com/adamkirchberger/nectl/commit/05542a99947e1e01ce8afdd686955e9e0f8bf940))

* fix: set logger level ([`719c806`](https://github.com/adamkirchberger/nectl/commit/719c806a29e0e38363c6eaa3a2266532cb059585))

* fix: rewrite block to catch multiple exceptions ([`541f7c2`](https://github.com/adamkirchberger/nectl/commit/541f7c2fd948c7f4994f8de6039ff7bda76ff9dc))

* fix: remove unused imports and comments ([`96b72b4`](https://github.com/adamkirchberger/nectl/commit/96b72b485c44c875486f1b77c0a6278c72f069ef))

* fix: make get_config return same config every time ([`ee2f46b`](https://github.com/adamkirchberger/nectl/commit/ee2f46b755bc20954185ec0fd212843cc80effe1))

* fix: replace additional calls for single dict iter ([`3c4cd42`](https://github.com/adamkirchberger/nectl/commit/3c4cd42994e12cd1b0a97ee3b92589d55ceb8b31))

* fix: resolve type issues ([`80fa19d`](https://github.com/adamkirchberger/nectl/commit/80fa19dfd364f399db38d7dab12d0fa0f6ae61b7))

* fix: templates render based on order of definition ([`834c5e6`](https://github.com/adamkirchberger/nectl/commit/834c5e6e95d25a8dd940c43f5916037fc3a7bf02))

* fix: add git ignore for coverage files ([`e5c196c`](https://github.com/adamkirchberger/nectl/commit/e5c196cf3dea1253620e8d8bf50713693d296bdb))

* fix: compile regex from string to avoid errors ([`d935415`](https://github.com/adamkirchberger/nectl/commit/d9354152d77809a202d2ecdbb186a61f2585ae89))

* fix: ignore protected variables ([`da61696`](https://github.com/adamkirchberger/nectl/commit/da61696193f04ab7ae6effb736a766c60d9f548c))

* fix: rename generate to render ([`f6a46b6`](https://github.com/adamkirchberger/nectl/commit/f6a46b6868e305fdddf72b817c14808db8bab7e1))

* fix: default config get logic ([`dd1aa9e`](https://github.com/adamkirchberger/nectl/commit/dd1aa9e9318daf654fb3f5a9e89485a18e93e9bd))

* fix: rename os_regex to os_name_regex ([`e15be34`](https://github.com/adamkirchberger/nectl/commit/e15be34b0d59795e6025f99f54199289f4e9b3f6))

* fix: update template handling ([`d230415`](https://github.com/adamkirchberger/nectl/commit/d230415df25eb40040afb133ca7e1b92e3fe9c50))

* fix: update arg order ([`a8bc33e`](https://github.com/adamkirchberger/nectl/commit/a8bc33e82af86163d71f4c23febec4de6fc7d91c))

* fix: catch errors from invalid fact files ([`a8e8109`](https://github.com/adamkirchberger/nectl/commit/a8e8109d9c156989cdcc93c9bb5919e6522cbee8))

* fix: update default logging level to error ([`2e30b12`](https://github.com/adamkirchberger/nectl/commit/2e30b128518507089b13d67611ee63b0b965f6dd))

* fix: rename os to os_name missed in prev commit ([`34e35e0`](https://github.com/adamkirchberger/nectl/commit/34e35e00b2800bf9eb2ee6d547238989ef4d0a5c))

* fix: rename host os to os_name for readability ([`d8449b9`](https://github.com/adamkirchberger/nectl/commit/d8449b9cc5a05b10a849c9c15b701a70b268f358))

* fix: set default to none for optional fields ([`4860e67`](https://github.com/adamkirchberger/nectl/commit/4860e67aa5006c7b241e966ba6ca8b6d5708f056))

* fix: use consistent logging format ([`c722087`](https://github.com/adamkirchberger/nectl/commit/c722087d4288a8d063670dea8d2ca8fa7bee20b6))

* fix: logging config issue ([`fb0cf35`](https://github.com/adamkirchberger/nectl/commit/fb0cf35c73170f556bae043d92821a675946f700))

### Refactor

* refactor: rename render var for readability ([`2e07307`](https://github.com/adamkirchberger/nectl/commit/2e07307d5211d2ff356700e46b09da92c39c1797))

* refactor: set config as required arg and use context ([`4e0db5e`](https://github.com/adamkirchberger/nectl/commit/4e0db5e6ae57f4c28ced4c243cf1e064e129941a))

* refactor: rename render facts method ([`05fb6c0`](https://github.com/adamkirchberger/nectl/commit/05fb6c041145febee30b685e12e775081f994854))

* refactor: update getter ([`d417ad8`](https://github.com/adamkirchberger/nectl/commit/d417ad8198c8c8f2a59ca00b635fd0e059ccdb9e))

* refactor: update logging ([`5debb56`](https://github.com/adamkirchberger/nectl/commit/5debb56b00c7a49e12b40c6c3550752574fe39a3))

* refactor: use shared global config variable ([`231fab5`](https://github.com/adamkirchberger/nectl/commit/231fab5aeadd48c5b6d5baa87423d87fd632bdf3))

* refactor: set facts as property of a host object ([`2784211`](https://github.com/adamkirchberger/nectl/commit/27842115b1a90d0db0c0f421af6c97b1e3839003))

### Style

* style: remove full stop from error messages. ([`6271797`](https://github.com/adamkirchberger/nectl/commit/62717971d62151e777369fba92d5970acae264f8))

### Test

* test: fix tests and comments ([`0988eb7`](https://github.com/adamkirchberger/nectl/commit/0988eb7688752ad90934c1fa5f93636b1c3ebb12))

* test: add more tests and restructure existing ([`1be41d2`](https://github.com/adamkirchberger/nectl/commit/1be41d2d99f7334071bf41c1bc3a8edb6045de84))

* test: add blueprints_map to config ([`5d89afd`](https://github.com/adamkirchberger/nectl/commit/5d89afd5b59c76f2f94e683c8e9a9ebb3b540de2))

* test: add coverage plugin and stubs ([`4abe2e2`](https://github.com/adamkirchberger/nectl/commit/4abe2e20ebd98f68af2f34f01a410e872bfc49ea))

### Unknown

* Initial commit ([`6c83f20`](https://github.com/adamkirchberger/nectl/commit/6c83f2098c22ca8be4b05d94def29f2c61332d64))

# Changelog

# [0.7.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.6.0...0.7.0) (2022-01-15)


### Bug Fixes

* remove templates list cmd ([5e7a6b7](https://gitlab.com/adamkirchberger/nectl-dev/commit/5e7a6b764e256ed00104752be88b6aebf77aea32))
* set default  file path to current directory ([2fce693](https://gitlab.com/adamkirchberger/nectl-dev/commit/2fce693151dbf1ecec62ac06a5d6436857ced97c))
* site discovery issue ([771fea8](https://gitlab.com/adamkirchberger/nectl-dev/commit/771fea88928dc8d0462663cae731136619e8cd7f))
* skip empty render sections ([aaa4cf5](https://gitlab.com/adamkirchberger/nectl-dev/commit/aaa4cf52330f4fda8279962d489e989807e9e04f))
* update error for failed sub template import ([f443628](https://gitlab.com/adamkirchberger/nectl-dev/commit/f443628978ff0031d01c700e7f50f95298b4b058))


### Features

* add single site datatree support ([85b9468](https://gitlab.com/adamkirchberger/nectl-dev/commit/85b946846a097e64ff5dee5a2e057a9f84fc3914))
* write configs to staged directory ([2a35d1f](https://gitlab.com/adamkirchberger/nectl-dev/commit/2a35d1f3ac32cfef5879278156a3fc46b687b27d))

# [0.6.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.5.0...0.6.0) (2022-01-11)


### Bug Fixes

* host types ([3535e92](https://gitlab.com/adamkirchberger/nectl-dev/commit/3535e927add7060e8ae06a929066958ce4e22f02))
* increase log severity for hosts missing os vars ([472920b](https://gitlab.com/adamkirchberger/nectl-dev/commit/472920b81d4c4c5104f42231bfb553660db600fc))
* issue related to frozen and merge data actions ([6eceace](https://gitlab.com/adamkirchberger/nectl-dev/commit/6eceacebb008d1efb7888873af846cc633415db5))
* rename config var for readability ([c0eb13e](https://gitlab.com/adamkirchberger/nectl-dev/commit/c0eb13e24c03c43d4b617e5a09bcf06767bd8e2b))
* separate render context functions ([1032403](https://gitlab.com/adamkirchberger/nectl-dev/commit/10324033c0ecdf3a538ecbc2b475211492c8402f))
* unset config env var during tests ([a48133f](https://gitlab.com/adamkirchberger/nectl-dev/commit/a48133ff61b93b3d4c8858dc2f0748d8e3d2b1c0))


### Features

* add dict deep merging ([bace069](https://gitlab.com/adamkirchberger/nectl-dev/commit/bace069b08a49a73497dfcf01cb1646916d31186))

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
* update dependencies ([e69edd5](https://gitlab.com/adamkirchberger/nectl-dev/commit/e69edd505c6ea22cb416fe22f0dd6a82da765918))

# [0.4.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.3.0...0.4.0) (2021-12-19)


### Bug Fixes

* add git ignore for coverage files ([ee4d3fa](https://gitlab.com/adamkirchberger/nectl-dev/commit/ee4d3fa8d2c5715a46508e122f058a7e93289926))
* compile regex from string to avoid errors ([ab2e99c](https://gitlab.com/adamkirchberger/nectl-dev/commit/ab2e99c08dd275eeb2d16958d5a89ca2da8e4053))
* ignore protected variables ([99323f3](https://gitlab.com/adamkirchberger/nectl-dev/commit/99323f356701bf1b6cd0f94f2be3723b370e6b68))


### Features

* add support for single tenant data tree ([19e0e4a](https://gitlab.com/adamkirchberger/nectl-dev/commit/19e0e4a05868e4d430cbf2b863c94f0798f3baf2))

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
* rename blueprints to templates ([b59b170](https://gitlab.com/adamkirchberger/nectl-dev/commit/b59b170ecd0cebde5dccd8d0c9e11d56e8cd4942))

# [0.2.0](https://gitlab.com/adamkirchberger/nectl-dev/compare/0.1.0...0.2.0) (2021-09-09)


### Bug Fixes

* logging config issue ([ac44793](https://gitlab.com/adamkirchberger/nectl-dev/commit/ac44793705696f20a1130c28af6c78e3b02d48ec))
* set default to none for optional fields ([d864229](https://gitlab.com/adamkirchberger/nectl-dev/commit/d864229b26705b3f40d35fcda81e0247ff3ca1b0))
* use consistent logging format ([3ab3f01](https://gitlab.com/adamkirchberger/nectl-dev/commit/3ab3f011118c57b16fe31319d7a20ca9f53184e1))


### Features

* add template rendering using blueprints ([ba8f8c5](https://gitlab.com/adamkirchberger/nectl-dev/commit/ba8f8c53bc83df787ac8364ed26a75327b234bfc))

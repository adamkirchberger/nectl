# Changelog

<!--next-version-placeholder-->

## v0.15.5 (2022-05-01)
### Fix
* Update dependencies ([#4](https://github.com/adamkirchberger/nectl/issues/4)) ([`320583d`](https://github.com/adamkirchberger/nectl/commit/320583d0a1cb39afa8c5911bd6a86411785b29d9))

### Documentation
* Fix bad character ([`36f2370`](https://github.com/adamkirchberger/nectl/commit/36f237039d7020b72ada6233dc3cdd630ed41655))
* Fix changelog ([#3](https://github.com/adamkirchberger/nectl/issues/3)) ([`5cab1be`](https://github.com/adamkirchberger/nectl/commit/5cab1bec4c23af4420b195e23a22cd805341087d))

## 0.15.4 (2022-04-24)
### Fix
* readme image ([`680d264`](https://github.com/adamkirchberger/nectl/commit/680d264518dc44be57e04ea6e39795883f587e19))

## 0.15.3 (2022-04-24)
### Fix
* update broken links and img ([`b8df020`](https://github.com/adamkirchberger/nectl/commit/b8df020b32b42617af16cd1bbd55d11c163c53d9))

## 0.15.2 (2022-04-24)
### Fix
* package documentation link ([`a4bf460`](https://github.com/adamkirchberger/nectl/commit/a4bf460eab17ff34584abe0a20c7fa741e4db0d0))

## 0.15.1 (2022-04-24)
### Fix
* update readme and docs favicon ([`6dbc6ed`](https://github.com/adamkirchberger/nectl/commit/6dbc6ed22a384e5f191686d1a4955859e82f27ae))

## 0.15.0 (2022-04-24)
### Feature
* add example demo-kit1 ([`b55e6b`](https://github.com/adamkirchberger/nectl/commit/b55e6b0304798e99fd2772a6cce6e90b0c3e5437))
### Fix
* host discovery regex ([`7ff0f1a`](https://github.com/adamkirchberger/nectl/commit/7ff0f1ac0e31daacaf6420f42513639405ad731e))
* log attempts to modify frozen facts ([`9f26e13`](https://github.com/adamkirchberger/nectl/commit/9f26e13ec95edb59e671b30696ce5a17b4efa6a0))
* show matched hosts when applying ([`c9bf83b`](https://github.com/adamkirchberger/nectl/commit/c9bf83b44dc5ed7d90aeb1a67f82797d7b08ea46))
* rename test to checks ([`afacfd6`](https://github.com/adamkirchberger/nectl/commit/afacfd62f58b859aa1a4f3354dac3a6e57e9576d))

## 0.14.0 (2022-04-17)
### Feature
* add deployment groups ([`417abd4`](https://github.com/adamkirchberger/nectl/commit/417abd41b7e3d666ad511974da22adb8c6bd8dfc))

## 0.13.1 (2022-04-09)
### Fix
* datatree list-hosts json output ([`b578a6e`](https://github.com/adamkirchberger/nectl/commit/b578a6e9da6b11bb7f1794317193b7c13146fac6))

## 0.13.0 (2022-04-09)
### Fix
* add optional user and pass args for config diff ([`478b1e4`](https://github.com/adamkirchberger/nectl/commit/478b1e49f085bca4d6c59514287201b923105209))
* fetch user and pass from datatree if no args supplied ([`20fdd27`](https://github.com/adamkirchberger/nectl/commit/20fdd27d36031cede5e1bf4c776ebb6d642e3028))
* skip driver calls when os_name or mgmt_ip missing ([`f7bef73`](https://github.com/adamkirchberger/nectl/commit/f7bef736e18625a24f07dae611484a3c0517206d))

### Feature
* add assume yes flag to config apply cli action ([`462f5a8`](https://github.com/adamkirchberger/nectl/commit/462f5a8aa07a1f13f0de58b1cc82c723c599eff3))
* add cli facts check only action ([`ae4316b`](https://github.com/adamkirchberger/nectl/commit/ae4316b8d34f1dcdf86847127212de82d3284111))
* rename data to datatree ([`055ae4f`](https://github.com/adamkirchberger/nectl/commit/055ae4f759f79ffa9a0ee4e2099534ed22fa3b3e))

## 0.12.0 (2022-03-28)
### Fix
* add Host object to module public attributes ([`ea39a4c`](https://github.com/adamkirchberger/nectl/commit/ea39a4cded32ef78a3a0d5773f4242f0316b5ec5))
* remove unnecessary compare config parameter ([`ccd013f`](https://github.com/adamkirchberger/nectl/commit/ccd013f48094c848a82da2189882cabfa4e33ee2))
* update app description ([`3f10f84`](https://github.com/adamkirchberger/nectl/commit/3f10f84c4abc8375bf9c424a9f331f654d5229e4))
* use IPv4Address type for host mgmt_ip ([`9fd76e2`](https://github.com/adamkirchberger/nectl/commit/9fd76e228b95be2a4532e3bf73d7c560aaa3a4fa))

### Feature
* add action to get active config from host ([`89f9334`](https://github.com/adamkirchberger/nectl/commit/89f93347ef86081ac4c568ca7a8d0990ab387cdf))
* rename config replace to apply ([`dbaae00`](https://github.com/adamkirchberger/nectl/commit/dbaae00ada707a807c8d6302d18912f63083ccd7))
* rename default datatree dirname to datatree ([`ccbc90d`](https://github.com/adamkirchberger/nectl/commit/ccbc90da18bedb0023970d59e4c155dea8f27b7f))
* username and password are host core facts ([`720750e`](https://github.com/adamkirchberger/nectl/commit/720750e64bbc398fda9a88b410afc0600bce3f9e))

## 0.11.0 (2022-03-15)
### Fix
* add encoding to generated config files ([`5ed9ab5`](https://github.com/adamkirchberger/nectl/commit/5ed9ab5c8d235d6d83d3cd20217e1854709aaa0e))
* test kit settings filename ([`f215702`](https://github.com/adamkirchberger/nectl/commit/f2157021ad6546a99217f0db5fc4012c7c328e06))

### Feature
* add config compare and replace cli actions ([`c0f2aed`](https://github.com/adamkirchberger/nectl/commit/c0f2aed2648588d2d2fdfe9778b13e5054bf4d44))
* add kit custom drivers ([`d6d9806`](https://github.com/adamkirchberger/nectl/commit/d6d980689e25a74043b6cf26855177565c0896c2))

## 0.10.2 (2022-03-06)
### Fix
* python for kit settings instead of yaml ([`9e2f1a4`](https://github.com/adamkirchberger/nectl/commit/9e2f1a4ffd89351f3d2aafb91666b4227a41223c))
* use default fact action from settings ([`09302df`](https://github.com/adamkirchberger/nectl/commit/09302dfbe139e75721d4e205366e877ddd63b698))

## 0.10.1 (2022-02-19)
### Fix
* ensure only funcs are used as template sections ([`e8fc620`](https://github.com/adamkirchberger/nectl/commit/e8fc620730d39fa0953510c9f4770bb1bfd915f7))
* linting issues ([`e8ad624`](https://github.com/adamkirchberger/nectl/commit/e8ad624c32acd2b984c8fd06b8caadc760e335d8))

## 0.10.0 (2022-02-19)
### Fix
* facts not being loaded from directories ([`0611555`](https://github.com/adamkirchberger/nectl/commit/0611555fd28656e635a15762c336f54b7b5cc359))
* incorrect import for importlib ([`b4a10e3`](https://github.com/adamkirchberger/nectl/commit/b4a10e3de0b0076979484457462944b4136763f8))
* linting issues ([`548ac9e`](https://github.com/adamkirchberger/nectl/commit/548ac9ed0ce82e5ccca6ed1e330fc27d2fc28798))
* log file path missing slash ([`d364d1a`](https://github.com/adamkirchberger/nectl/commit/d364d1ac7b74233d44c576aade0a1c8ab6fb840f))
* make mgmt_ip a core fact ([`b3f1315`](https://github.com/adamkirchberger/nectl/commit/b3f131579597b80653553d2482d22e510dd113c9))
* set default data tree action to replace ([`08c9300`](https://github.com/adamkirchberger/nectl/commit/08c9300c7cede28fa558d14df1f15dc0d459d20c))
* update logging setup methods and docstring ([`5cc0f59`](https://github.com/adamkirchberger/nectl/commit/5cc0f594c2b1db1904c7d535705a683f34da8ea9))
* update writer to skip blank configs and return total ([`eb31d90`](https://github.com/adamkirchberger/nectl/commit/eb31d90bdc1343e35b4edc8d915c113dc2527032))

### Feature
* add host drivers ([`0100f39`](https://github.com/adamkirchberger/nectl/commit/0100f39cae4317a4846e7dd6792686eda95a05e9))
* add junos driver ([`d0a81ea`](https://github.com/adamkirchberger/nectl/commit/d0a81ea5a1173f7241450a40daac4b011f26a192))
* add junos-eznc dependency ([`77a08ed`](https://github.com/adamkirchberger/nectl/commit/77a08ed2650b12f039599b0a04cf7a6434b99f22))
* file and console logs include other loggers ([`e1b3a52`](https://github.com/adamkirchberger/nectl/commit/e1b3a52265b168f8ddcaadaec4fd4ee037f3ce03))
* update public methods ([`1c1bcee`](https://github.com/adamkirchberger/nectl/commit/1c1bceebba767f92bd35b23691a8cbea7a9bd46c))

## 0.9.0 (2022-01-27)
### Fix
* host directory facts loading ([`f380f23`](https://github.com/adamkirchberger/nectl/commit/f380f239ef70ac160ff1a00bb8fd29d1a0ffe72e))

### Feature
* support host core facts in datatree lookup paths ([`d097019`](https://github.com/adamkirchberger/nectl/commit/d0970198eb08f36b9965911182fad6d0928f55de))

## 0.8.0 (2022-01-26)
### Feature
* add mgmt_ip core host fact. ([`b6028cd`](https://github.com/adamkirchberger/nectl/commit/b6028cdaac53bcde975d6bf1a4c3b2d2f298cc2e))
* facts can be files or directories of files ([`775cfbb`](https://github.com/adamkirchberger/nectl/commit/775cfbb697dde439d6efb38bbb9def84074829dd))
* log to console and file in kit ([`c057f69`](https://github.com/adamkirchberger/nectl/commit/c057f69bd5d58acd8bd6ea1249d98130a2e4a2fa))

## 0.7.0 (2022-01-15)
### Fix
* remove templates list cmd ([`5e7a6b7`](https://github.com/adamkirchberger/nectl/commit/5e7a6b764e256ed00104752be88b6aebf77aea32))
* set default file path to current directory ([`2fce693`](https://github.com/adamkirchberger/nectl/commit/2fce693151dbf1ecec62ac06a5d6436857ced97c))
* site discovery issue ([`771fea8`](https://github.com/adamkirchberger/nectl/commit/771fea88928dc8d0462663cae731136619e8cd7f))
* skip empty render sections ([`aaa4cf5`](https://github.com/adamkirchberger/nectl/commit/aaa4cf52330f4fda8279962d489e989807e9e04f))
* update error for failed sub template import ([`f443628`](https://github.com/adamkirchberger/nectl/commit/f443628978ff0031d01c700e7f50f95298b4b058))

### Feature
* add single site datatree support ([`85b9468`](https://github.com/adamkirchberger/nectl/commit/85b946846a097e64ff5dee5a2e057a9f84fc3914))
* write configs to staged directory ([`2a35d1f`](https://github.com/adamkirchberger/nectl/commit/2a35d1f3ac32cfef5879278156a3fc46b687b27d))

## 0.6.0 (2022-01-11)
### Fix
* host types ([`3535e92`](https://github.com/adamkirchberger/nectl/commit/3535e927add7060e8ae06a929066958ce4e22f02))
* increase log severity for hosts missing os vars ([`472920b`](https://github.com/adamkirchberger/nectl/commit/472920b81d4c4c5104f42231bfb553660db600fc))
* issue related to frozen and merge data actions ([`6eceace`](https://github.com/adamkirchberger/nectl/commit/6eceacebb008d1efb7888873af846cc633415db5))
* rename config var for readability ([`c0eb13e`](https://github.com/adamkirchberger/nectl/commit/c0eb13e24c03c43d4b617e5a09bcf06767bd8e2b))
* separate render context functions ([`1032403`](https://github.com/adamkirchberger/nectl/commit/10324033c0ecdf3a538ecbc2b475211492c8402f))
* unset config env var during tests ([`a48133f`](https://github.com/adamkirchberger/nectl/commit/a48133ff61b93b3d4c8858dc2f0748d8e3d2b1c0))

### Feature
* add dict deep merging ([`bace069`](https://github.com/adamkirchberger/nectl/commit/bace069b08a49a73497dfcf01cb1646916d31186))

## 0.5.0 (2022-01-03)
### Fix
* log and raise any template import errors ([`ced65f4`](https://github.com/adamkirchberger/nectl/commit/ced65f494a67e5e093c7e3753e86431027211690))
* make get_config return same config every time ([`0b65de2`](https://github.com/adamkirchberger/nectl/commit/0b65de24a6e15c5637764f3ec452da0d2af07c2d))
* move render context out of try block ([`71776e1`](https://github.com/adamkirchberger/nectl/commit/71776e1680f89b28d45ff7d4b939c679d69ca39b))
* raise error for issues during discovery ([`f310cf8`](https://github.com/adamkirchberger/nectl/commit/f310cf8cde59674e9d1bb3383a88bc5cc147c290))
* raise render error only after all errors found ([`7fdaf43`](https://github.com/adamkirchberger/nectl/commit/7fdaf433d5b83c323292bc2038a8b89e51873063))
* remove unused imports and comments ([`a2f0434`](https://github.com/adamkirchberger/nectl/commit/a2f043459cf4ee9b6eaa51b30c4eddfaec73dd4b))
* replace additional calls for single dict iter ([`d396d9f`](https://github.com/adamkirchberger/nectl/commit/d396d9fe126fa06cfdda5eccba3d55ffdde5b3a4))
* resolve type issues ([`508465e`](https://github.com/adamkirchberger/nectl/commit/508465e7895a5ff19d66cd51709e199275bbd836))
* return None if host attr not found in facts ([`9863fe3`](https://github.com/adamkirchberger/nectl/commit/9863fe30cfd4b16ed56fa2ad303fe9430b7c96a3))
* rewrite block to catch multiple exceptions ([`1e8bccc`](https://github.com/adamkirchberger/nectl/commit/1e8bccc7339dab07e667bff9743d317d8e3b808f))
* set host customer value to optional ([`fb14a55`](https://github.com/adamkirchberger/nectl/commit/fb14a55778e406b7503bef4b1d246490f019c2fe))
* set logger level ([`0fbeffa`](https://github.com/adamkirchberger/nectl/commit/0fbeffaeee3981f016f1dfdd7b456143b353ffb5))
* templates render based on order of definition ([`05b62dc`](https://github.com/adamkirchberger/nectl/commit/05b62dc4939a61f28c8309a318cafd8e394fb021))

### Feature
* add render context ([`4881af1`](https://github.com/adamkirchberger/nectl/commit/4881af1eb187bb7d84c49a1a8c1656c51aa35040))
* templates are determined based on os_name ([`296267b`](https://github.com/adamkirchberger/nectl/commit/296267b5ae31435bcf3c6581160a7879da6fbf83))
* templates use functions with print methods ([`a5a8a54`](https://github.com/adamkirchberger/nectl/commit/a5a8a54e77666191110cfeb3e9ba681cb0b33853))
* update dependencies ([`e69edd5`](https://github.com/adamkirchberger/nectl/commit/e69edd505c6ea22cb416fe22f0dd6a82da765918))

## 0.4.0 (2021-12-19)
### Fix
* add git ignore for coverage files ([`ee4d3fa`](https://github.com/adamkirchberger/nectl/commit/ee4d3fa8d2c5715a46508e122f058a7e93289926))
* compile regex from string to avoid errors ([`ab2e99c`](https://github.com/adamkirchberger/nectl/commit/ab2e99c08dd275eeb2d16958d5a89ca2da8e4053))
* ignore protected variables ([`99323f3`](https://github.com/adamkirchberger/nectl/commit/99323f356701bf1b6cd0f94f2be3723b370e6b68))

### Feature
* add support for single tenant data tree ([`19e0e4a`](https://github.com/adamkirchberger/nectl/commit/19e0e4a05868e4d430cbf2b863c94f0798f3baf2))

## 0.3.0 (2021-09-26)
### Fix
* catch errors from invalid fact files ([`94fa23d`](https://github.com/adamkirchberger/nectl/commit/94fa23d13543644797f21f6476fa9a3816a7d7d2))
* default config get logic ([`f7b8489`](https://github.com/adamkirchberger/nectl/commit/f7b8489e65acf41cc077643dd19dc8558764992b))
* rename generate to render ([`9afe8cd`](https://github.com/adamkirchberger/nectl/commit/9afe8cdf61901453fc16beb0e2cd4b01a7a80125))
* rename host os to os_name for readability ([`3b7ac9f`](https://github.com/adamkirchberger/nectl/commit/3b7ac9f941de51947ae5c0f91395099b7600192a))
* rename os to os_name missed in prev commit ([`6bb9a20`](https://github.com/adamkirchberger/nectl/commit/6bb9a208bd5ed2fc30c8cac8bfc8a37f37248e82))
* rename os_regex to os_name_regex ([`b5c2aac`](https://github.com/adamkirchberger/nectl/commit/b5c2aac1745d9652916caf2e6e193545cdc8b0db))
* update arg order ([`24758df`](https://github.com/adamkirchberger/nectl/commit/24758df98ad633527b7c81db9c8bdb7f2bdace6d))
* update default logging level to error ([`bb369fc`](https://github.com/adamkirchberger/nectl/commit/bb369fc266a0cf188b3296872740bc9497bf487c))
* update template handling ([`addff3d`](https://github.com/adamkirchberger/nectl/commit/addff3d867cbaacc76a045d0cbc30ba18b1549c2))

### Feature
* merge cli groups for templates and configs ([`7dc9071`](https://github.com/adamkirchberger/nectl/commit/7dc9071ea2c7cd78dacf6da725fd23c94c46fa2c))
* rename blueprints to templates ([`b59b170`](https://github.com/adamkirchberger/nectl/commit/b59b170ecd0cebde5dccd8d0c9e11d56e8cd4942))

## 0.2.0 (2021-09-09)
### Fix
* logging config issue ([`ac44793`](https://github.com/adamkirchberger/nectl/commit/ac44793705696f20a1130c28af6c78e3b02d48ec))
* set default to none for optional fields ([`d864229`](https://github.com/adamkirchberger/nectl/commit/d864229b26705b3f40d35fcda81e0247ff3ca1b0))
* use consistent logging format ([`3ab3f01`](https://github.com/adamkirchberger/nectl/commit/3ab3f011118c57b16fe31319d7a20ca9f53184e1))

### Feature
* add template rendering using blueprints ([`ba8f8c5`](https://github.com/adamkirchberger/nectl/commit/ba8f8c53bc83df787ac8364ed26a75327b234bfc))

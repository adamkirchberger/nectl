<!--
 Copyright (C) 2022 Adam Kirchberger

 This file is part of Nectl.

 Nectl is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Nectl is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Nectl.  If not, see <http://www.gnu.org/licenses/>.
-->

# CI/CD

## Summary

Nectl can be run directly from engineer laptops using the CLI tool or via a CI/CD pipeline.

Integrating Nectl into a CI/CD pipeline has several advantages and this is the recommended approach.

## Advantages

- Audit trail for who and when a deployment was run including job outputs and logs.
- Avoid overlapping deployments to the same devices.
- Pass secrets via environment variables so they are not on engineer laptops.
- Avoid engineers needing direct network access to devices.
- Implement tests and checks that cannot be skipped.
- Troubleshooting is simpler as failed CI/CD pipeline links can be shared.
- Centralised analytics and monitoring of deployments.

## Examples

### Gitlab pipeline with 3 deployment groups

<details>
<summary>Expand code block</summary>

```yaml
---
image: nectl:latest

stages:
  - test
  - build
  - diff
  - deploy-1
  - deploy-2
  - deploy-3
  - validate

.common:
  artifacts:
    paths:
      - nectl.log

.mr_trigger:
  extends: .common
  only:
    refs:
      - merge_requests

.mr_and_deploy_trigger:
  extends: .common
  only:
    refs:
      - main
      - merge_requests

.deploy_trigger:
  extends: .common
  only:
    refs:
      - main

facts-check:
  extends: .mr_trigger
  stage: test
  script:
    - nectl --version
    - nectl datatree get-facts -v --check

hosts-check:
  extends: .mr_trigger
  stage: test
  script:
    - nectl --version
    - nectl datatree list-hosts -v

configs-render:
  extends: .mr_and_deploy_trigger
  stage: build
  script:
    - nectl --version
    - nectl configs render -v
  artifacts:
    expose_as: "configs-staged"
    paths:
      - "configs/staged/"
      - nectl.log

configs-diff:
  extends: .mr_trigger
  stage: diff
  script:
    - nectl --version
    - nectl configs diff -v
  artifacts:
    expose_as: "configs-diffs"
    paths:
      - "configs/diffs/"
      - nectl.log

configs-deploy-1:
  extends: .deploy_trigger
  stage: deploy-1
  when: manual
  script:
    - nectl --version
    - nectl configs apply -v -y --deployment-group prod_1
  artifacts:
    expose_as: "configs-deploy-1-diff"
    paths:
      - "configs/diffs/"
      - nectl.log

configs-deploy-2:
  extends: .deploy_trigger
  stage: deploy-2
  when: manual
  script:
    - nectl --version
    - nectl configs apply -v -y --deployment-group prod_2
  artifacts:
    expose_as: "configs-deploy-2-diff"
    paths:
      - "configs/diffs/"
      - nectl.log

configs-deploy-3:
  extends: .deploy_trigger
  stage: deploy-3
  when: manual
  script:
    - nectl --version
    - nectl configs apply -v -y --deployment-group prod_3
  artifacts:
    expose_as: "configs-deploy-3-diff"
    paths:
      - "configs/diffs/"
      - nectl.log
```

</details>

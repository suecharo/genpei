# Genpei (源平)

[![pytest](https://github.com/suecharo/genpei/workflows/pytest/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Apytest)
[![flake8](https://github.com/suecharo/genpei/workflows/flake8/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Aflake8)
[![isort](https://github.com/suecharo/genpei/workflows/isort/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Aisort)
[![mypy](https://github.com/suecharo/genpei/workflows/mypy/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Amypy)
[![Apache License](https://img.shields.io/badge/license-Apache%202.0-orange.svg?style=flat&color=important)](http://www.apache.org/licenses/LICENSE-2.0)

[Japanese Document](https://github.com/suecharo/genpei/blob/master/README_ja.md)

Genpei (源平) is a standard implementation conforming to the [Global Alliance for Genomics and Health](https://www.ga4gh.org) (GA4GH) [Workflow Execution Service](https://github.com/ga4gh/workflow-execution-service-schemas) (WES) API specification.
A simple and highly scalable REST API Server using [Flask](https://a2c.bitbucket.io/flask/) and [cwltool](https://github.com/common-workflow-language/cwltool) that follows the philosophy of Microservice.
It supports the execution and management of Workflow written in [Common Workflow Language](https://www.commonwl.org) (CWL).

## Install and Run

Genpei supports Python 3.6 or newer.

```bash
$ pip3 install genpei
$ genpei
```

### Docker

We also expect to launch using Docker.
Because of the compatibility of cwltool and Docker-in-Docker (DinD), you have to mount `docker.sock`, `/tmp`, etc.
Please check the documentation in [DockerHub - cwltool](https://hub.docker.com/r/commonworkflowlanguage/cwltool/) for more information.

```bash
# Launch
$ docker-compose up -d

# Launch confirmation
$ docker-compose logs
```

## Usage

As API specifications, please check [GitHub - GA4GH WES](https://github.com/ga4gh/workflow-execution-service-schemas) and [SwaggerUI - GA4GH WES](https://suecharo.github.io/genpei-swagger-ui/dist/).

As the simplest example of a REST API Request, here is the result of a `GET /service-info`.

```json
GET /service-info
{
  "auth_instructions_url": "https://github.com/suecharo/genpei",
  "contact_info_url": "https://github.com/suecharo/genpei",
  "default_workflow_engine_parameters": [],
  "supported_filesystem_protocols": [
    "http",
    "https",
    "file"
  ],
  "supported_wes_versions": [
    "1.0.0"
  ],
  "system_state_counts": {},
  "tags": {
    "wes_name": "genpei"
  },
  "workflow_engine_versions": {
    "cwltool": "3.0.20200324120055"
  },
  "workflow_type_versions": {
    "CWL": {
      "workflow_type_version": [
        "v1.0",
        "v1.1",
        "v1.1.0-dev1",
        "v1.2.0-dev1",
        "v1.2.0-dev2"
      ]
    }
  }
}
```

The host and port used by the application can be changed by specifying the startup arguments (`--host` and `--port`). And environment variables corresponding to these arguments are `GENPEI_HOST` and `GENPEI_PORT`.

```bash
$ genpei --help
usage: genpei [-h] [--host] [-p] [--debug] [-r] [--service-info]

An implementation of GA4GH Workflow Execution Service Standard as a microservice

optional arguments:
  -h, --help       show this help message and exit
  --host           Host address of Flask. (default: 127.0.0.1)
  -p , --port      Port of Flask. (default: 8080)
  --debug          Enable debug mode of Flask.
  -r , --run-dir   Specify the run dir. (default: ./run)
  --service-info   Specify `service-info.json`. The workflow_engine_versions, workflow_type_versions
                   and system_state_counts are overwritten in the application.

$ genpei --host 0.0.0.0 --port 5000
```

Genpei manages the submitted workflows, workflow parameters, output files, etc. on the file system. The location of run dir can be overridden by the startup argument `--run-dir` or the environment variable `GENPEI_RUN_DIR`.

The run dir structure is as follows. Initialization and deletion of each run can be done by physical deletion with `rm`.

```bash
$ tree run
.
├── 11
│   └── 11a23a68-a914-427a-80cd-9ad6f7cfd256
│      ├── cmd.txt
│      ├── end_time.txt
│      ├── exe
│      │   └── workflow_params.json
│      ├── exit_code.txt
│      ├── outputs
│      │   ├── ERR034597_1.small_fastqc.html
│      │   ├── ERR034597_1.small.fq.trimmed.1P.fq
│      │   ├── ERR034597_1.small.fq.trimmed.1U.fq
│      │   ├── ERR034597_1.small.fq.trimmed.2P.fq
│      │   ├── ERR034597_1.small.fq.trimmed.2U.fq
│      │   └── ERR034597_2.small_fastqc.html
│      ├── run.pid
│      ├── run_request.json
│      ├── start_time.txt
│      ├── state.txt
│      ├── stderr.log
│      └── stdout.log
├── 14
│   └── ...
├── 2d
│   └── ...
└── 6b
    └── ...
```

The execution of `POST /runs` is very complex. Examples using Python's [requests](https://requests.readthedocs.io/en/master/) are provided by [GitHub - genpei/tests/post_runs_examples](https://github.com/suecharo/genpei/tree/master/tests/post_runs_examples). Please use this as a reference

## Development

The development environment starts with the following.

```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app bash
```

We use [flake8](https://pypi.org/project/flake8/), [isort](https://github.com/timothycrosley/isort), and [mypy](http://mypy-lang.org) as the linter.

```bash
$ bash ./tests/lint_and_style_check/flake8.sh
$ bash ./tests/lint_and_style_check/isort.sh
$ bash ./tests/lint_and_style_check/mypy.sh
```

We use [pytest](https://docs.pytest.org/en/latest/) as a Test Tool.

```bash
$ pytest .
```

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](https://github.com/suecharo/genpei/blob/master/LICENSE).

- The Developer and Maintainer: [@suecharo](https://github.com/suecharo)
- The Godfather of this library: [@inutano](https://github.com/inutano)

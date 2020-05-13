# Genpei (源平)

[![pytest](https://github.com/suecharo/genpei/workflows/pytest/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Apytest)
[![flake8](https://github.com/suecharo/genpei/workflows/flake8/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Aflake8)
[![isort](https://github.com/suecharo/genpei/workflows/isort/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Aisort)
[![mypy](https://github.com/suecharo/genpei/workflows/mypy/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Amypy)

[Japanese Document](https://github.com/suecharo/genpei/blob/master/README_ja.md)

Genpei (源平) is a standard implementation conforming to the [Global Alliance for Genomics and Health](https://www.ga4gh.org) (GA4GH) [Workflow Execution Service](https://github.com/ga4gh/workflow-execution-service-schemas) (WES) API specification.
A simple and highly scalable REST API Server using [Flask](https://a2c.bitbucket.io/flask/) and [cwltool](https://github.com/common-workflow-language/cwltool) that follows the philosophy of Microservice.
It supports the execution and management of Workflow written in [Common Workflow Language](https://www.commonwl.org) (CWL).

## Install and Run

Genpei supports Python 3.5 or newer.

```bash
$ pip3 install genpei
$ genpei
```

### Docker

We also expect to run using Docker.
Because of the compatibility of cwltool and Docker-in-Docker (DinD), you have to mount `docker.dock`, `/tmp`, etc.
Please check the documentation in [DockerHub - cwltool](https://hub.docker.com/r/commonworkflowlanguage/cwltool/) for more information.

```bash
$ docker-compose up -d --build
$ docker-compose exec app genpei
```

## Usage

As API specifications, please check [GitHub - GA4GH WES](https://github.com/ga4gh/workflow-execution-service-schemas) and [SwaggerUI - GA4GH WES](https://suecharo.github.io/genpei-swagger-ui/dist/).

As the simplest example of a REST API Request, here is the result of a `GET /service-info`.

```bash
$ curl -X GET localhost:8080/service-info
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

Startup Option (`--host` and `--port`) of Genpei allows you to change the startup host and port.

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

Genpei manages submitted workflow files, workflow parameters, output files, etc. on the FileSystem. It is called `Run dir`. The location of default is `./run`. You can change the location of `Run dir` by specifying the startup option (`-r`).

The run dir structure looks like the following. There are various files related to each run. Initialization and deletion of each run can be done by physical deletion using `rm`.

```bash
$ tree run
.
├── 11
│   └── 11a23a68-a914-427a-80cd-9ad6f7cfd256
│       ├── cmd.txt
│       ├── end_time.txt
│       ├── exe
│       │   ├── ERR034597_1.small.fq.gz
│       │   ├── ERR034597_2.small.fq.gz
│       │   ├── fastqc.cwl
│       │   ├── trimming_and_qc.cwl
│       │   ├── trimmomatic_pe.cwl
│       │   └── workflow_params.json
│       ├── exit_code.txt
│       ├── outputs
│       │   ├── ERR034597_1.small_fastqc.html
│       │   ├── ERR034597_1.small_fastqc.html_2
│       │   ├── ERR034597_1.small.fq.trimmed.1P.fq
│       │   ├── ERR034597_1.small.fq.trimmed.1U.fq
│       │   ├── ERR034597_1.small.fq.trimmed.2P.fq
│       │   └── ERR034597_1.small.fq.trimmed.2U.fq
│       ├── run.pid
│       ├── run_request.json
│       ├── start_time.txt
│       ├── state.txt
│       ├── stderr.log
│       └── stdout.log
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

We use [flake8](https://pypi.org/project/flake8/), [isort](https://github.com/timothycrosley/isort), and [mypy](http://mypy-lang.org) as the Linter.

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

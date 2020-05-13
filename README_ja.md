# Genpei (源平)

[![pytest](https://github.com/suecharo/genpei/workflows/pytest/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Apytest)
[![flake8](https://github.com/suecharo/genpei/workflows/flake8/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Aflake8)
[![isort](https://github.com/suecharo/genpei/workflows/isort/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Aisort)
[![mypy](https://github.com/suecharo/genpei/workflows/mypy/badge.svg)](https://github.com/suecharo/genpei/actions?query=workflow%3Amypy)

Genpei (源平) は、[Global Alliance for Genomics and Health](https://www.ga4gh.org) (GA4GH) により制定された [Workflow Execution Service](https://github.com/ga4gh/workflow-execution-service-schemas) (WES) API 定義に準拠した標準実装です。
Microservice の思想に則り、[Flask](https://a2c.bitbucket.io/flask/) と [cwltool](https://github.com/common-workflow-language/cwltool) を用いており、[Common Workflow Language](https://www.commonwl.org) を用いて作られた、シンプルかつ拡張性の高い REST API Server です。
[Common Workflow Language](https://www.commonwl.org) (CWL) により書かれた Workflow の実行や管理をサポートします。

## Install and Run

Python 3.6 以上を想定しています。

```bash
$ pip3 install genpei
$ genpei
```

### Docker

Docker の利用も想定しています。
cwltool と Docker-in-Docker (DinD) の相性より、`docker.dock` や `/tmp` などを mount しなければなりません。
詳しくは、[DockerHub - cwltool](https://hub.docker.com/r/commonworkflowlanguage/cwltool/) のドキュメントを確認してください。

```bash
$ docker-compose up -d --build
$ docker-compose exec app genpei
```

## Usage

API 仕様は、[GitHub - GA4GH WES](https://github.com/ga4gh/workflow-execution-service-schemas) や [SwaggerUI - GA4GH WES](https://suecharo.github.io/genpei-swagger-ui/dist/) を確認してください。

一番簡単な REST API Request として、`GET /service-info` の例を挙げます。

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

Genpei の起動 Option (`--host` and `--port`) を指定することで、起動 Host や Port を変更できます。

```bash
genpei --help
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

Genpei は、投入された workflow file や workflow parameter、output files などを FileSystem 上で管理しています。System 上では Run dir と呼んでおり、default は `./run` です。Run dir の場所は、起動 Option (`-r`) で指定することで、変更できます。

Run dir 構造は、以下のようになっており、それぞれの run に関わる様々な file 群が配置されています。初期化やそれぞれの run の削除は `rm` を用いた物理的な削除により行えます。

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

`POST /runs` の実行は非常に複雑です。Python の [requests](https://requests.readthedocs.io/en/master/) を用いた例として、[GitHub - genpei/tests/post_runs_examples](https://github.com/suecharo/genpei/tree/master/tests/post_runs_examples) が用意されています。参考にしてください。

## Development

開発環境は以下で起動します。

```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app bash
```

Lint Tool として、[flake8](https://pypi.org/project/flake8/), [isort](https://github.com/timothycrosley/isort), [mypy](http://mypy-lang.org) を用いています。

それぞれの実行方法は以下のとおりです。

```bash
$ bash ./tests/lint_and_style_check/flake8.sh
$ bash ./tests/lint_and_style_check/isort.sh
$ bash ./tests/lint_and_style_check/mypy.sh
```

Test Tool として、[pytest](https://docs.pytest.org/en/latest/) を用いてます。

実行方法は以下のとおりです。

```bash
$ pytest .
```

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](https://github.com/suecharo/genpei/blob/master/LICENSE).

- The Developer and Maintainer: [@suecharo](https://github.com/suecharo)
- The Godfather of this library: [@inutano](https://github.com/inutano)

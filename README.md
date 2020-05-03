# stayhome_wes a.k.a Genpei(源平)

![Lint and Style Check](https://github.com/suecharo/stayhome_wes/workflows/Lint%20and%20Style%20Check/badge.svg)

- 後から追記していく
- 英語に書き直す (はず)

## やりたいこと

- GA4GH WES の標準実装を実際に作ってみる
- なるべく簡単かつ薄く作ってみる
  - pip install -> exec command のみで local で動作する
- cwltool を直持ちさせて、pip install 時に使用する
  - 内部で import して実行する

## Environment

- Docker
  - もし cwltool が使うのならば
- Python 3.6 以上

- 開発時は Docker and docker-compose を使って開発しているが、動作としては、local への pip install を想定する
  - for cwltool のための、docker sibling mount がめんどくさい

### Develop

```
$ docker-compose up -d --build
$ docker-compose exec app bash
```

## Lisense

Apache 2.0

The Godfather of this library: inutano

## Reference

TODO

- Sapporo WES
- WES-ELIXIR
- GA4GH Cloud Work Stream
  - https://www.ga4gh.org/work_stream/cloud/
- GA4GH WES
  - https://github.com/ga4gh/workflow-execution-service-schemas

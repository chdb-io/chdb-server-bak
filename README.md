<a href="https://chdb.fly.dev" target="_blank">
  <img src="https://avatars.githubusercontent.com/u/132536224" width=140 />
</a>

[![.github/workflows/release.yml](https://github.com/chdb-io/chdb-server/actions/workflows/release.yml/badge.svg)](https://github.com/chdb-io/chdb-server/actions/workflows/release.yml)

# chdb-server
[chDB](https://github.com/auxten/chdb) + basic HTTP/s API server in a docker container, _pretending to be ClickHouse_

### [Public Demo](https://chdb.fly.dev/)

<br>

<a href="https://flyctl.sh/shell?repo=chdb-io/chdb-server" target="_blank">
  <img src="https://user-images.githubusercontent.com/1423657/236479471-a1cb0484-dfd3-4dc2-8d62-121debd7faa3.png" width=300>
</a>

<br><br>


### Docker Setup
```
docker run --rm -p 8123:8123 ghcr.io/chdb-io/chdb-server:latest
```

<br>

### Stateless & Stateful Sessions

> chdb-server queries default to stateless. Stateful sessions can be paired with Basic HTTP Auth.

![image](https://github.com/chdb-io/chdb-server/assets/1423657/dee938a2-ec2a-4b4a-87a9-458a6db791a0)

<br>

### ClickHouse Play
chdb-server is compatible with the ClickHouse Play query interface:
<a href="https://chdb.fly.dev/?user=default#U0VMRUNUCiAgICB0b3duLAogICAgZGlzdHJpY3QsCiAgICBjb3VudCgpIEFTIGMsCiAgICByb3VuZChhdmcocHJpY2UpKSBBUyBwcmljZQpGUk9NIHVybCgnaHR0cHM6Ly9kYXRhc2V0cy1kb2N1bWVudGF0aW9uLnMzLmV1LXdlc3QtMy5hbWF6b25hd3MuY29tL2hvdXNlX3BhcnF1ZXQvaG91c2VfMC5wYXJxdWV0JykKR1JPVVAgQlkKICAgIHRvd24sCiAgICBkaXN0cmljdApMSU1JVCAxMA==" target="_blank">
  <img src="https://user-images.githubusercontent.com/1423657/232862594-21bacfb1-e4f3-467f-a409-5d4f6a62ab4b.png">
</a>

### Grafana
chdb-server is compatible with Grarfana using the official ClickHouse drivers:

![image](https://github.com/chdb-io/chdb-server/assets/1423657/cfe60c6d-c714-44b1-bca4-893c287a17e4)


### Superset
chdb-server is compatible with Superset and the ClickHouse sqlalchemy driver:

##### SQLALCHEMY URI
```
clickhouse+http://chdb.fly.dev:443/db?protocol=https
```



![image](https://github.com/chdb-io/chdb-server/assets/1423657/b6291840-4e24-492b-a386-548d3bcce5fe)

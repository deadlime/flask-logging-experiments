# Flask logging experiments

This is a complementary repository for the following blog post:

[A bug's life](https://deadlime.hu/en/2023/02/03/a-bugs-life/) (english)\
[Egy hiba élete](https://deadlime.hu/2023/02/03/egy-hiba-elete/) (hungarian)

To install dependencies run:

```shell
$ pipenv install
```

The examples can be run with the following command:

```shell
$ pipenv run gunicorn --bind 0.0.0.0:8080 --worker-class gevent --reload <version>:app
```

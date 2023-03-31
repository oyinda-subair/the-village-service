# the-village-service
The backend service for the village app

Local Setup
Ensure you have a PYTHONPATH

```bash
export PYTHONPATH=$PWD
```

Install dependency
```bash
$ poetry install
```

setup database
```bash
poetry run scripts/prestart.sh
```

Run Test

```bash
ENVIRONMENT=test poetry run -m pytest
```
or run the command in the shell
```bash
./scripts/test.sh
```
to run specific file
```bash
​​pytest​​ ​​-v​​ ​​tasks/test_four.py::test_asdict​
```
or
```bash
./scripts/test.sh ​-v​​ ​​tasks/test_four.py::test_asdict​
```

To run test with  covarege report

```bash
ENVIRONMENT=test  poetry run coverage run -m pytest && poetry run coverage report -m
```
or run the command in the poetry shell
./scripts/testcov.sh

Start the Service

```bash
poetry run scripts/dev.sh
```


```bash
rm -rf `poetry env info -p`
```

```bash
$ dropdb my_db
$ createdb my_db
$ alembic upgrade head
```
```bash
alembic downgrade base
```
This command will undo all migrations.

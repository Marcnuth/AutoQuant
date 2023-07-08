
# Contribution Guide

## Test
### Test all
```shell
PYTHONPATH=./ pytest
```

### Test specified test
```shell
PYTHONPATH=./ pytest tests/<YOUR_DISIRE_FILE>.py -k "<YOUR_DISIRE_TEST_CASE>" -s
```


## Development

### Generate Requirements

```shell
pipreqs ./ --encoding=utf8 --force
```
### Package Update

```shell
python3 -m build 
python3 -m twine upload dist/*
```
# TOML

>[TOML](https://en.wikipedia.org/wiki/TOML) is a file format for configuration files. It is intended to be easy to read and write, and is designed to map unambiguously to a dictionary. Its specification is open-source. `TOML` is implemented in many programming languages. The name `TOML` is an acronym for "Tom's Obvious, Minimal Language" referring to its creator, Tom Preston-Werner.

If you need to load `Toml` files, use the `TomlLoader`.


```python
from langchain.document_loaders import TomlLoader
```


```python
loader = TomlLoader("example_data/fake_rule.toml")
```


```python
rule = loader.load()
```


```python
rule
```




    [Document(page_content='{"internal": {"creation_date": "2023-05-01", "updated_date": "2022-05-01", "release": ["release_type"], "min_endpoint_version": "some_semantic_version", "os_list": ["operating_system_list"]}, "rule": {"uuid": "some_uuid", "name": "Fake Rule Name", "description": "Fake description of rule", "query": "process where process.name : \\"somequery\\"\\n", "threat": [{"framework": "MITRE ATT&CK", "tactic": {"name": "Execution", "id": "TA0002", "reference": "https://attack.mitre.org/tactics/TA0002/"}}]}}', metadata={'source': 'example_data/fake_rule.toml'})]




```python

```

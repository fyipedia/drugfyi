# drugfyi

Drug interactions and pharmacology API client — [drugfyi.com](https://drugfyi.com)

## Install

```bash
pip install drugfyi
```

## Quick Start

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    results = api.search("ibuprofen")
    print(results)
```

## License

MIT

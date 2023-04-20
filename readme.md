# Joshua

Joshua is a light-weight python wsgi

## Installation
Inside of project
```bash
git clone https://github.com/aludayalu/joshua
```
## Usage

```python
import joshua

def home_page(query_string,env):
    return {"data":"Hello World!"}

joshua.start_server(port=8080,routes={"/":home_page})
```

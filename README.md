# Tezos API Noobs

A collection of community scripts to access public Tezos API and collect data from it.

- `sudo apt-get install git`
- `git clone https://github.com/hclivess/tezos_api_noobs`
- `sudo apt-get install Python3.9`
- `sudo apt install python3-pip`
- `sudo Python3.9 -m pip install -f requirements.txt`
- `sudo Python3.9 [filename].py`

All `.json` files are just structured examples of individual operations for easy navigation in element identification.

## API data structure
There are two types of data structures in this API:
### list
- introduced as `[]`
- example: `["hello", 100, 500, "world"]`

#### we access list values with index numbers:
- `list[0]` returns `"hello"`
- `list[1]` returns `100`
- `list[2]` returns `500`
- `list[3]` returns `"world"`

### dictionary
- introduced with `{}`
- example: `{"operation": "sell", "name": "john", "age": 50}`

#### we access dictionary values with keys
- `dictionary["operation"]` returns `"sell"`
- `dictionary["name"]` returns `"john"`
- `dictionary["operation"]` returns `50`

### combined data structures
What API usually returns are combined and nested data structures, simplified examples:
- `[{transactions: ["{"name": "transaction1", "value": 50}, {"name": "transaction2", "value": 50}}]`

To see how this is done in practice, open individual Python files in this directory. Examples returned for each of this files are stored in the corresponding json files.
To format a json file to make it more readable, try a service like  [curiousconcept url formatter](https://jsonformatter.curiousconcept.com).
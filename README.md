# Universal Tennis Ranking (UTR) Tracker
Keep track of your tennis performance using [UTR](https://universaltennis.com/rankings).

## Installation

1. Clone this repository.
2. Install dependencies.
3. Run `python3 src/main.py.`

## Usage

### Logging In

A UTR login must be provided to obtain data. This can be provided as arguments.
```
python3 src/main.py --username=<USER> --password=<PASSWORD>
```

Alternatively, these can be referenced as system environment variables `UTR_USERNAME` and `UTR_PASSWORD`.


### Recording Data

A custom path can be provided to record data in `csv` format:


```
python3 src/main.py --save --database=<PATH>.csv
```

This will create a new file if not found, otherwise will append to the file.

### Viewing Data

Historical UTR can be viewed using the `--graph` argument:

```
python3 src/main.py --graph --database=<PATH>.csv
```

## Automation

Logging of UTR can be automated to run daily/weekly/monthly by following these steps:

### Linux/Mac

1. In a browser, visit https://crontab.guru/ to generate a crontab frequency expression.
2. In terminal, open up `crontab` using the command `crontab -e`.
3. Paste the following command with your custom paths and frequency:

```
<FREQUENCY_EXPRESSION> source <PATH_TO_LOGIN_INFO>.sh && /usr/bin/python3 $HOME/Git/utr-tracker/src/main.py --save --database="<PATH>.csv" 2>&1
```
4. Save and exit.

### Windows
TBC.

## License

This project is covered under the terms described in [LICENSE](LICENSE).


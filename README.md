# Scraping Rent
> test task for https://www.lun.ua/

Scraping system which collect daily apartments rent calendar

## Installing / Getting started

A quick introduction of the minimal setup you need to prepare system

For python3.5(May be root required)
```shell
add-apt-repository ppa:fkrull/deadsnakes
apt-get update
apt-get install python3.5
```

For lxml(May be root required)
```shell

```


## How to Run

Few to stages to setup project

```shell
git clone https://github.com/BogBel/scraping-rent.git
cd scraping-rent/
virtualenv -p /usr/bin/python3.5 .env
source .env/bin/activate
pip install -r requirements.txt
```

- Clone project
- go to project folder
- create environment
- activate it
- install required packages


## Features

Just collect data from sources and
* Store in stdout
* Save to json

## Configuration

#### --write FILENAME

Will save result data to FILENAME.json

Example:
```bash
python scrape.py --write calendar  # save data to calendar.json
```

#### --show

Will print result to stdout

Example:
```bash
python scrape.py --show
```

#### --debug

Show requests url

Example:
```bash
python scrape.py --debug
```

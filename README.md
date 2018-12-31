[![Build Status](https://travis-ci.org/stmcli/stmcli.svg?branch=master)](https://travis-ci.org/stmcli/stmcli)
# stmcli
The unofficial STM CLI client.

stmcli aims to use the data made available by the [Société de transport de Montréal](http://www.stm.info/)
to create an easy to use command line application to access bus/metro informations.

This tool does not use any information of STM real time. It only retrieve the scheduled times for bus. 

## Installation

``` pip3 install stmcli ```

(stmcli is only compatible with python3+ and GNU/Linux)

## Usage

```
usage: stmcli [-h] [-b BUS_NUMBER] [-s BUS_STOP_CODE] [-n NUMBER_DEPARTURE]
              [-d DATE] [-t TIME] [-m METRO] [-y]

optional arguments:
  -h, --help            show this help message and exit
  -b BUS_NUMBER, --bus-number BUS_NUMBER
                        # of the bus
  -s BUS_STOP_CODE, --bus-stop-code BUS_STOP_CODE
                        Code of the bus stop
  -n NUMBER_DEPARTURE, --number-departure NUMBER_DEPARTURE
                        The number of departures to print. Only works with
                        both -b and -s specified
  -d DATE, --date DATE  specify the date to use when getting Departure times.
                        Format: aaaammjj
  -t TIME, --time TIME  specify the time to use when getting Departure times.
                        Format: HH:MM
  -m METRO, --metro METRO
                        print the metro status for a given line require an
                        internet connection. Accepted options: green, orange,
                        yellow, blue and all
  -y, --force-update    Do not ask before updating
```
### Bus
To get the next departures times you need to specify at least -b and -s which are the bus number and the bus stop code.

For example: ``` stmcli -b 150 -s 52150 ```

would print the next 10 departures times of the bus "150 René-Lévesque EST" at the "du Sussex / René-Lévesque (52150)" bus stop.

If you don't know your bus stop code or your bus number you can specify only -b or -s. specifying only -b will print all of the bus stop and -s alone will print all bus number for this stop code.

By using the -d and/or the -t arguments you can get bus departures times from sometime in the future.

For example: ``` stmcli -b 150 -s 52150 -d 20160328 -t 06:30 ```

Would print almost the same thing as our first example The only exception is that it will print the 10 next departures after 6:30 AM on march 28th 2016.

### Metro
You can also get the current status of the metro with ```-m```.

For example: ``` stmcli -m green ``` will give you the current status of the green line.

## Language

You can switch the output language of stmcli by editing your ```~/.stmcli/lang.txt```. (The file is generated the first time you run stmcli)
The default is english.

Switch to french with: ```echo "fr" > ~/.stmcli/lang.txt```

Switch to english with: ```echo "en" > ~/.stmcli/lang.txt```

## Developper
Some information to generate a new package for local deployment

* python3 setup.py bdist_wheel
* pip3 install stmcli-1.*-py3-none-any.whl --user --upgrade
* Linux user: the stmcli command is available at $HOME/.local/bin/stmcli
* Verify installed is available: TBD

### Investigate database

By default, the database is createdin ~/.stmcli/stm.db as sqlite format.

Useful tool will be sqlitebrowser https://github.com/sqlitebrowser/sqlitebrowser

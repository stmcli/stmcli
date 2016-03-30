#!/bin/bash


echo "data.check_for_update()"
echo "data.download_gtfs_data()"
echo "database.create_db()"
echo "database.init_table()"
echo "database.load_stm_data()"
echo "database.load_data()"
stmcli -y
if [[ $? -ne 0 ]]
then
  echo "Update Failed"
fi

echo "---------printinfo.next_departures()---------"
stmcli -s 51253 -b 435
if [[ $? -ne 0 ]]
then
  echo "printinfo.next_departures() Failed"
fi

echo "---------main() (custom time test)---------"
stmcli -s 51253 -b 435 -t 10:30
if [[ $? -ne 0 ]]
then
  echo "main() (custom time test) Failed"
fi

echo "---------printinfo.all_bus_for_stop_code()---------"
stmcli -s 51253
if [[ $? -ne 0 ]]
then
  echo "printinfo.all_bus_for_stop_code() Failed"
fi

echo "---------printinfo.all_bus_stop()---------"
stmcli -b 435
if [[ $? -ne 0 ]]
then
  echo "printinfo.all_bus_stop() Failed"
fi

echo "Not tested yet : data.date_in_scope()"

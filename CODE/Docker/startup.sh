#!/bin/bash
cd public_mm
./bin/install.sh <<< $'\n'
./bin/skrmedpostctl start
./bin/wsdserverctl start
cd ..
./solr_server/solr-8.5.0/bin/solr start -force &
./apache-tomcat-9.0.34/bin/startup.sh
cd ..
cd DataIndexer
python3 ./src/MetaMapServerBroker.py &
cd ..









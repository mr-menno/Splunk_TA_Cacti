#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import subprocess

#valid arguments available?
if len(sys.argv)<2:
	sys.stderr.write('[cacti_lookup_mirage] missing cacti path\n')
	exit(1)

cacti_path = sys.argv[1]
cacti_config_file = cacti_path + '/include/config.php'
try: 
	cacti_config = open(cacti_config_file).read()
except:
	sys.stderr.write('[cacti_lookup_mirage] failed to read '+cacti_config_file+'\n');
	exit(1)

cacti_config_database_type = re.search('database_type\s*=\s*[\"\']([^\'\"]+)',cacti_config).group(1)
cacti_config_database_db = re.search('database_default\s*=\s*[\"\']([^\'\"]+)',cacti_config).group(1)
cacti_config_database_hostname = re.search('database_hostname\s*=\s*[\"\']([^\'\"]+)',cacti_config).group(1)
cacti_config_database_username = re.search('database_username\s*=\s*[\"\']([^\'\"]+)',cacti_config).group(1)
cacti_config_database_password = re.search('database_password\s*=\s*[\"\']([^\'\"]+)',cacti_config).group(1)
cacti_config_database_port = re.search('database_port\s*=\s*[\"\']([^\'\"]+)',cacti_config).group(1)

dbQuery = 'SELECT B.local_data_id, B.name_cache, A.host_id, '
dbQuery += 'E.description, E.hostname, F.data_source_type_id '
dbQuery += 'FROM (data_local A, data_template_data B) '
dbQuery += 'LEFT JOIN data_input C ON (C.id = B.data_input_id) '
dbQuery += 'LEFT JOIN data_template D ON (A.data_template_id = D.id) '
dbQuery += 'LEFT JOIN host E ON (A.host_id = E.id) '
dbQuery += 'LEFT JOIN data_template_rrd F ON (A.id = F.local_data_id) '
dbQuery += 'WHERE A.id = B.local_data_id ORDER BY B.local_data_id ASC;'

try:
	results = subprocess.check_output('mysql --user="'+cacti_config_database_username+'" --password="'+cacti_config_database_password+'" --host="'+cacti_config_database_hostname+'" -P'+cacti_config_database_port+' -D '+cacti_config_database_db+' -e "'+dbQuery+'" -B | sed \'s/,/-/g\' | sed \'s/\t/,/g\'',shell=True)
except:
	sys.stderr.write('[cacti_lookup_mirage] failed to run mysql client\n')
	sys.stderr.write('[cacti_lookup_mirage] mysql --user="..." --password="..." --host="'+cacti_config_database_hostname+'" -P'+cacti_config_database_port+' -D '+cacti_config_database_db+'\n')
sys.stdout.write(results);

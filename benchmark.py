#! /usr/bin/python

"""
Dependencies:
 
    pip install tabulate simplejson
    pip install dict2xml
    pip install protobuf
    pip install avro
    pip install pyyaml
    pip install msgpack
 
"""

from timeit import timeit 
from tabulate import tabulate
import sys 
import os
import io

message = '''d = {
    'PackageID' : 1539,
    'PersonID' : 33,
    'Name' : """MEGA_GAMER_2222""",
    'Inventory': dict((str(i),i) for i in iter(range(100))),  
    'CurrentLocation': """
		Pentos is a large port city, more populous than Astapor on Slaver Bay, 
		and may be one of the most populous of the Free Cities. 
		It lies on the bay of Pentos off the narrow sea, with the Flatlands 
		plains and Velvet Hills to the east.
		The city has many square brick towers, controlled by the spice traders. 
		Most of the roofing is done in tiles. There is a large red temple in 
		Pentos, along with the manse of Illyrio Mopatis and the Sunrise Gate 
		allows the traveler to exit the city to the east, 
		in the direction of the Rhoyne.
		"""
}'''

setup_pickle    = '%s ; import pickle ; src = pickle.dumps(d, 2)' % message
setup_json      = '%s ; import json; src = json.dumps(d)' % message
setup_yaml      = '%s ; import yaml; src = yaml.dump(d, Dumper = yaml.CDumper)' % message
setup_msgpack   = '%s ; import msgpack; src = msgpack.dumps(d)' % message
with open('xml_test.py', 'r') as xml_test:
    setup_xml = xml_test.read()
    xml_test.close()
with open('Protobuf/proto_test.py', 'r') as protobuf_test:
    setup_protobuf = protobuf_test.read()
    protobuf_test.close()
with open('ApacheAvro/avro_test.py', 'r') as avro_test:
    setup_avro = avro_test.read()
    avro_test.close()
with open('ApacheAvro/avro_test_serialize.py', 'r') as avro_test_serialize:
    setup_avro_serialize = avro_test_serialize.read()
    avro_test_serialize.close()
with open('ApacheAvro/avro_test_deserialize.py', 'r') as avro_test_deserialize:
    setup_avro_deserialize = avro_test_deserialize.read()
    avro_test_deserialize.close()

tests = [
    # (title, setup, enc_test, dec_test)
    ('pickle (native serialization)', 'import pickle; %s' % setup_pickle, 'pickle.dumps(d, 2)', 'pickle.loads(src)'),
    ('json', 'import json; %s' % setup_json, 'json.dumps(d)', 'json.loads(src)'),
    ('xml', setup_xml, 'dict2xml(d)', 'parseString(src)'),
    ('protobuf', setup_protobuf, 'src = Parse(json.dumps(d), Person())', 'message.ParseFromString(src)'),
    ('avro', setup_avro, setup_avro_serialize, setup_avro_deserialize),
    ('yaml', 'import yaml; %s' % setup_yaml, 'yaml.dump(d, Dumper = yaml.CDumper)', 'yaml.load(src, Loader = yaml.CLoader)'),
    ('msgpack', 'import msgpack; %s' % setup_msgpack, 'src = msgpack.dumps(d)', 'msgpack.loads(src)'),
]

loops = 5000
enc_table = []
dec_table = []

print ("Running tests (%d loops each)" % loops)
 
for title, mod, enc, dec in tests:
    print (title)
 
    print ("  [Encode]", enc) 
    result = timeit(enc, mod, number=loops)
    exec (mod)

    enc_table.append([title, result, sys.getsizeof(src)])

    print ("  [Decode]", dec) 
    result = timeit(dec, mod, number=loops)
    dec_table.append([title, result])

enc_table.sort(key=lambda x: x[1])
enc_table.insert(0, ['Package', 'Seconds', 'Size'])
 
dec_table.sort(key=lambda x: x[1])
dec_table.insert(0, ['Package', 'Seconds'])
 
print ("\nEncoding Test (%d loops)" % loops)
print (tabulate(enc_table, headers="firstrow"))
 
print ("\nDecoding Test (%d loops)" % loops)
print (tabulate(dec_table, headers="firstrow"))
try:
    writer.close()
except Exception:
    pass
reader = DataFileReader(open("ApacheAvro/people.avro", "rb"), DatumReader())
reader.close()
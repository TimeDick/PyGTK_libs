import csv, _csv
class CSV_Error(_csv.Error):
    pass
    
class CSV_Functions:
    @staticmethod
    def get_sniffed_reader( filename, size=1024 ):
        csvfile = open(filename, "rb")
        dialect = csv.Sniffer().sniff(csvfile.read(size))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        return reader
    
    @staticmethod
    def get_reader( filename, delimiter=';', quotechar='"', dialect=csv.excel):
        reader = csv.reader(open(filename, 'rb'), dialect=dialect)
        return reader
    
    @staticmethod
    def get_writer( filename, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, dialect=csv.excel ):
        writer = csv.writer(open(filename, 'wb'), dialect=dialect)
        return writer
        
    @staticmethod
    def set_data( writer, data ):
        writer.writerow( data )
        
    def opencsv(filename):
        tfile = open(filename, "r")
        line  = tfile.readline()
        tfile.close()
        if   line[0] == '"':
            quote_char = '"'
            quote_opt  = csv.QUOTE_ALL
        elif line[0] == "'":
            quote_char = "'"
            quote_opt  = csv.QUOTE_ALL
        else:
            quote_char = '"'
            quote_opt  = csv.QUOTE_MINIMAL
        
        if   line.find('\t') != -1:
            delim_char = '\t'
        else:
            delim_char = ','
        
        tfile  = open(filename, "rb")
        reader = csv.reader(tfile, delimiter=delim_char, quotechar=quote_char, quoting=quote_opt)
        return (tfile, reader)
        
        
import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = open(f, 'wb')
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

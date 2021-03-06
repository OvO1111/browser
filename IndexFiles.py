#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

import jieba
import urllib2
import re, nltk
from bs4 import BeautifulSoup

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""


def pick_charset(html):
    charset = None
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(html)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    return charset


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)

        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        COUNT = 1
        stat2 = datetime.now()

        for root, dirnames, filenames in os.walk(root):
            print root
            try:
                sroot = unicode(root, 'utf-8')
                print sroot
            except:
                print "************ unicode error ************"

            for filename in filenames:
                if filename.endswith(('jpg', 'exe')):
                    continue
                print "adding", filename
                try:
                    '''stat1 = datetime.now()
                    if stat2-stat1>'00.00:00:00.10':
                        print 'timeout'
                        continue'''
                    path = unicode(root, 'GBK')
                    path = os.path.join(sroot, filename)
                    print "read file", path
                    doc = Document()
                    with open("index2.txt", "r") as myfile:
                        for i in myfile:
                            if filename in i:
                                head = i.split()[0]
                                doc.add(Field("url", head, t1))
                                break
                    url = urllib2.urlopen(head).read()

                    charset = pick_charset(url)
                    print charset.upper()
                    file = open(path)

                    contents = unicode(file.read(), charset)
                    contents = jieba.cut(contents)
                    contents = ''.join(contents).encode('utf-8')
                    # contents = unicode(file.read(), 'gbk')
                    file.close()

                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", path, t1))
                    with open("html_test/"+filename, "r") as fp:
                        p = re.compile('<title>.*</title>', re.DOTALL)
                        for line in fp:
                            if "<title>" in line.decode(charset.upper()):
                                title = re.findall(p, line)[0].decode("string_escape")
                                print str(title).strip('<title>').strip('</title>')
                                title = str(title).strip('<title>').strip('</title>')
                                doc.add(Field("title", title, t1))
                                break

                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
                    else:
                        print "warning: no content in %s" % filename
                    if COUNT:
                        writer.commit()
                        COUNT = 0
                    writer.addDocument(doc)
                    # stat2 = datetime.now()
                except Exception, e:
                    print "Failed in indexDocs:", e


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('html_test', "index")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e

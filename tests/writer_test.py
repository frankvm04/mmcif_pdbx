##
# File:    writerTests.py
# Author:  jdw
# Date:    3-November-2009
# Version: 0.001
#
# Update:
#  5-Apr-2011 jdw   Using the double quote format preference
# 24-Oct-2012 jdw   Update path and examples.
##
"""
Test implementing PDBx/mmCIF write and formatting operations.

"""
__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"



import sys, unittest, traceback
import sys, time, os, os.path, shutil

from pdbx.reader.reader  import PdbxReader
from pdbx.writer.writer  import PdbxWriter
from pdbx.reader.containers import *

class writerTests(unittest.TestCase):
    def setUp(self):
        self.lfh=sys.stderr
        self.verbose=False
        self.pathPdbxDataFile     ="tests/data/1kip.cif"
        self.pathOutputFile       ="testOutputDataFile.cif"

    def tearDown(self):
        pass

    def testWriteDataFile(self): 
        """Test case -  write data file 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myDataList=[]
            ofh = open("test-output.cif", "w")
            current_container=DataContainer("myblock")
            aCat=DataCategory("pdbx_seqtool_mapping_ref")
            aCat.append_attribute("ordinal")
            aCat.append_attribute("entity_id")
            aCat.append_attribute("auth_mon_id")
            aCat.append_attribute("auth_mon_num")
            aCat.append_attribute("pdb_chain_id")
            aCat.append_attribute("ref_mon_id")
            aCat.append_attribute("ref_mon_num")                        
            aCat.append((1,2,3,4,5,6,7))
            aCat.append((1,2,3,4,5,6,7))
            aCat.append((1,2,3,4,5,6,7))
            aCat.append((1,2,3,4,5,6,7))
            current_container.append(aCat)
            myDataList.append(current_container)
            pdbxW=PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()
        except:
            traceback.print_exc(file=sys.stderr)
            self.fail()

    def testUpdateDataFile(self): 
        """Test case -  write data file 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            # Create a initial data file --
            #
            myDataList=[]
            ofh = open("test-output-1.cif", "w")
            current_container=DataContainer("myblock")
            aCat=DataCategory("pdbx_seqtool_mapping_ref")
            aCat.append_attribute("ordinal")
            aCat.append_attribute("entity_id")
            aCat.append_attribute("auth_mon_id")
            aCat.append_attribute("auth_mon_num")
            aCat.append_attribute("pdb_chain_id")
            aCat.append_attribute("ref_mon_id")
            aCat.append_attribute("ref_mon_num")                        
            aCat.append((1,2,3,4,5,6,7))
            aCat.append((1,2,3,4,5,6,7))
            aCat.append((1,2,3,4,5,6,7))
            aCat.append((1,2,3,4,5,6,7))
            current_container.append(aCat)
            myDataList.append(current_container)
            pdbxW=PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()
            #
            # Read and update the data -
            # 
            myDataList=[]
            input_file = open("test-output-1.cif", "r")
            pRd=PdbxReader(input_file)
            pRd.read(myDataList)
            input_file.close()
            #
            myBlock=myDataList[0]
            myBlock.print_it()
            myCat=myBlock.get_object('pdbx_seqtool_mapping_ref')
            myCat.print_it()
            for irow in range(0,myCat.row_count):
                myCat.set_value('some value', 'ref_mon_id',irow)
                myCat.set_value(100, 'ref_mon_num',irow)
            ofh = open("test-output-2.cif", "w")            
            pdbxW=PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()            
            
        except:
            traceback.print_exc(file=sys.stderr)
            self.fail()

    def testReadDataFile(self): 
        """Test case -  read data file 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        myDataList=[]
        input_file = open(self.pathPdbxDataFile, "r")
        pRd=PdbxReader(input_file)
        pRd.read(myDataList)
        input_file.close()            

    def testReadWriteDataFile(self): 
        """Test case -  data file read write test
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        myDataList=[]
        input_file = open(self.pathPdbxDataFile, "r")            
        pRd=PdbxReader(input_file)
        pRd.read(myDataList)
        input_file.close()            
        
        ofh = open(self.pathOutputFile, "w")
        pWr=PdbxWriter(ofh)
        pWr.write(myDataList)        
        ofh.close()

def suite():
    return unittest.makeSuite(writerTests,'test')

if __name__ == '__main__':
    unittest.main()

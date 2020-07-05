##
# File:    PdbxReadWriteTests.py
# Author:  jdw
# Date:    9-Oct-2011
# Version: 0.001
#
# Updated:
#         24-Oct-2012 jdw update path details and reorganize.
#
##
"""  Various tests caess for PDBx/mmCIF data file and dictionary reader and writer. 
"""

__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"

import sys, unittest, traceback
import sys, time, os, os.path, shutil

from pdbx.reader.reader import PdbxReader
from pdbx.writer.writer import PdbxWriter
from pdbx.reader.containers import *


class PdbxReadWriteTests(unittest.TestCase):
    def setUp(self):
        self.lfh=sys.stdout
        self.verbose=False
        self.pathPdbxDataFile     = "tests/data/1kip.cif"
        self.pathOutputFile       = "testOutputDataFile.cif"

    def tearDown(self):
        pass


    def testSimpleInitialization(self):
        """Test case -  Simple initialization of a data category and data block
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            fn="test-simple.cif"
            attribute_name_list=['aOne','aTwo','aThree','aFour','aFive','aSix','aSeven','aEight','aNine','aTen']
            row_list=[[1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10],
                     [1,2,3,4,5,6,7,8,9,10] 
                     ]
            nameCat='category'
            #
            #
            current_container=DataContainer("myblock")
            aCat=DataCategory(nameCat,attribute_name_list,row_list)
            aCat.print_it()
            current_container.append(aCat)
            current_container.print_it()
            #
            myContainerList=[]
            myContainerList.append(current_container)
            ofh = open(fn, "w")        
            pdbxW=PdbxWriter(ofh)
            pdbxW.write(myContainerList)
            ofh.close()

            myContainerList=[]            
            input_file = open(fn, "r")
            pRd=PdbxReader(input_file)
            pRd.read(myContainerList)
            input_file.close()
            for container in myContainerList:
                for objName in container.get_object_name_list():
                    name,aList,rList=container.get_object(objName).get()
                    self.lfh.write("Recovered data category  %s\n" % name)
                    self.lfh.write("Attribute list           %r\n" % repr(aList))
                    self.lfh.write("Row list                 %r\n" % repr(rList))                                        
        except:
            traceback.print_exc(file=self.lfh)
            self.fail()
            
        
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
            aCat.append([1,2,3,4,5,6,7])
            aCat.append([1,2,3,4,5,6,7])
            aCat.append([1,2,3,4,5,6,7])
            aCat.append([1,2,3,4,5,6,7])
            aCat.append([7,6,5,4,3,2,1])
            aCat.print_it()            
            current_container.append(aCat)
            current_container.print_it()
            #
            myDataList.append(current_container)
            pdbxW=PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()
        except:
            traceback.print_exc(file=self.lfh)
            self.fail()

    def testUpdateDataFile(self): 
        """Test case -  update data file 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            # Create a initial data file --
            #
            myDataList=[]

            current_container=DataContainer("myblock")
            aCat=DataCategory("pdbx_seqtool_mapping_ref")
            aCat.append_attribute("ordinal")
            aCat.append_attribute("entity_id")
            aCat.append_attribute("auth_mon_id")
            aCat.append_attribute("auth_mon_num")
            aCat.append_attribute("pdb_chain_id")
            aCat.append_attribute("ref_mon_id")
            aCat.append_attribute("ref_mon_num")                        
            aCat.append([9,2,3,4,5,6,7])
            aCat.append([10,2,3,4,5,6,7])
            aCat.append([11,2,3,4,5,6,7])
            aCat.append([12,2,3,4,5,6,7])
            
            #self.lfh.write("Assigned data category state-----------------\n")            
            #aCat.dump_it(fh=self.lfh)

            current_container.append(aCat)
            myDataList.append(current_container)
            ofh = open("test-output-1.cif", "w")            
            pdbxW=PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()
            #
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
            #
            
        except:
            traceback.print_exc(file=self.lfh)
            self.fail()

    def testReadDataFile(self): 
        """Test case -  read data file 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myDataList=[]
            input_file = open(self.pathPdbxDataFile, "r")
            pRd=PdbxReader(input_file)
            pRd.read(myDataList)
            input_file.close()            
        except:
            traceback.print_exc(file=self.lfh)
            self.fail()

    def testReadWriteDataFile(self): 
        """Test case -  data file read write test
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            myDataList=[]            
            input_file = open(self.pathPdbxDataFile, "r")
            pRd=PdbxReader(input_file)
            pRd.read(myDataList)
            input_file.close()            
            
            ofh = open(self.pathOutputFile, "w")
            pWr=PdbxWriter(ofh)
            pWr.write(myDataList)        
            ofh.close()
        except:
            traceback.print_exc(file=self.lfh)
            self.fail()


def simpleSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReadWriteTests("testSimpleInitialization"))
    suiteSelect.addTest(PdbxReadWriteTests("testUpdateDataFile"))        
    suiteSelect.addTest(PdbxReadWriteTests("testReadWriteDataFile"))    
    return suiteSelect


if __name__ == '__main__':
    #
    mySuite=simpleSuite()      
    unittest.TextTestRunner(verbosity=2).run(mySuite)
    #


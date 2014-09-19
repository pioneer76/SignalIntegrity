import unittest

import SignalIntegrity as si
from numpy import linalg
from numpy import array
from numpy import matrix
import copy
import math
import os

class TestVirtualProbe(unittest.TestCase):
    def testVirtualProbeOneMeasOneOut(self):
        D=si.sd.SystemDescription()
        D.AddDevice('T',1,si.dev.SeriesZ(50))
        D.AddDevice('C',2,si.dev.SeriesZ(100))
        D.AddDevice('R',1,si.dev.SeriesZ(25))
        D.ConnectDevicePort('T',1,'C',1)
        D.ConnectDevicePort('C',2,'R',1)
        D.AssignM('T',1,'m1')
        #D.Print()
        vp = si.sd.VirtualProbeNumeric(D)
        vp.pMeasurementList = [('T',1)]
        vp.pOutputList = [('R',1)]
        H=vp.TransferFunctions()
        #print "H", H
        SC=D[D.DeviceNames().index('C')].pSParameters
        SC21=SC[2-1][1-1]
        SC11=SC[1-1][1-1]
        SC22=SC[2-1][2-1]
        GR=D[D.DeviceNames().index('R')].pSParameters[0][0]
        SCD=linalg.det(matrix(SC))
        # this is what I say the answer should be
        H2=(SC21*(1+GR))/(1+SC11-GR*(SC22+SCD))
        #print "H2", H2
        difference = linalg.norm(H-H2)
        self.assertTrue(difference<1e-10,'Simple Virtual Probe incorrect')
    def testVirtualProbeTwoMeasTwoOut(self):
        #First, make a structure with two series resistors with a shunt across them at the end
        #We will use this for all configurations, except the ends will be grounded for the terminations
        D1=si.sd.SystemDescription()
        D1.AddDevice('Zs1',2)
        D1.AddDevice('Zs2',2)
        D1.AddDevice('Zh',2)
        D1.ConnectDevicePort('Zs1',1,'Zh',1)
        D1.ConnectDevicePort('Zs2',1,'Zh',2)
        D1.AddPort('Zs1',1,1)
        D1.AddPort('Zs2',1,2)
        D2=copy.deepcopy(D1)
        D1.AddPort('Zs1',2,3)
        D1.AddPort('Zs2',2,4)
        D2.AddDevice('G',1,si.dev.Ground())
        D2.ConnectDevicePort('Zs1',2,'G',1)
        D2.ConnectDevicePort('Zs2',2,'G',1)
        #print 'D1\n'
        #D1.Print()
        #print 'D2\n'
        #D2.Print()
        D1.AssignSParameters('Zs1',si.dev.SeriesZ(25))
        D1.AssignSParameters('Zs2',si.dev.SeriesZ(35))
        D1.AssignSParameters('Zh',si.dev.SeriesZ(20))
        C=si.sd.SystemSParametersNumeric(D1).SParameters()
        D2.AssignSParameters('Zs1',si.dev.SeriesZ(38))
        D2.AssignSParameters('Zs2',si.dev.SeriesZ(82))
        D2.AssignSParameters('Zh',si.dev.SeriesZ(24))
        T=si.sd.SystemSParametersNumeric(D2).SParameters()
        D2.AssignSParameters('Zs1',si.dev.SeriesZ(26))
        D2.AssignSParameters('Zs2',si.dev.SeriesZ(45))
        D2.AssignSParameters('Zh',si.dev.SeriesZ(20))
        R=si.sd.SystemSParametersNumeric(D2).SParameters()
        D=si.sd.SystemDescription()
        D.AddDevice('T',2,T)
        D.AddDevice('C',4,C)
        D.AddDevice('R',2,R)
        D.ConnectDevicePort('T',1,'C',1)
        D.ConnectDevicePort('T',2,'C',2)
        D.ConnectDevicePort('C',3,'R',1)
        D.ConnectDevicePort('C',4,'R',2)
        D.AssignM('T',1,'m1')
        D.AssignM('T',2,'m2')
        #D.Print()
        vp=si.sd.VirtualProbeNumeric(D)
        vp.pMeasurementList = [('T',1),('T',2)]
        vp.pOutputList = [('R',1),('R',2)]
        H=vp.TransferFunctions()
        #print "H", H
        #This result was the result of a prior run - it's a regression test
        H2=[[0.3858829,0.13673016],[0.19142223,0.35129134]]
        difference = linalg.norm(H-H2)
        #print difference
        self.assertTrue(difference<1e-8,'Virtual Probe Two Input, Two Output incorrect')
    def testVirtualProbeOneMeasTwoOut(self):
        #First, make a structure with two series resistors with a shunt across them at the end
        #We will use this for all configurations, except the ends will be grounded for the terminations
        D1=si.sd.SystemDescription()
        D1.AddDevice('Zs1',2)
        D1.AddDevice('Zs2',2)
        D1.AddDevice('Zh',2)
        D1.ConnectDevicePort('Zs1',1,'Zh',1)
        D1.ConnectDevicePort('Zs2',1,'Zh',2)
        D1.AddPort('Zs1',1,1)
        D1.AddPort('Zs2',1,2)
        D2=copy.deepcopy(D1)
        D1.AddPort('Zs1',2,3)
        D1.AddPort('Zs2',2,4)
        D2.AddDevice('G',1,si.dev.Ground())
        D2.ConnectDevicePort('Zs1',2,'G',1)
        D2.ConnectDevicePort('Zs2',2,'G',1)
        #print 'D1\n'
        #D1.Print()
        #print 'D2\n'
        #D2.Print()
        D1.AssignSParameters('Zs1',si.dev.SeriesZ(25))
        D1.AssignSParameters('Zs2',si.dev.SeriesZ(35))
        D1.AssignSParameters('Zh',si.dev.SeriesZ(20))
        C=si.sd.SystemSParametersNumeric(D1).SParameters()
        D2.AssignSParameters('Zs1',si.dev.SeriesZ(38))
        D2.AssignSParameters('Zs2',si.dev.SeriesZ(82))
        D2.AssignSParameters('Zh',si.dev.SeriesZ(24))
        T=si.sd.SystemSParametersNumeric(D2).SParameters()
        D2.AssignSParameters('Zs1',si.dev.SeriesZ(26))
        D2.AssignSParameters('Zs2',si.dev.SeriesZ(45))
        D2.AssignSParameters('Zh',si.dev.SeriesZ(20))
        R=si.sd.SystemSParametersNumeric(D2).SParameters()
        D=si.sd.SystemDescription()
        D.AddDevice('T',2,T)
        D.AddDevice('MM1',4,si.dev.MixedModeConverter())
        D.AddDevice('MM2',4,si.dev.MixedModeConverter())
        D.AddDevice('C',4,C)
        D.AddDevice('R',2,R)
        D.ConnectDevicePort('T',1,'MM1',1)
        D.ConnectDevicePort('T',2,'MM1',2)
        D.ConnectDevicePort('MM1',3,'MM2',3)
        D.ConnectDevicePort('MM1',4,'MM2',4)
        D.ConnectDevicePort('MM2',1,'C',1)
        D.ConnectDevicePort('MM2',2,'C',2)
        D.ConnectDevicePort('C',3,'R',1)
        D.ConnectDevicePort('C',4,'R',2)
        D.AssignM('T',1,'m1')
        D.AssignM('T',2,'m2')
        #D.Print()
        vp = si.sd.VirtualProbeNumeric(D)
        vp.pMeasurementList = [('MM1',3)]
        vp.pOutputList = [('R',1),('R',2)]
        vp.pStimDef = array([[1],[-1]])
        H=vp.TransferFunctions()
        #print "H", H
        #This result was the result of a prior run - it's a regression test
        H2=[[0.20965471848736478],[-0.07827982596732863]]
        difference = linalg.norm(H-H2)
        #print difference
        self.assertTrue(difference<1e-8,'Virtual Probe Two Input, Two Output incorrect')
    def testBookVirtualProbe1(self):
        D=si.sd.SystemDescription()
        D.AddDevice('T',1)
        D.AddDevice('C',2)
        D.AddDevice('R',1)
        D.ConnectDevicePort('T',1,'C',1)
        D.ConnectDevicePort('C',2,'R',1)
        D.AssignM('T',1,'m1')
        D=si.sd.VirtualProbe(D)
        D.m_ml=[('T',1)]
        D.m_ol=[('R',1)]
        W = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(D).WeightsMatrix())
        nv = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(D).NodeVector())
        sv = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(D).StimulusVector())
        line1 = '\\left[ \\identity - ' + W + '\\right]' + nv + '^T' + ' = ' + sv + '^T'
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        fileName1='_'.join(self.id().split('.'))+'_1.txt'
        if not os.path.exists(fileName1):
            resultFile1=open(fileName1,'w')
            resultFile1.write(line1)
            resultFile1.close()
            self.assertTrue(False,fileName1+ ' not found')
        regressionFile1=open(fileName1,'r')
        regressionLine1 = regressionFile1.read()
        regressionFile1.close()
        sipr =  si.helper.Matrix2LaTeX(D.SIPrime(True))
        vem = si.helper.Matrix2LaTeX(D.VoltageExtractionMatrix(D.m_ml))
        veo = si.helper.Matrix2LaTeX(D.VoltageExtractionMatrix(D.m_ol))
        line2 = '\\left[ '+veo+' \\cdot '+sipr+' \\right]' + '\\left[ '+vem+' \\cdot '+sipr+' \\right]^{-1}'
        self.assertTrue(regressionLine1==line1,'Virtual Probe Example 1 line 1 in book incorrect')
        fileName2='_'.join(self.id().split('.'))+'_2.txt'
        if not os.path.exists(fileName2):
            resultFile2=open(fileName2,'w')
            resultFile2.write(line2)
            resultFile2.close()
            self.assertTrue(False,fileName2+ ' not found')
        regressionFile2=open(fileName2,'r')
        regressionLine2 = regressionFile2.read()
        regressionFile2.close()
        self.assertTrue(regressionLine2==line2,'Virtual Probe Example 1 line 2 in book incorrect')
    def testBookVirtualProbe2(self):
        D=si.sd.SystemDescription()
        D.AddDevice('T',2)
        D.AddDevice('C',4)
        D.AddDevice('R',2)
        D.ConnectDevicePort('T',1,'C',1)
        D.ConnectDevicePort('T',2,'C',2)
        D.ConnectDevicePort('C',3,'R',1)
        D.ConnectDevicePort('C',4,'R',2)
        D.AssignM('T',1,'m1')
        D.AssignM('T',2,'m2')
        D=si.sd.VirtualProbe(D)
        D.m_ml=[('T',1),('T',2)]
        D.m_ol=[('R',1),('R',2)]
        W = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(D).WeightsMatrix())
        nv = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(D).NodeVector())
        sv = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(D).StimulusVector())
        line1 = '\\left[ \\identity - ' + W + '\\right]' + nv + '^T' + ' = ' + sv + '^T'
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        fileName1='_'.join(self.id().split('.'))+'_1.txt'
        if not os.path.exists(fileName1):
            resultFile1=open(fileName1,'w')
            resultFile1.write(line1)
            resultFile1.close()
            self.assertTrue(False,fileName1+ ' not found')
        regressionFile1=open(fileName1,'r')
        regressionLine1 = regressionFile1.read()
        regressionFile1.close()
        sipr =  si.helper.Matrix2LaTeX(D.SIPrime(True))
        vem = si.helper.Matrix2LaTeX(D.VoltageExtractionMatrix(D.m_ml))
        veo = si.helper.Matrix2LaTeX(D.VoltageExtractionMatrix(D.m_ol))
        line2 = '\\left[ '+veo+' \\cdot '+sipr+' \\right]' + '\\left[ '+vem+' \\cdot '+sipr+' \\right]^{-1}'
        self.assertTrue(regressionLine1==line1,'Virtual Probe Example 2 line 1 in book incorrect')
        fileName2='_'.join(self.id().split('.'))+'_2.txt'
        if not os.path.exists(fileName2):
            resultFile2=open(fileName2,'w')
            resultFile2.write(line2)
            resultFile2.close()
            self.assertTrue(False,fileName2+ ' not found')
        regressionFile2=open(fileName2,'r')
        regressionLine2 = regressionFile2.read()
        regressionFile2.close()
        self.assertTrue(regressionLine2==line2,'Virtual Probe Example 2 line 2 in book incorrect')
    def testBookVirtualProbe3(self):
        SD=si.sd.SystemDescription()
        SD.AddDevice('T',2)
        SD.AddDevice('C',4)
        SD.AddDevice('R',2)
        SD.ConnectDevicePort('T',1,'C',1)
        SD.ConnectDevicePort('T',2,'C',2)
        SD.ConnectDevicePort('C',3,'R',1)
        SD.ConnectDevicePort('C',4,'R',2)
        SD.AssignM('T',1,'m1')
        SD.AssignM('T',2,'m2')
        SD=si.sd.VirtualProbe(SD)
        SD.m_ml=[('T',1),('T',2)]
        SD.m_ol=[('R',1),('R',2)]
        SD.m_D=[[1],[-1]]
        W = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(SD).WeightsMatrix())
        nv = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(SD).NodeVector())
        sv = si.helper.Matrix2LaTeX(si.sd.SystemSParameters(SD).StimulusVector())
        line1 = '\\left[ \\identity - ' + W + '\\right]' + nv + '^T' + ' = ' + sv + '^T'
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        fileName1='_'.join(self.id().split('.'))+'_1.txt'
        if not os.path.exists(fileName1):
            resultFile1=open(fileName1,'w')
            resultFile1.write(line1)
            resultFile1.close()
            self.assertTrue(False,fileName1+ ' not found')
        regressionFile1=open(fileName1,'r')
        regressionLine1 = regressionFile1.read()
        regressionFile1.close()
        sipr =  si.helper.Matrix2LaTeX(SD.SIPrime(True))
        vem = si.helper.Matrix2LaTeX(SD.VoltageExtractionMatrix(SD.m_ml))
        veo = si.helper.Matrix2LaTeX(SD.VoltageExtractionMatrix(SD.m_ol))
        D = si.helper.Matrix2LaTeX(SD.m_D)
        vd = si.helper.Matrix2LaTeX([[1,-1]])
        line2 = '\\left[ '+veo+' \\cdot '+sipr+' \\cdot '+ D + '\\right]' + '\\left[ '+vd+' \\cdot '+vem+' \\cdot '+sipr+' \\cdot '+ D + ' \\right]^{-1}'
        self.assertTrue(regressionLine1==line1,'Virtual Probe Example 3 line 1 in book incorrect')
        fileName2='_'.join(self.id().split('.'))+'_2.txt'
        if not os.path.exists(fileName2):
            resultFile2=open(fileName2,'w')
            resultFile2.write(line2)
            resultFile2.close()
            self.assertTrue(False,fileName2+ ' not found')
        regressionFile2=open(fileName2,'r')
        regressionLine2 = regressionFile2.read()
        regressionFile2.close()
        self.assertTrue(regressionLine2==line2,'Virtual Probe Example 3 line 2 in book incorrect')
if __name__ == '__main__':
    unittest.main()
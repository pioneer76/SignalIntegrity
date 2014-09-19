import unittest
import SignalIntegrity as si
import math
import os

class TestSParameterFile(unittest.TestCase):
    def testIt(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.spf.File('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC(self):
        L1=1e-15
        C1=1e-9
        L2=1e-15
        freq=[100e6*(i+1) for i in range(100)]
        spc=[]
        spc.append(('L1',[si.dev.SeriesZ(1j*2.*math.pi*f*L1) for f in freq]))
        spc.append(('C1',[si.dev.SeriesZ(1./(1j*2.*math.pi*C1*f)) for f in freq]))
        spc.append(('L2',[si.dev.SeriesZ(1j*2.*math.pi*f*L2) for f in freq]))
        SD=si.sd.SystemDescription()
        SD.AddDevice('L1',2)
        SD.AddDevice('L2',2)
        SD.AddDevice('C1',2)
        SD.AddDevice('G',1,si.dev.Ground())
        SD.AddPort('L1',1,1)
        SD.AddPort('L2',2,2)
        SD.ConnectDevicePort('L1',2,'L2',1)
        SD.ConnectDevicePort('L1',2,'C1',1)
        SD.ConnectDevicePort('C1',2,'G',1)
        result=[]
        for n in range(len(freq)):
            for d in range(len(spc)):
                SD[SD.IndexOfDevice(spc[d][0])].pSParameters=spc[d][1][n]
            result.append(si.sd.SystemSParametersNumeric(SD).SParameters())
        sf=si.spf.SParameters(freq,result)
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC2(self):
        L1=1e-15
        C1=1e-9
        L2=1e-15
        freq=[100e6*(i+1) for i in range(100)]
        spc=[]
        spc.append(('L1',si.p.dev.SeriesLf(freq,L1)))
        spc.append(('C1',si.p.dev.SeriesCf(freq,C1)))
        spc.append(('L2',si.p.dev.SeriesLf(freq,L2)))
        SD=si.sd.SystemDescription()
        SD.AddDevice('L1',2)
        SD.AddDevice('L2',2)
        SD.AddDevice('C1',2)
        SD.AddDevice('G',1,si.dev.Ground())
        SD.AddPort('L1',1,1)
        SD.AddPort('L2',2,2)
        SD.ConnectDevicePort('L1',2,'L2',1)
        SD.ConnectDevicePort('L1',2,'C1',1)
        SD.ConnectDevicePort('C1',2,'G',1)
        result=[]
        for n in range(len(freq)):
            for d in range(len(spc)):
                SD[SD.IndexOfDevice(spc[d][0])].pSParameters=spc[d][1][n]
            result.append(si.sd.SystemSParametersNumeric(SD).SParameters())
        sf=si.spf.SParameters(freq,result)
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRes(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        newf=[100e6*n for n in range(100)]
        sf=si.spf.File('TestDut.s4p').Resample([1e9*n for n in range(10)])
        sf2=si.spf.File('TestDut.s4p').Resample([1e9*n for n in range(10)]).Resample(newf)
        if not os.path.exists('Test1.s4p'):
            sf.WriteToFile('Test1.s4p')
            self.assertTrue(False,'Test1.s4p' + ' does not exist')
        if not os.path.exists('Test2.s4p'):
            sf2.WriteToFile('Test2.s4p')
            self.assertTrue(False,'Test2.s4p' + ' does not exist')
        regression = si.spf.File('Test1.s4p')
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'first result not same')
        regression = si.spf.File('Test2.s4p')
        self.assertTrue(sf2.AreEqual(regression,0.001),self.id()+'second result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        f2=sf2.f()
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                responseVector2=sf2.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                y2=[20*math.log(abs(resp),10) for resp in responseVector2]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
                plt.plot(f2,y2)
        plt.show()
        """
    def testRLC3(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        L1=1e-15
        C1=1e-9
        L2=1e-15
        freq=[100e6*(i+1) for i in range(100)]
        spc=[]
        spc.append(('L1',si.p.dev.SeriesLf(freq,L1)))
        spc.append(('C1',si.p.dev.SeriesCf(freq,C1)))
        spc.append(('L2',si.p.dev.SeriesLf(freq,L2)))
        spc.append(('D1',si.spf.File('TestDut.s4p').Resample(freq)))
        SD=si.sd.SystemDescription()
        SD.AddDevice('D1',4)
        SD.AddDevice('L1',2)
        SD.AddDevice('L2',2)
        SD.AddDevice('C1',2)
        SD.AddDevice('G',1,si.dev.Ground())
        SD.AddPort('D1',1,1)
        SD.AddPort('D1',2,2)
        SD.AddPort('D1',3,3)
        SD.ConnectDevicePort('L1',2,'L2',1)
        SD.ConnectDevicePort('L1',2,'C1',1)
        SD.ConnectDevicePort('C1',2,'G',1)
        SD.ConnectDevicePort('D1',4,'L1',1)
        SD.AddPort('L2',2,4)
        result=[]
        for n in range(len(freq)):
            for d in range(len(spc)):
                SD[SD.IndexOfDevice(spc[d][0])].pSParameters=spc[d][1][n]
            result.append(si.sd.SystemSParametersNumeric(SD).SParameters())
        sf=si.spf.SParameters(freq,result)
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC4(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(100)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device L1 2 L 1e-15')
        parser.AddLine('device C1 2 C 1e-9')
        parser.AddLine('device L2 2 L 1e-15')
        parser.AddLine('device D1 4 file TestDut.s4p')
        parser.AddLine('device G 1 ground')
        parser.AddLine('port 1 D1 1 2 D1 2 3 D1 3 4 L2 2')
        #parser.AddLine('port 2 D1 2')
        #parser.AddLine('port 3 D1 3')
        parser.AddLine('connect L1 2 L2 1 C1 1')
        parser.AddLine('connect C1 2 G 1')
        parser.AddLine('connect D1 4 L1 1')
        #parser.AddLine('port 4 L2 2')
        sf=si.spf.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        regression = si.spf.File('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC5(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(100)]
        parser=si.p.SystemSParametersNumericParser(freq,'%Lleft 1e-15 %Cshunt 1e-9 %Lright 1e-15')
        parser.AddLine('var %Lleft x %Cshunt x %Lright x')
        parser.AddLine('device L1 2 L %Lleft')
        parser.AddLine('device C1 2 C %Cshunt')
        parser.AddLine('device L2 2 L %Lright')
        parser.AddLine('device D1 4 file TestDut.s4p')
        parser.AddLine('device G 1 ground')
        parser.AddLine('port 1 D1 1 2 D1 2 3 D1 3 4 L2 2')
        #parser.AddLine('port 2 D1 2')
        #parser.AddLine('port 3 D1 3')
        parser.AddLine('connect L1 2 L2 1 C1 1')
        parser.AddLine('connect C1 2 G 1')
        parser.AddLine('connect D1 4 L1 1')
        #parser.AddLine('port 4 L2 2')
        sf=si.spf.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC6(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(100)]
        if not os.path.exists('rlc.txt'):
            parser=si.p.SystemDescriptionParser(freq)
            parser.AddLine('var Ll x Cs x Lr x')
            parser.AddLine('device L1 2 L Ll')
            parser.AddLine('device C1 2 C Cs')
            parser.AddLine('device L2 2 L Lr')
            parser.AddLine('device G 1 ground')
            parser.AddLine('connect L1 2 L2 1 C1 1')
            parser.AddLine('connect C1 2 G 1')
            parser.AddLine('port 1 L1 1')
            parser.AddLine('port 2 L2 2')
            parser.WriteToFile('rlc.txt')
        if not os.path.exists('r.txt'):
            parser=si.p.SystemDescriptionParser(freq)
            parser.AddLine('var Rs 50')
            parser.AddLine('device D1 2 R Rs')
            parser.AddLine('port 1 D1 1 2 D1 2')
            parser.WriteToFile('r.txt')
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device RLC 2 subcircuit rlc.txt Ll 1e-15 Cs 1e-9 Lr 1e-15')
        parser.AddLine('device R1 2 subcircuit r.txt')
        parser.AddLine('device D1 4 file TestDut.s4p')
        parser.AddLine('port 1 D1 1 2 D1 2 3 D1 3 4 RLC 2')
        parser.AddLine('connect D1 4 R1 1')
        parser.AddLine('connect R1 2 RLC 1')
        #parser.AddLine('port 4 L2 2')
        sf=si.spf.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRes2(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(10)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device R1 2 R 0.001')
        parser.AddLine('port 1 R1 1 2 R1 2')
        sf=si.spf.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testS2P(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[0.1e9*i for i in range(400)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('port 1 D1 1 2 D1 2')
        sf=si.spf.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.spf.File(fileName)
        self.assertTrue(sf.AreEqual(regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testAreEqual(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        firstFileRead = si.spf.File('TestDut.s4p')
        secondFileRead = si.spf.File('TestDut.s4p')
        self.assertTrue(firstFileRead.AreEqual(secondFileRead,0.001),'same file read is not equal')
    def testDeembed(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[0.1e9*i for i in range(400)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device D2 2 file cable.s2p')
        parser.AddLine('port 1 D1 1 2 D2 2')
        parser.AddLine('connect D1 2 D2 1')
        system=si.spf.SParameters(freq,parser.SParameters())
        systemSParametersFileName='_'.join(self.id().split('.'))+'.s'+str(system.m_P)+'p'
        if not os.path.exists(systemSParametersFileName):
            system.WriteToFile(systemSParametersFileName)
        del parser
        parser = si.p.DeembedderNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device ? 2')
        parser.AddLine('port 1 D1 1 2 ? 2')
        parser.AddLine('connect D1 2 ? 1')
        parser.AddLine('system file '+systemSParametersFileName)
        de=si.spf.SParameters(freq,parser.Deembed())
        self.assertTrue(de.AreEqual(si.spf.File('cable.s2p').Resample(freq),0.00001),self.id()+'result not same')
    def testDeembed2(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[0.1e9*i for i in range(400)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device D2 2 file cable.s2p')
        parser.AddLine('port 1 D1 1 2 D2 2')
        parser.AddLine('connect D1 2 D2 1')
        system=si.spf.SParameters(freq,parser.SParameters())
        systemSParametersFileName='_'.join(self.id().split('.'))+'.s'+str(system.m_P)+'p'
        if not os.path.exists(systemSParametersFileName):
            system.WriteToFile(systemSParametersFileName)
        del parser
        parser = si.p.DeembedderNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device ? 2')
        parser.AddLine('port 1 D1 1 2 ? 2')
        parser.AddLine('connect D1 2 ? 1')
        parser.AddLine('system file '+systemSParametersFileName)
        de=si.spf.SParameters(freq,parser.Deembed(system))
        self.assertTrue(de.AreEqual(si.spf.File('cable.s2p').Resample(freq),0.00001),self.id()+'result not same')

if __name__ == '__main__':
    unittest.main()
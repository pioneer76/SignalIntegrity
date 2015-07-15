from SignalIntegrity.FrequencyDomain.FrequencyList import FrequencyList


from numpy import zeros

class TransferMatrices(object):
    def __init__(self,f,d):
        self.f=FrequencyList(f)
        self.Matrices=d
        self.Inputs=len(d[0][0])
        self.Outputs=len(d[0])
    def SParameters(self):
        from SignalIntegrity.SParameters.SParameters import SParameters
        if self.Inputs == self.Outputs:
            return SParameters(self.f,self.Matrices)
        else:
            squareMatrices=[]
            P=max(self.Inputs,self.Outputs)
            for transferMatrix in self.Matrices:
                squareMatrix=zeros((P,P),complex).tolist()
                for r in range(len(transferMatrix)):
                    for c in range(len(transferMatrix[0])):
                        squareMatrix[r][c]=transferMatrix[r][c]
                squareMatrices.append(squareMatrix)
            return SParameters(self.f,squareMatrices)
    def __len__(self):
        return len(self.f)
    def __getitem__(self,item):
        return self.Matrices[item]
    def FrequencyResponse(self,o,i):
        from SignalIntegrity.FrequencyDomain.FrequencyResponse import FrequencyResponse
        return FrequencyResponse(self.f,[Matrix[o-1][i-1] for Matrix in self.Matrices])
    def FrequencyResponses(self):
        return [[self.FrequencyResponse(o+1,s+1)
            for s in range(self.Inputs)] for o in range(self.Outputs)]
    def ImpulseResponses(self,td=None):
        fr = self.FrequencyResponses()
        if td is None or isinstance(td,float) or isinstance(td,int):
            td = [td for m in range(len(fr[0]))]
        return [[fro[m].ImpulseResponse(td[m]) for m in range(len(fro))]
            for fro in fr]
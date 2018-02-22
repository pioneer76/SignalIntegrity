class Waveform(list):
    def __mul__(self,other):
        if isinstance(other,FirFilter):
            return other.FilterWaveform(self)
        elif isinstance(other,WaveformTrimmer):
            return other.TrimWaveform(self)
        elif isinstance(other,WaveformDecimator):
            return other.DecimateWaveform(self)
        elif isinstance(other,(float,int,complex)):
            return Waveform(self.td,[v*other.real for v in self])
...

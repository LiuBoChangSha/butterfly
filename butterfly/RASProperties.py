"BlockMeshDict class."
from foamfile import FoamFile
from collections import OrderedDict


class RASProperties(FoamFile):
    """Finite Volume Solution class."""

    # set default valus for this class
    __defaultValues = OrderedDict()
    __defaultValues['RASModel'] = 'kEpsilon'
    __defaultValues['turbulence'] = 'on'
    __defaultValues['printCoeffs'] = 'on'

    def __init__(self, values=None):
        """Init class."""
        FoamFile.__init__(self, name='RASProperties', cls='dictionary',
                          location='constant', defaultValues=self.__defaultValues,
                          values=values)

# fv = RASProperties()
# fv.save(r'C:\Users\Administrator\butterfly\innerflow_3')

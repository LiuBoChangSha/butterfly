# Butterfly: A Plugin for CFD Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Butterfly.
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Create Case from wind tunnel.

-

    Args:
        _name: Project name.
        _BFGeometries: List of butterfly geometries that will be inside the tunnel.
        _windSpeed: Wind speed in m/s at a the reference height (_refWindHeight_).
        _refWindHeight_: Reference height for wind velocity (default: 10m).
        _windDirection_: Wind direction as Vector3D (default: 0, 1, 0).
        _landscape_: An integer between 0-7 to calculate z0 (roughness).
            You can find full description of the landscape in Table I at this
            link (onlinelibrary.wiley.com/doi/10.1002/met.273/pdf)

            0 > '0.0002'  # sea. Open sea or lake (irrespective of wave size),
            tidal flat, snow-covered flat plain, featureless desert, tarmac and
            concrete, with a free fetch of several kilometres

            1 > '0.005'   # smooth. Featureless land surface without any noticeable
            obstacles and with negligible vegetation; e.g. beaches, pack ice without
            large ridges, marsh and snow-covered or fallow open country.

            2 > '0.03'    # open. Level country with low vegetation (e.g. grass)
            and isolated obstacles with separations of at least 50 obstacle heights;
            e.g. grazing land without wind breaks, heather, moor and tundra,
            runway area of airports. Ice with ridges across-wind.

            3 > '0.10'    # roughly open. Cultivated or natural area with low crops
            or plant covers, or moderately open country with occasional obstacles
            (e.g. low hedges, isolated low buildings or trees) at relative horizontal
            distances of at least 20 obstacle heights

            4 > '0.25'    # rough. Cultivated or natural area with high crops or
            crops of varying height, and scattered obstacles at relative distances
            of 1215 obstacle heights for porous objects (e.g. shelterbelts) or
            812 obstacle heights for low solid objects (e.g. buildings).

            5 > '0.5'     # very rough. Intensively cultivated landscape with many
            rather large obstacle groups (large farms, clumps of forest) separated
            by open spaces of about eight obstacle heights. Low densely planted
            major vegetation like bush land, orchards, young forest. Also, area
            moderately covered by low buildings with interspaces of three to
            seven building heights and no high trees.

            6 > '1.0'     # Skimming. Landscape regularly covered with similar-size
            large obstacles, with open spaces of the same order of magnitude as
            obstacle heights; e.g. mature regular forests, densely built-up area
            without much building height variation.

            7 > '2.0'     # chaotic. City centres with mixture of low-rise and
            high-rise buildings, or large forests of irregular height with many
            clearings.

        _globalRefLevel_: A tuple of (min, max) values for global refinment.
        _tunnelPar_: Butterfly tunnel parameters.
        _run: Create wind tunnel case from inputs.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        geo: Wind tunnel geometry for visualization.
        case: Butterfly case.
"""

ghenv.Component.Name = "Butterfly_Create Case from Tunnel"
ghenv.Component.NickName = "createCaseFromTunnel"
ghenv.Component.Message = 'VER 0.0.02\nOCT_02_2016'
ghenv.Component.Category = "Butterfly"
ghenv.Component.SubCategory = "00::Create"
ghenv.Component.AdditionalHelpFromDocStrings = "3"

try:
    import butterfly.gh.windtunnel
except ImportError as e:
    msg = '\nFailed to import butterfly. Did you install butterfly on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/mostaphaRoudsari/Butterfly/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/mostaphaRoudsari/Butterfly/issues'
        
    raise ImportError('{}\n{}'.format(msg, e))

import sys
import types

def main():
    wt = butterfly.gh.windtunnel.GHWindTunnel(_name, _BFGeometries, _windSpeed,
        _windDirection_, _tunnelPar_, _landscape_, _globalRefLevel_, _refWindHeight_)
    
    print "Wind tunnel dimensions: {}, {} and {}".format(wt.X, wt.Y, wt.Z)
    print "Number of divisions: {}, {} and {}".format(*_tunnelPar_.nDivXYZ)
    for region in refRegions_:
        wt.addRefinementRegion(region)
    geo =  wt.boundingbox
    case = wt.toOpenFOAMCase()
    case.createCaseFolders()
    case.populateContents()
    
    
    return geo, case

if _run and _name and _BFGeometries and _windSpeed:
        geo, case = main()

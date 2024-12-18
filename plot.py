#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Generated on Tue Nov 05 14:54:59 2024

Turbine: iea10MW
Model:   GAD
Cases:   1

"""

import math
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from scipy import interpolate
import subprocess                              # for .gif videos
###########################################################################
np.seterr(divide='ignore', invalid='ignore')
###########################################################################
def mean_bias_error(pred,true):
    return np.nanmean(pred-true)
def mean_relative_error(pred,true):
    return 100*(np.nanmean((pred-true)/true))
def mean_absolute_relative_error(pred,true):
    return 100*(np.nanmean(np.abs(pred-true)/true))
def root_mean_square_error(pred,true):
    return math.sqrt(np.nanmean(np.square(np.subtract(pred,true))))
def grid2gif(image_str,output_gif):
    str1 = 'magick -delay 50 -loop 0 ' + image_str  + ' ' + output_gif
    subprocess.call(str1,shell=True)
###########################################################################

# casenames = [r'U04', r'U06', r'U07', r'U08', r'U09', r'U10', r'U106', r'U11', r'U12']
casenames = [r's0_v2']

disk_avg = False
forces   = False
contours = True
profiles = False
itqp     = False
###########################################################################
# load wrf data
print('Loading data...')

wrfles_data = []
for count, name in enumerate(casenames):
    wrfles_data.append(dict(np.load('/anvil/scratch/x-smata/wrf_les_sweep/runs/clockwise/gad_sweep/' + casenames[count]+'.npz')))

###########################################################################
# set figure layout parameters
plt.style.use('/anvil/scratch/x-smata/postprocessing/scripts/figures_layout.mplstyle')
fontsize = 24
mpl.rcParams['xtick.labelsize'] = 20 
mpl.rcParams['ytick.labelsize'] = 20 
###########################################################################
## Plotting turbine-representing circle in y-z plots
# number of points
n = 1000

# radius
r = wrfles_data[0]['diameter']/2

# locations
# c11 = rotor_yloc-0.5*dx;
c11 = wrfles_data[0]['rotor_yloc']
# c12 = z_av(k_loc_new)+0.5*dz(1, k_loc_new);
c12 = wrfles_data[0]['hub_height']

# running variable
t = np.linspace(0, 2*np.pi, n)

x11 = c11 + r*np.sin(t)
y11 = c12 + r*np.cos(t)

# calculation of the horizontal spacing:
Lx = wrfles_data[0]['Nx']*wrfles_data[0]['dx'] # Lx of the computational domain
xx = np.linspace(wrfles_data[0]['dx']/2,Lx-(wrfles_data[0]['dx']/2),wrfles_data[0]['Nx']) # Longitudinal spacing in meters
###########################################################################
# error quantification 
zmin=-1
zmax=1
nondim_r=(wrfles_data[0]['z_av']-wrfles_data[0]['hub_height'])/wrfles_data[0]['diameter'] # wrf
n=25 # required length
tdata=np.linspace(zmin,zmax,n)
###########################################################################
plt.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsfonts}'
})
# colors = [
#     (31/255, 119/255, 180/255), 
#     (255/255, 127/255, 14/255),
#     (44/255, 160/255, 44/255),
#     (214/255, 39/255, 40/255),
#     (148/255, 103/255, 189/255),
#     (140/255, 86/255, 75/255),
#     (227/255, 119/255, 194/255),
#     (127/255, 127/255, 127/255),
#     (188/255, 189/255, 34/255),
#     (23/255, 190/255, 207/255),
#     (255/255, 152/255, 150/255),
#     (197/255, 176/255, 213/255),
#     (219/255, 219/255, 141/255)
# ]

colors = [
    '#ffdead',  # Navajo White (light)
    '#4b0082',  # Indigo (blue shade)
    '#ff0000',  # Red
    '#008000',  # Green
    '#ff69b4',  # Hot Pink
    '#0000ff',  # Blue
    '#ffd700',  # Gold
    '#6495ed',  # Cornflower Blue
    '#8b4513',  # Saddle Brown
    '#00ff00',  # Lime
    '#2f4f4f',  # Dark Slate Gray
    '#ff00ff',  # Magenta
    '#00ffff'   # Cyan
]

force_colors = ['#440154',
                '#3b528b',
                '#21918c',
                '#5ec962',
                '#fde725']

T06ws = np.array([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99])
T06F  = np.array([6.5355, -0.8609, -9.1350, -12.5995, -10.5876, 7.5030, 29.9606, 57.2243, 83.3288, 107.1296, 151.2716, 176.5041, 193.5240, 208.3316, 222.6920, 229.6005, 238.0783, 245.6420, 253.5425, 261.1921, 267.3927, 278.1468, 275.9846, 278.4538, 279.2069, 279.6457, 279.6143, 279.2133, 278.7763, 278.7759, 278.3369, 277.9062, 277.0424, 277.0377, 277.0364, 276.6019, 276.1669, 276.1666, 275.2814, 275.2964, 274.4261, 273.9833, 273.5573, 273.1017, 272.6887, 271.8181, 271.3740, 270.9480, 270.3511, 270.0780, 269.2081, 269.2098, 268.3357, 268.3348, 267.4689, 267.3852, 266.5991, 266.5946, 265.9283, 265.7293, 265.7283, 265.2648, 264.8594, 264.8595, 264.8595, 264.8554, 264.4246, 264.4246, 264.4246, 264.4246, 263.9898, 263.9898, 263.1245, 262.6880, 261.7126, 260.5114, 259.6378, 257.8938, 257.0499, 255.2757, 254.4239, 253.5507, 252.6826, 252.6826, 252.2472, 251.8129, 251.2031, 250.0742, 248.3418, 245.7217, 242.0516, 237.6733, 231.3812, 223.8541, 213.9438, 200.9425, 182.4930, 160.9912, 108.2709, 25.7000])

N06ws = np.array([0.050,0.060,0.070,0.080,0.090,0.100,0.110,0.120,0.130,0.140,0.150,0.160,0.170,0.180,0.190,0.200,0.210,0.220,0.230,0.240,0.250,0.260,0.270,0.280,0.290,0.300,0.310,0.320,0.330,0.340,0.350,0.360,0.370,0.380,0.390,0.400,0.410,0.420,0.430,0.440,0.450,0.460,0.470,0.480,0.490,0.500,0.510,0.520,0.530,0.540,0.550,0.560,0.570,0.580,0.590,0.600,0.610,0.620,0.630,0.640,0.650,0.660,0.670,0.680,0.690,0.700,0.710,0.720,0.730,0.740,0.750,0.760,0.770,0.780,0.790,0.800,0.810,0.820,0.830,0.840,0.850,0.860,0.870,0.880,0.890,0.900,0.910,0.920,0.930,0.940,0.950,0.960,0.970,0.980,0.990])
N06F  = np.array([14.23084,45.19727,90.69679,148.54529,217.43773,305.59961,389.44057,472.01494,554.56360,629.53341,702.00398,765.94804,828.64239,886.18513,943.91478,999.81383,1057.12006,1108.25846,1173.70301,1216.39464,1260.79930,1309.12066,1357.12975,1403.83055,1450.28330,1498.64641,1545.94379,1593.29806,1646.17665,1687.87266,1735.34750,1784.29620,1830.65124,1877.13641,1925.64375,1971.52528,2018.67792,2065.07565,2112.92405,2160.79035,2206.06972,2256.43969,2302.83747,2350.49512,2397.99223,2446.09644,2495.87992,2544.79837,2592.94088,2644.50680,2696.29618,2742.75768,2795.85960,2847.15760,2926.90702,2947.35640,2997.95714,3050.44437,3113.55480,3153.34650,3205.63222,3256.78698,3310.71147,3365.13890,3422.94403,3481.30208,3537.75559,3602.62535,3670.30386,3737.21495,3804.86181,3870.79850,3934.46175,3993.98910,4056.63133,4113.39398,4158.68979,4197.99652,4225.68964,4245.67747,4254.74348,4255.46922,4250.44638,4235.69514,4215.95401,4178.55412,4162.09996,4074.00199,4005.81274,3912.20075,3791.86748,3636.59044,3390.99215,2334.99593,999.83437])

T07ws = np.array([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5,  0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,  0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84,  0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99])
T07F  = np.array([5.5858610120308185, -1.748292049, -11.85283502, -16.95534241, -13.38688696, 3.304797409470666, 6.668690930895536, 29.55476023926576, 74.55016999393717, 122.55251917940893, 187.4170929922351, 240.47611303739905, 278.4844112191894, 309.05832120738967, 329.8988980704064, 349.6207326799548, 369.3559149567975, 387.32784885713306, 400.5325536528935, 411.8471428203992, 421.88830540964807, 430.8810471366238, 436.89495342136934, 442.24716427640476, 444.3104131118454, 446.1589668970106, 446.64303772950177, 447.0779618643521, 447.51282365092163, 447.51282520089967, 447.51282520089967, 447.51282520089967, 447.51282520044094, 447.3252186624163, 447.07793636534893, 447.0779363683655, 446.6265957587078, 446.64304753446436, 446.64313227371326, 446.2081563985338, 445.77326467156206, 445.3377353236456, 444.9035099613509, 444.46892053376155, 444.0333932, 443.1677891, 442.72032923763925, 442.29420648342386, 441.42620718225055, 440.99406726970494, 440.5545885852953, 440.13262532030546, 439.6826581687401, 438.8149007774741, 437.94971729863505, 437.5085670726029, 437.0741658, 436.2057232, 435.3299479672496, 435.2265551638833, 434.4661098019993, 434.34323972363256, 433.5836814252149, 433.59638254057506, 433.1466634801112, 433.16149370463813, 433.1614937, 433.1614937, 433.16149370460573, 433.15081973369354, 433.2745998436891, 433.16149370438404, 433.1575279966039, 432.7266048703648, 432.27578794182784, 431.8568312149863, 430.9881494301404, 429.8770992033586, 428.3634507547938, 427.25792569994394, 425.7736076851962, 424.03176488426436, 422.28147881700363, 420.5458814416453, 418.2545334659736, 415.32642754010067, 411.94525085594125, 407.31531730322433, 402.1197304540501, 396.05591471487753, 387.9778297814554, 378.9204266, 367.94029882973575, 354.9717670628861, 338.3042660238367, 317.0193689480499, 288.50976416643164, 254.57423700218044, 150.71585646156802, 34.78188640911981])

N07ws = np.array([0.030,0.040,0.050,0.060,0.070,0.080,0.090,0.100,0.110,0.120,0.130,0.140,0.150,0.160,0.170,0.180,0.190,0.200,0.210,0.220,0.230,0.240,0.250,0.260,0.270,0.280,0.290,0.300,0.310,0.320,0.330,0.340,0.350,0.360,0.370,0.380,0.390,0.400,0.410,0.420,0.430,0.440,0.450,0.460,0.470,0.480,0.490,0.500,0.510,0.520,0.530,0.540,0.550,0.560,0.570,0.580,0.590,0.600,0.610,0.620,0.630,0.640,0.650,0.660,0.670,0.680,0.690,0.700,0.710,0.720,0.730,0.740,0.750,0.760,0.770,0.780,0.790,0.800,0.810,0.820,0.830,0.840,0.850,0.860,0.870,0.880,0.890,0.900,0.910,0.920,0.930,0.940,0.950,0.960,0.970,0.980,0.990])
N07F  = np.array([0.00011,4.97331,30.63566,66.09665,116.40001,177.60826,258.64908,366.22780,476.55393,587.44121,694.99316,783.98504,886.92552,991.54416,1100.40849,1189.76027,1274.20842,1355.39507,1435.66851,1513.61966,1588.00916,1659.62015,1728.50966,1796.31278,1865.62985,1928.98078,1994.41526,2058.97666,2123.94976,2188.50911,2252.51868,2315.20165,2380.34286,2444.91828,2507.85558,2572.70208,2637.50367,2701.41705,2764.14537,2828.82995,2891.09693,2953.37381,3016.34149,3076.55036,3136.63676,3198.75681,3260.33904,3320.21337,3379.60723,3442.74214,3506.69435,3569.54100,3634.15732,3696.27645,3758.61579,3823.99249,3888.45899,3952.21499,4016.06040,4078.51626,4143.62699,4204.92587,4268.01988,4330.15104,4390.22545,4450.63241,4511.55311,4576.87496,4640.65879,4711.45646,4784.01347,4857.72761,4933.66435,5007.08899,5082.38500,5152.89372,5219.51047,5285.00482,5334.68358,5378.60686,5398.71228,5413.78779,5418.76383,5408.41728,5397.68912,5368.87001,5334.89756,5283.09315,5225.61441,5142.95634,5051.84863,4938.10475,4792.42988,4597.89693,4305.93639,2959.70278,1259.91598])

T08ws = np.array([0.000,0.010,0.020,0.030,0.040,0.050,0.060,0.070,0.080,0.090,0.100,0.110,0.120,0.130,0.140,0.150,0.160,0.170,0.180,0.190,0.200,0.210,0.220,0.230,0.240,0.250,0.260,0.270,0.280,0.290,0.300,0.310,0.320,0.330,0.340,0.350,0.360,0.370,0.380,0.390,0.400,0.410,0.420,0.430,0.440,0.450,0.460,0.470,0.480,0.490,0.500,0.510,0.520,0.530,0.540,0.550,0.560,0.570,0.580,0.590,0.600,0.610,0.620,0.630,0.640,0.650,0.660,0.670,0.680,0.690,0.700,0.710,0.720,0.730,0.740,0.750,0.760,0.770,0.780,0.790,0.800,0.810,0.820,0.830,0.840,0.850,0.860,0.870,0.880,0.890,0.900,0.910,0.920,0.930,0.940,0.950,0.960,0.970,0.980,0.990])
T08F  = np.array([4.0392,-3.4923,-16.9194,-23.9066,-18.9069,3.9249,4.6696,35.6207,92.7253,156.6728,240.5629,313.1787,362.9595,402.9768,430.5275,456.5637,482.6067,506.0042,524.0411,538.7668,551.9215,563.2761,571.9592,578.7399,581.4938,584.0188,584.7756,585.3724,585.8086,585.8075,585.8075,585.8075,585.8075,585.8051,585.3726,585.3726,584.9365,584.9377,584.5070,584.0676,583.7018,583.1981,582.7587,581.8814,581.4598,580.5887,579.7214,578.8333,578.4284,577.5285,577.1066,576.2398,575.3672,574.4833,573.6350,572.8509,571.8898,571.0989,570.5788,569.7825,569.2816,568.7239,568.4104,567.9767,567.5421,567.5421,567.1099,567.5421,567.5421,567.5421,567.5421,567.5421,567.1076,566.6716,566.3246,565.8024,564.3836,563.1960,561.4496,559.7135,557.9649,555.5177,553.6569,550.9908,547.8259,543.7505,539.1336,533.2544,526.2613,517.9480,507.7857,495.8264,481.0132,463.6660,442.6607,414.6243,377.5722,333.1116,194.7676,45.8483])

N08ws = np.array([0.030,0.040,0.050,0.060,0.070,0.080,0.090,0.100,0.110,0.120,0.130,0.140,0.150,0.160,0.170,0.180,0.190,0.200,0.210,0.220,0.230,0.240,0.250,0.260,0.270,0.280,0.290,0.300,0.310,0.320,0.330,0.340,0.350,0.360,0.370,0.380,0.390,0.400,0.410,0.420,0.430,0.440,0.450,0.460,0.470,0.480,0.490,0.500,0.510,0.520,0.530,0.540,0.550,0.560,0.570,0.580,0.590,0.600,0.610,0.620,0.630,0.640,0.650,0.660,0.670,0.680,0.690,0.700,0.710,0.720,0.730,0.740,0.750,0.760,0.770,0.780,0.790,0.800,0.810,0.820,0.830,0.840,0.850,0.860,0.870,0.880,0.890,0.900,0.910,0.920,0.930,0.940,0.950,0.960,0.970,0.980,0.990])
N08F  = np.array([9.82908,21.81716,58.90327,106.64254,170.32659,245.41295,347.43095,487.52617,630.96169,772.10931,919.10627,1031.79765,1149.96544,1293.07829,1433.33837,1548.82137,1660.88202,1766.17993,1871.01076,1971.36888,2067.37625,2161.24262,2252.56071,2342.73241,2431.18423,2514.59516,2600.64131,2683.81465,2769.20626,2851.75356,2934.43708,3019.77166,3101.92097,3185.39580,3268.96866,3351.06881,3438.34330,3518.64490,3602.62734,3685.39865,3765.98911,3847.92049,3929.01029,4008.07990,4088.62481,4167.66624,4246.26274,4325.27715,4402.92624,4486.99823,4568.92062,4651.88360,4732.13909,4816.57238,4898.79486,4982.86103,5063.81608,5149.22246,5231.66039,5313.99106,5396.50659,5477.13562,5556.76550,5636.24857,5716.57113,5795.71177,5878.88850,5960.71223,6044.83986,6136.15891,6231.44349,6326.36311,6423.41678,6520.06472,6617.47200,6707.25435,6795.78851,6879.35649,6944.22510,6999.94219,7029.12372,7049.35684,7049.36375,7040.16329,7019.18179,6987.21488,6941.03008,6874.78095,6794.77727,6693.85899,6571.41845,6421.71956,6231.59800,5983.70172,5595.46041,3803.28446,1631.10576])

T09ws = np.array([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99])
T09F  = np.array([2.466426647, -6.102401433, -22.41119756, -31.74206914, -24.51021714, 5.565433172, 3.978667244, 45.35894866,  116.3885444, 195.9972769, 300.4905685, 395.6087327, 459.289683, 509.5909316, 544.8756767, 578.2776562,  611.2867936, 640.645114, 663.6307643, 682.0415665, 698.9345394, 713.4273335, 723.9324389, 732.4140655,  736.5545315, 739.3061466, 740.6417222, 741.4951884, 741.5340658, 741.9325653, 741.9325653, 741.9325653,  741.9325652, 741.4990066, 741.4976765, 741.4976766, 741.0627028, 741.0628311, 740.6275825, 739.9607966,  739.3920882, 738.8874424, 738.0188953, 737.1477733, 736.2819735, 735.4101586, 734.5393215, 733.6789379,  732.6380763, 731.6251782, 730.8846699, 729.8721722, 729.1293867, 728.0351198, 726.7158916, 725.8416883,  724.7509356, 723.6879219, 722.5615559, 721.8185603, 721.0619134, 720.5000983, 719.7532322, 719.3182703,  718.8834586, 718.8845549, 718.4485683, 718.8817635, 718.8834571, 718.8834571, 718.8834571, 718.8834598,  718.4485606, 718.0136751, 717.2309955, 716.4887282, 715.3216324, 713.4160998, 711.0311725, 709.2828716,  706.7037061, 704.081225, 700.9490895, 697.6879434, 693.7676958, 688.754938, 682.9138321, 675.4816135,  666.5522488, 655.9214158, 642.8524738, 627.6436062, 609.0952716, 587.1959974, 560.2807123, 524.4749028,  477.7354055, 421.6709003, 245.0133894, 58.42078875])

N09ws = np.array([0.000,0.010,0.020,0.030,0.040,0.050,0.060,0.070,0.080,0.090,0.100,0.110,0.120,0.130,0.140,0.150,0.160,0.170,0.180,0.190,0.200,0.210,0.220,0.230,0.240,0.250,0.260,0.270,0.280,0.290,0.300,0.310,0.320,0.330,0.340,0.350,0.360,0.370,0.380,0.390,0.400,0.410,0.420,0.430,0.440,0.450,0.460,0.470,0.480,0.490,0.500,0.510,0.520,0.530,0.540,0.550,0.560,0.570,0.580,0.590,0.600,0.610,0.620,0.630,0.640,0.650,0.660,0.670,0.680,0.690,0.700,0.710,0.720,0.730,0.740,0.750,0.760,0.770,0.780,0.790,0.800,0.810,0.820,0.830,0.840,0.850,0.860,0.870,0.880,0.890,0.900,0.910,0.920,0.930,0.940,0.950,0.960,0.970,0.980,0.990])
N09F  = np.array([78.40049,32.27904,3.71122,32.26304,49.43242,91.98628,152.48113,228.17620,320.45104,443.68455,618.67330,795.83265,975.96753,1158.23147,1304.48637,1457.42341,1632.39312,1809.78346,1955.89062,2099.83085,2234.56841,2364.64296,2488.88513,2614.46832,2733.37726,2848.53205,2962.79678,3071.53914,3180.35663,3286.95101,3392.18032,3498.91879,3604.39877,3710.19280,3816.24779,3922.65678,4029.32657,4133.69503,4239.44781,4344.74655,4449.59829,4554.87182,4659.13510,4762.20243,4864.25486,4968.70690,5069.23027,5168.30838,5268.55874,5369.06370,5469.34000,5571.59687,5672.01801,5776.24090,5879.67012,5984.74169,6089.18784,6193.58726,6298.65385,6402.60067,6508.08805,6612.02459,6718.74267,6821.49041,6923.77246,7025.82049,7128.40007,7227.55468,7329.66364,7431.58723,7533.90248,7638.36080,7756.61845,7875.08295,7996.85901,8120.60492,8243.10802,8366.58642,8480.71779,8589.60843,8693.49529,8781.09424,8847.91332,8884.33756,8908.64447,8908.68282,8898.99063,8876.59668,8830.73777,8771.82367,8686.34443,8586.05774,8455.60920,8306.32403,8113.68260,7870.99737,7556.24342,7073.31811,4759.67816,2064.86593])

T10ws = np.array([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99])
T10F  = np.array([-6.173256293, -19.59153033, -36.36743594, -42.17275545, -38.59487767, -11.14127367, 33.28325364, 95.08322305,  180.9452335, 282.3474264, 390.3889289, 487.7086202, 566.51865, 629.0540765, 673.5066288, 714.6622621,  755.4228306, 791.1731032, 819.7538689, 842.3236251, 863.3354978, 881.1577231, 894.2232734, 904.779776,  909.8467956, 913.6645643, 914.8563989, 915.8879198, 916.3230801, 916.7578789, 916.7578762, 916.7578762,  916.3275797, 916.3229874, 915.8710639, 915.8880986, 915.457618, 915.4531981, 914.6642001, 914.1486357,  913.6075115, 912.8310591, 911.8248487, 910.6712491, 909.6655228, 908.4944628, 907.450312, 906.0301724,  905.0116395, 903.8421742, 902.8529436, 901.5196116, 900.6646524, 899.3813262, 898.0565575, 896.4126081,  895.4470158, 893.7855278, 892.8410051, 891.5998944, 890.6628197, 889.7827553, 889.3371855, 888.4928526,  888.0551368, 887.6545081, 887.6203244, 887.6193645, 888.0552133, 888.0552133, 888.0552133, 887.8479635,  887.6163587, 887.1847177, 886.2278411, 885.0107991, 883.2760949, 881.2830667, 878.6958306, 875.8051772,  872.8718017, 869.5110547, 865.7637187, 861.6195359, 857.0570795, 850.7432822, 843.3779825, 834.1964625,  823.3796217, 809.7980398, 793.7740148, 774.7390232, 751.9609073, 724.4989354, 691.8172368, 647.8543405,  589.8401729, 520.8677392, 380.0149326, 175.1731327])

N10ws = np.array([0.000,0.010,0.020,0.030,0.040,0.050,0.060,0.070,0.080,0.090,0.100,0.110,0.120,0.130,0.140,0.150,0.160,0.170,0.180,0.190,0.200,0.210,0.220,0.230,0.240,0.250,0.260,0.270,0.280,0.290,0.300,0.310,0.320,0.330,0.340,0.350,0.360,0.370,0.380,0.390,0.400,0.410,0.420,0.430,0.440,0.450,0.460,0.470,0.480,0.490,0.500,0.510,0.520,0.530,0.540,0.550,0.560,0.570,0.580,0.590,0.600,0.610,0.620,0.630,0.640,0.650,0.660,0.670,0.680,0.690,0.700,0.710,0.720,0.730,0.740,0.750,0.760,0.770,0.780,0.790,0.800,0.810,0.820,0.830,0.840,0.850,0.860,0.870,0.880,0.890,0.900,0.910,0.920,0.930,0.940,0.950,0.960,0.970,0.980,0.990])
N10F  = np.array([38.16988,61.93259,96.83108,123.62141,135.31269,193.68158,264.56217,355.44645,468.21882,630.74942,826.04023,1019.97829,1222.65001,1427.63574,1607.92965,1796.51398,2012.10717,2230.14743,2414.33408,2587.16149,2750.71838,2916.51706,3072.50882,3222.55074,3369.09082,3514.29466,3648.90116,3788.42936,3923.57892,4056.17840,4184.07893,4316.09364,4448.22687,4575.56582,4711.72922,4834.84935,4970.13712,5094.63225,5229.36431,5359.66810,5488.56735,5622.25584,5747.06293,5873.10431,5997.95308,6128.55163,6252.47759,6375.91574,6496.57994,6620.38511,6744.58528,6869.90159,6994.35393,7128.01718,7254.32222,7377.64977,7513.60091,7636.84987,7772.83016,7896.31570,8031.52615,8155.60799,8281.50564,8414.88138,8540.18399,8664.74912,8789.52674,8914.71807,9038.06127,9164.03818,9292.28881,9425.76285,9566.58065,9713.33014,9864.44508,10011.08355,10164.46839,10315.25001,10459.36566,10593.99602,10723.09824,10828.42162,10914.47233,10958.69653,10986.65786,10991.64556,10976.31633,10946.03366,10889.60898,10817.41833,10711.39329,10588.70090,10429.86193,10239.55672,10008.62510,9703.52451,9324.25232,8713.17342,6856.53594,3853.76213,])

if forces:

    print('Plotting spanwise forces')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(11, 5), constrained_layout=True)

    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['rOverR'],np.mean(wrfles_data[count]['ft'],axis=(0,2)),
                        color=force_colors[count],linestyle='solid',linewidth=2,label=name)    
        # ax[0].set_xlim([0,1])
        ax[0].set_xticks(np.arange(0,1.2,0.2));
        # ax[0].axes.xaxis.set_ticklabels([])
        ax[0].set_ylabel(r'Tangential force [N/m]')
        ax[0].set_xlabel(r'Spanwise position $r/R$ [-]')
        ax[0].legend(loc="upper right", fancybox=True, shadow=False, ncol=3, fontsize=8)


        ax[1].plot(wrfles_data[count]['rOverR'],np.mean(wrfles_data[count]['fn'],axis=(0,2)),
                        color=force_colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[0].set_xlim([0,1])
        ax[1].set_xticks(np.arange(0,1.2,0.2));
        # ax[1].axes.xaxis.set_ticklabels([])
        ax[1].set_ylabel(r'Normal force [N/m]')
        ax[1].set_xlabel(r'Spanwise position $r/R$ [-]')
        ax[1].legend(loc="upper right", fancybox=True, shadow=False, ncol=3, fontsize=8)

    # ax[0].plot(T06ws,T06F,color=force_colors[0],linestyle='--',linewidth=2)
    # ax[0].plot(T07ws,T07F,color=force_colors[1],linestyle='--',linewidth=2)
    # ax[0].plot(T08ws,T08F,color=force_colors[2],linestyle='--',linewidth=2)
    # ax[0].plot(T09ws,T09F,color=force_colors[3],linestyle='--',linewidth=2)
    # ax[0].plot(T10ws,T10F,color=force_colors[4],linestyle='--',linewidth=2)

    # ax[1].plot(N06ws,N06F,color=force_colors[0],linestyle='--',linewidth=2)
    # ax[1].plot(N07ws,N07F,color=force_colors[1],linestyle='--',linewidth=2)
    # ax[1].plot(N08ws,N08F,color=force_colors[2],linestyle='--',linewidth=2)
    # ax[1].plot(N09ws,N09F,color=force_colors[3],linestyle='--',linewidth=2)
    # ax[1].plot(N10ws,N10F,color=force_colors[4],linestyle='--',linewidth=2)

    # plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/iea22MW_validation/gad_sweep/figs/spanwise_forces.png", bbox_inches="tight", dpi=600)    

###########################################################################
# disk-averaged quantities along the blade
###########################################################################

if disk_avg:

    print('Plotting disk-averaged quantities')

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(11, 5), constrained_layout=True)

    for count, name in enumerate(casenames):
        ax[0,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['aoam'],
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0,0].set_xlim([0,1])
        # ax[0,0].set_ylim([0,60])
        ax[0,0].set_xticks(np.arange(0,1.2,0.2));
        # ax[0,0].set_yticks(np.arange(0,80,20))
        ax[0,0].axes.xaxis.set_ticklabels([])
        ax[0,0].set_ylabel(r'$\overline{\alpha}~[^{\circ}]$')
        ax[0,0].legend(loc="upper right", fancybox=True, shadow=False, ncol=3, fontsize=8)

    for count, name in enumerate(casenames):
        ax[0,1].plot(wrfles_data[count]['rOverR'],(1.0-wrfles_data[count]['v1m_star']),
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0,1].set_xlim([0,1])
        # ax[0,1].set_ylim([0.1,0.4])
        ax[0,1].set_xticks(np.arange(0,1.2,0.2));
        # ax[0,1].set_yticks(np.arange(0.1,0.5,0.1))
        ax[0,1].axes.xaxis.set_ticklabels([])
        ax[0,1].set_ylabel(r'$\overline{a}=1-\frac{\overline{u}_{m}}{U_{\infty}}~[-]$')

    for count, name in enumerate(casenames):
        ax[1,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fd_star'],
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1,0].set_xlim([0,1])
        # ax[1,0].set_ylim([0,0.01])
        ax[1,0].set_xticks(np.arange(0,1.2,0.2));
        # ax[1,0].set_yticks(np.arange(0,0.0125,0.005))
        ax[1,0].set_ylabel(r'$\overline{F}^{*}_{D}~[-]$'); ax[1,0].set_xlabel(r'$r/R~[-]$')

    for count, name in enumerate(casenames):
        ax[1,1].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fl_star'],
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1,1].set_xlim([0,1])
        # ax[1,1].set_ylim([-0.025,0.6])
        ax[1,1].set_xticks(np.arange(0,1.2,0.2));
        # ax[1,1].set_yticks(np.arange(0.0,0.8,0.2))
        ax[1,1].set_ylabel(r'$\overline{F}^{*}_{L}~[-]$'); ax[1,1].set_xlabel(r'$r/R~[-]$')

    plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/iea15MW_validation/gad_sweep/figs/disk_averaged_quantities.png", bbox_inches="tight", dpi=600)    

###########################################################################
# y-z wind speed profile comparison
###########################################################################

if profiles:

    print('Plotting wind speed profiles')

    fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(16, 6), constrained_layout=True)

    # 0D
    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['uxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0].set_xlim([0.0,1.5])
        ax[0].set_ylim([-1.0,1.0])
        ax[0].set_xticks(np.linspace(0.25,1.25,3))
        ax[0].set_yticks(np.linspace(-1,1.0,5))
        ax[0].grid(True, 'major', alpha=0.2)
        ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize);
        ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
        ax[0].set_title(r'$x/D=0$')
        ax[0].legend(loc="best", fancybox=True, shadow=False, framealpha=0.5, ncol=1, fontsize=8)

    # 1D
    # for count, name in enumerate(casenames):
        ax[1].plot(wrfles_data[count]['uxyt_2D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1].set_xlim([0.0,1.5])
        ax[1].set_ylim([-1.0,1.0])
        ax[1].set_xticks(np.linspace(0.25,1.25,3))
        ax[1].set_yticks(np.linspace(-1,1.0,5))
        ax[1].grid(True, 'major', alpha=0.2)
        ax[1].axes.yaxis.set_ticklabels([])
        ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
        ax[1].set_title(r'$x/D=2$')

    # 3D
    # for count, name in enumerate(casenames):
        ax[2].plot(wrfles_data[count]['uxyt_4D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[2].set_xlim([0.0,1.5])
        ax[2].set_ylim([-1.0,1.0])
        ax[2].set_xticks(np.linspace(0.25,1.25,3))
        ax[2].set_yticks(np.linspace(-1,1.0,5))
        ax[2].grid(True, 'major', alpha=0.2)
        ax[2].axes.yaxis.set_ticklabels([])
        ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
        ax[2].set_title(r'$x/D=4$')

    # # 6D
    # # for count, name in enumerate(casenames):
    #     ax[3].plot(wrfles_data[count]['uxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[3].set_xlim([0.0,1.5])
    #     ax[3].set_ylim([-1.0,1.0])
    #     ax[3].set_xticks(np.linspace(0.25,1.25,3))
    #     ax[3].set_yticks(np.linspace(-1,1.0,5))
    #     ax[3].grid(True, 'major', alpha=0.2)
    #     ax[3].axes.yaxis.set_ticklabels([])
    #     ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
    #     ax[3].set_title(r'$x/D=6$')

    # # 9D
    # # for count, name in enumerate(casenames):
    #     ax[4].plot(wrfles_data[count]['uxyt_8D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[4].set_xlim([0.0,1.5])
    #     ax[4].set_ylim([-1.0,1.0])
    #     ax[4].set_xticks(np.linspace(0.25,1.25,3))
    #     ax[4].set_yticks(np.linspace(-1,1.0,5))
    #     ax[4].grid(True, 'major', alpha=0.2)
    #     ax[4].axes.yaxis.set_ticklabels([])
    #     ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
    #     ax[4].set_title(r'$x/D=8$')

    # # 12D
    # # for count, name in enumerate(casenames):
    #     ax[5].plot(wrfles_data[count]['uxyt_10D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[5].set_xlim([0.0,1.5])
    #     ax[5].set_ylim([-1.0,1.0])
    #     ax[5].set_xticks(np.linspace(0.25,1.25,3))
    #     ax[5].set_yticks(np.linspace(-1,1.0,5))
    #     ax[5].grid(True, 'major', alpha=0.2)
    #     ax[5].axes.yaxis.set_ticklabels([])
    #     ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
    #     ax[5].set_title(r'$x/D=10$')

    plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/clockwise/gad_sweep/figs/u_profiles.png", bbox_inches="tight", dpi=600)  


    fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(16, 6), constrained_layout=True)

    # 0D
    xlims = [-1.5, 1.0]
    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['vxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0].set_xlim(xlims)
        ax[0].set_ylim([-1.0,1.0])
        # ax[0].set_xticks(np.linspace(0.25,1.25,3))
        ax[0].set_yticks(np.linspace(-1,1.0,5))
        ax[0].grid(True, 'major', alpha=0.2)
        ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize);
        ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
        ax[0].set_title(r'$x/D=0$')
        ax[0].legend(loc="best", fancybox=True, shadow=False, framealpha=0.5, ncol=1, fontsize=8)

    # 1D
    # for count, name in enumerate(casenames):
        ax[1].plot(wrfles_data[count]['vxyt_2D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1].set_xlim(xlims)
        ax[1].set_ylim([-1.0,1.0])
        # ax[1].set_xticks(np.linspace(0.25,1.25,3))
        ax[1].set_yticks(np.linspace(-1,1.0,5))
        ax[1].grid(True, 'major', alpha=0.2)
        ax[1].axes.yaxis.set_ticklabels([])
        ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
        ax[1].set_title(r'$x/D=2$')

    # 3D
    # for count, name in enumerate(casenames):
        ax[2].plot(wrfles_data[count]['vxyt_4D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[2].set_xlim(xlims)
        ax[2].set_ylim([-1.0,1.0])
        # ax[2].set_xticks(np.linspace(0.25,1.25,3))
        ax[2].set_yticks(np.linspace(-1,1.0,5))
        ax[2].grid(True, 'major', alpha=0.2)
        ax[2].axes.yaxis.set_ticklabels([])
        ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
        ax[2].set_title(r'$x/D=4$')

    # # 6D
    # # for count, name in enumerate(casenames):
    #     ax[3].plot(wrfles_data[count]['vxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[3].set_xlim(xlims)
    #     ax[3].set_ylim([-1.0,1.0])
    #     # ax[3].set_xticks(np.linspace(0.25,1.25,3))
    #     ax[3].set_yticks(np.linspace(-1,1.0,5))
    #     ax[3].grid(True, 'major', alpha=0.2)
    #     ax[3].axes.yaxis.set_ticklabels([])
    #     ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
    #     ax[3].set_title(r'$x/D=6$')

    # # 9D
    # # for count, name in enumerate(casenames):
    #     ax[4].plot(wrfles_data[count]['vxyt_8D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[4].set_xlim(xlims)
    #     ax[4].set_ylim([-1.0,1.0])
    #     # ax[4].set_xticks(np.linspace(0.25,1.25,3))
    #     ax[4].set_yticks(np.linspace(-1,1.0,5))
    #     ax[4].grid(True, 'major', alpha=0.2)
    #     ax[4].axes.yaxis.set_ticklabels([])
    #     ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
    #     ax[4].set_title(r'$x/D=8$')

    # # 12D
    # # for count, name in enumerate(casenames):
    #     ax[5].plot(wrfles_data[count]['vxyt_10D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[5].set_xlim(xlims)
    #     ax[5].set_ylim([-1.0,1.0])
    #     # ax[5].set_xticks(np.linspace(0.25,1.25,3))
    #     ax[5].set_yticks(np.linspace(-1,1.0,5))
    #     ax[5].grid(True, 'major', alpha=0.2)
    #     ax[5].axes.yaxis.set_ticklabels([])
    #     ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
    #     ax[5].set_title(r'$x/D=10$')

    plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/clockwise/gad_sweep/figs/v_profiles.png", bbox_inches="tight", dpi=600)  

# # ###########################################################################
# # # y-z wind speed profile comparison
# # ###########################################################################

# # fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(16, 6), constrained_layout=True)

# # # 0D
# # for count, name in enumerate(casenames):
# #     ax[0].plot(wrfles_data[count]['uupxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[0].set_xlim([0.0,1.5])
# # # ax[0].set_ylim([-1.0,1.0])
# # # ax[0].set_xticks(np.linspace(0.25,1.25,3))
# # ax[0].set_yticks(np.linspace(-1,1.0,5))
# # ax[0].grid(True, 'major', alpha=0.2)
# # ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize);
# # ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
# # ax[0].set_title(r'$x/D=0$')
# # ax[0].legend(loc="upper center", fancybox=True, shadow=False, framealpha=0.5, bbox_to_anchor=(0.675, 0.6), ncol=1, fontsize=12)

# # # 1D
# # for count, name in enumerate(casenames):
# #     ax[1].plot(wrfles_data[count]['uupxyt_1D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[1].set_xlim([0.0,1.5])
# # # ax[1].set_ylim([-1.0,1.0])
# # # ax[1].set_xticks(np.linspace(0.25,1.25,3))
# # ax[1].set_yticks(np.linspace(-1,1.0,5))
# # ax[1].grid(True, 'major', alpha=0.2)
# # ax[1].axes.yaxis.set_ticklabels([])
# # ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
# # ax[1].set_title(r'$x/D=1$')

# # # 3D
# # for count, name in enumerate(casenames):
# #     ax[2].plot(wrfles_data[count]['uupxyt_3D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[2].set_xlim([0.0,1.5])
# # # ax[2].set_ylim([-1.0,1.0])
# # # ax[2].set_xticks(np.linspace(0.25,1.25,3))
# # ax[2].set_yticks(np.linspace(-1,1.0,5))
# # ax[2].grid(True, 'major', alpha=0.2)
# # ax[2].axes.yaxis.set_ticklabels([])
# # ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
# # ax[2].set_title(r'$x/D=3$')

# # # 6D
# # for count, name in enumerate(casenames):
# #     ax[3].plot(wrfles_data[count]['uupxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[3].set_xlim([0.0,1.5])
# # # ax[3].set_ylim([-1.0,1.0])
# # # ax[3].set_xticks(np.linspace(0.25,1.25,3))
# # ax[3].set_yticks(np.linspace(-1,1.0,5))
# # ax[3].grid(True, 'major', alpha=0.2)
# # ax[3].axes.yaxis.set_ticklabels([])
# # ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
# # ax[3].set_title(r'$x/D=6$')

# # # 9D
# # for count, name in enumerate(casenames):
# #     ax[4].plot(wrfles_data[count]['uupxyt_9D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[4].set_xlim([0.0,1.5])
# # # ax[4].set_ylim([-1.0,1.0])
# # # ax[4].set_xticks(np.linspace(0.25,1.25,3))
# # ax[4].set_yticks(np.linspace(-1,1.0,5))
# # ax[4].grid(True, 'major', alpha=0.2)
# # ax[4].axes.yaxis.set_ticklabels([])
# # ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
# # ax[4].set_title(r'$x/D=9$')

# # # 12D
# # for count, name in enumerate(casenames):
# #     ax[5].plot(wrfles_data[count]['uupxyt_12D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[5].set_xlim([0.0,1.5])
# # # ax[5].set_ylim([-1.0,1.0])
# # # ax[5].set_xticks(np.linspace(0.25,1.25,3))
# # ax[5].set_yticks(np.linspace(-1,1.0,5))
# # ax[5].grid(True, 'major', alpha=0.2)
# # ax[5].axes.yaxis.set_ticklabels([])
# # ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
# # ax[5].set_title(r'$x/D=12$')

# # plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/px_z.png", bbox_inches="tight", dpi=600) 

###########################################################################
    # streamwise velocity component
    # wrfles
###########################################################################

if contours:

    print('Plotting streamwise velocity contours')

    ks = 0
    ke = 500
    js = 51
    je = 140

    levels = 255
    vmin = 0.5
    vmax = 1.0

    for count, name in enumerate(casenames):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,6), subplot_kw={"projection": "3d"})

        ax.set_box_aspect(aspect=(40,8,8))
        cs = ax.contourf(np.mean(wrfles_data[count]['ux_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=0*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_2D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=2*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_4D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=4*wrfles_data[count]['diameter'])
        # ax.contourf(np.mean(wrfles_data[count]['ux_6D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
        #                     wrfles_data[count]['Y3'][ks:ke,js:je],
        #                     wrfles_data[count]['Z3'][ks:ke,js:je],
        #                     levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
        #                     vmin=vmin, vmax=vmax, zdir='x', offset=6*wrfles_data[count]['diameter'])
        # ax.contourf(np.mean(wrfles_data[count]['ux_8D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
        #                     wrfles_data[count]['Y3'][ks:ke,js:je],
        #                     wrfles_data[count]['Z3'][ks:ke,js:je],
        #                     levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
        #                     vmin=vmin, vmax=vmax, zdir='x', offset=8*wrfles_data[count]['diameter'])
        # ax.contourf(np.mean(wrfles_data[count]['ux_10D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
        #                     wrfles_data[count]['Y3'][ks:ke,js:je],
        #                     wrfles_data[count]['Z3'][ks:ke,js:je],
        #                     levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
        #                     vmin=vmin, vmax=vmax, zdir='x', offset=10*wrfles_data[count]['diameter'])
        ax.view_init(azim=225, elev=30, roll=0)
        print(f"diameter: {wrfles_data[count]['diameter']}")
        ax.set_xticks(np.arange(0, 12*wrfles_data[count]['diameter'], 2*wrfles_data[count]['diameter']))
        ax.set_xticklabels([r'$0D$', r'$2D$', r'$4D$', r'$8D$', r'$8D$', r'$10D$'], fontsize=14)
        ax.tick_params(axis='x', labelrotation=-90)
        ax.set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
        ax.set_yticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='y', labelrotation=-30)
        ax.set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
        ax.set_zticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='z', labelrotation=-90)
        ax.xaxis.labelpad=50
        ax.yaxis.labelpad=-5
        ax.zaxis.labelpad=-5
        ax.yaxis.set_tick_params(pad=-5)
        ax.zaxis.set_tick_params(pad=-1)
        ax.set(xlabel=r'$x$', ylabel=r'$y$', zlabel=r'$z$')
        ax.set_title(casenames[count], fontsize=24, y=0.85)
        # Generate colorbar with adjusted settings
        cbar = fig.colorbar(cs, ax=ax, orientation='horizontal', pad=0.2, shrink=0.7)

        # Reduce the number of colorbar ticks to avoid overlap
        cbar.set_ticks(np.linspace(vmin, vmax, 6))  # Adjust the number of ticks to avoid crowding

        # Adjust tick label size and padding
        cbar.ax.tick_params(labelsize=10)  # Adjust tick label font size
        cbar.set_label('$\\overline{u}/U_{\\infty}$ [-]', fontsize=12, labelpad=15)  # Increase label padding

        plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/clockwise/gad_sweep/figs/{name}_uvel_yz.png", bbox_inches="tight", dpi=800)
        plt.close()

###########################################################################
# spanwise velocity component
vmin = -0.4
vmax = 0.4
###########################################################################

if contours:

    print('Plotting lateral velocity contours')

    for count, name in enumerate(casenames):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,8), subplot_kw={"projection": "3d"})

        ax.set_box_aspect(aspect=(40,8,8))
        cs = ax.contourf(np.mean(wrfles_data[count]['vx_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=0*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['vx_2D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=3*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['vx_4D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=6*wrfles_data[count]['diameter'])
        # ax.contourf(np.mean(wrfles_data[count]['vx_8D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
        #                     wrfles_data[count]['Y3'][ks:ke,js:je],
        #                     wrfles_data[count]['Z3'][ks:ke,js:je],
        #                     levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
        #                     vmin=vmin, vmax=vmax, zdir='x', offset=9*wrfles_data[count]['diameter'])
        # ax.contourf(np.mean(wrfles_data[count]['vx_10D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
        #                     wrfles_data[count]['Y3'][ks:ke,js:je],
        #                     wrfles_data[count]['Z3'][ks:ke,js:je],
        #                     levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
        #                     vmin=vmin, vmax=vmax, zdir='x', offset=12*wrfles_data[count]['diameter'])
        ax.view_init(azim=225, elev=30, roll=0)
        ax.set_xticks(np.arange(0, 15*wrfles_data[count]['diameter'], 3*wrfles_data[count]['diameter']))
        ax.set_xticklabels([r'$0D$', r'$3D$', r'$6D$', r'$9D$', r'$12D$'], fontsize=14)
        ax.tick_params(axis='x', labelrotation=-90)
        ax.set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
        ax.set_yticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='y', labelrotation=-30)
        ax.set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
        ax.set_zticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='z', labelrotation=-90)
        ax.xaxis.labelpad=50
        ax.yaxis.labelpad=-5
        ax.zaxis.labelpad=-5
        ax.yaxis.set_tick_params(pad=-5)
        ax.zaxis.set_tick_params(pad=-1)
        ax.set(xlabel=r'$x~[\textrm{m}]$', ylabel=r'$y~[\textrm{m}]$', zlabel=r'$z~[\textrm{m}]$')
        ax.set_title(casenames[count], fontsize=24, y=0.85)

        # Generate colorbar with adjusted settings
        cbar = fig.colorbar(cs, ax=ax, orientation='horizontal', pad=0.2, shrink=0.7)

        # Reduce the number of colorbar ticks to avoid overlap
        # cbar.set_ticks(np.linspace(vmin, vmax, 6))  # Adjust the number of ticks to avoid crowding

        # Adjust tick label size and padding
        cbar.ax.tick_params(labelsize=10)  # Adjust tick label font size
        cbar.set_label('$\\overline{u}/U_{\\infty}$ [-]', fontsize=12, labelpad=15)  # Increase label padding

        plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/clockwise/gad_sweep/figs/{name}_vvel_yz.png", bbox_inches="tight", dpi=800)
        plt.close()

###########################################################################
# spanwise velocity component
###########################################################################

if itqp:

    print('Plotting induction, power, thrust, and torque')

    # wrfles - simple controller
    # wrfles_rel_diff_power  = []
    # wrfles_rel_diff_thrust = []
    # wrfles_rel_diff_torque = []
    # wrfles_rel_diff_ind    = []
    # for count in range(len(casenames)):
    #     wrfles_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']))
    #     wrfles_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']))
    #     wrfles_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']))
    #     wrfles_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])))

    width = 0.75
    alpha = 1.0

    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(13, 9), sharex=True, constrained_layout = True)
    ax[0].axhline(0, color='black', linestyle='solid', linewidth=1)
    ax[1].axhline(0, color='black', linestyle='solid', linewidth=1)
    ax[2].axhline(0, color='black', linestyle='solid', linewidth=1)
    ax[3].axhline(0, color='black', linestyle='solid', linewidth=1)

    ind = np.arange(len(casenames))

    for count in range(len(casenames)):

        wrfles_rel_diff_power  = []
        wrfles_rel_diff_thrust = []
        wrfles_rel_diff_torque = []
        wrfles_rel_diff_ind    = []

        wrfles_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']).round(1))
        wrfles_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']).round(1))
        wrfles_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']).round(1))
        wrfles_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])).round(1))

        # induction
        ax[0].bar(ind[count], wrfles_rel_diff_ind, color=colors[count], edgecolor='black', alpha=alpha)
        ax[0].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{a}}~[\%]$', fontsize=fontsize)
        ax[0].text(ind[count], 3, f'{wrfles_rel_diff_ind[0]}\%', ha='center', fontsize=15)

        # thrust
        ax[1].bar(ind[count], wrfles_rel_diff_thrust, color=colors[count], edgecolor='black', alpha=alpha)
        ax[1].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{T}}~[\%]$', fontsize=fontsize)
        ax[1].text(ind[count], -0.5, f'{wrfles_rel_diff_thrust[0]}\%', ha='center', fontsize=15)

        # torque
        ax[2].bar(ind[count], wrfles_rel_diff_torque, color=colors[count], edgecolor='black', alpha=alpha)
        ax[2].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{Q}}~[\%]$', fontsize=fontsize)
        ax[2].text(ind[count], -2.5, f'{wrfles_rel_diff_torque[0]}\%', ha='center', fontsize=15)

        # power
        ax[3].bar(ind[count], wrfles_rel_diff_power, color=colors[count], edgecolor='black', alpha=alpha)
        ax[3].set_xticks(ind)
        ax[3].set_xticklabels(casenames)
        ax[3].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{P}}~[\%]$', fontsize=fontsize)
        ax[3].text(ind[count], -2.5, f'{wrfles_rel_diff_power[0]}\%', ha='center', fontsize=15)

    plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/iea15MW_validation/gad_sweep/figs/rel_err_ind_thrust_torque_power.png", bbox_inches="tight", dpi=800)
    plt.show()

# # ###########################################################################
# # # calculate total wind speed in streamwise direction:
# # ###########################################################################
# # ws_uytz_gal = np.sqrt(wrfles_data['uytz_gal']**2 + wrfles_data['vytz_gal']**2 + wrfles_data['wytz_gal']**2)
# # ws_min = 0.0
# # ws_max = 10.0
# # # ws_max = wrfles_data['uinf_gal']

# # # calculate dynamic pressure:
# # p_dyn = 0.5*wrfles_data['rho']*ws_uytz_gal**2/1000.0 # in kPa

# # # calculate pressure drop:
# # delta_p = np.max(wrfles_data['pytz_gal']) - wrfles_data['pytz_gal'][int(wrfles_data['ix_rotor'])+3]

# # # power
# # rho = wrfles_data['rho']
# # a = 1-(ws_uytz_gal[int(wrfles_data['ix_rotor'])]/wrfles_data['uinf_gal'])
# # area = np.pi*wrfles_data['diameter']**2/4
# # thrust = 2*rho*wrfles_data['uinf_gal']**2*a*(1-a)*area/1E3   # kN
# # power = 2*rho*wrfles_data['uinf_gal']**3*a*(1-a)**2*area/1E3 # kW

# # p_min = 98.940
# # p_max = 98.980

# # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(13.5, 4), sharex=True, constrained_layout = True)

# # # velocity distribution in streamwise direction:
# # ax[0].plot(xx, ws_uytz_gal, color='black', linestyle='solid', linewidth=3, zorder=10)
# # ax[0].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [wrfles_data['uinf_gal'], wrfles_data['uinf_gal']],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[0].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [ws_uytz_gal[int(wrfles_data['ix_rotor'])], ws_uytz_gal[int(wrfles_data['ix_rotor'])]],
# #             color='red', linestyle='dashdot', linewidth=1.5)
# # ax[0].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [np.min(ws_uytz_gal), np.min(ws_uytz_gal)],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[0].plot([wrfles_data['rotor_xloc'],wrfles_data['rotor_xloc']], [ws_min,ws_max],
# #             color='black', linestyle='dashed', linewidth=1.5)    
# # ax[0].set_xlim([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                 wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[0].set_xticks([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc'],
# #                     wrfles_data['rotor_xloc']+(5*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(10*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(15*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(20*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(25*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[0].set_ylim([ws_min,ws_max])
# # ax[0].set_ylabel(r'$U~\textrm{[m~s$^{-1}$]}$', fontsize=fontsize)
# # ax[0].tick_params(direction='in', length=6)
# # ax[0].axes.xaxis.set_ticklabels([])

# # # pressure distribution in streamwise direction:
# # ax[1].plot(xx, wrfles_data['pytz_gal']/1000.0, color='black', linestyle='solid', linewidth=3, zorder=10)
# # ax[1].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [np.max(wrfles_data['pytz_gal'])/1000.0, np.max(wrfles_data['pytz_gal'])/1000.0],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[1].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [wrfles_data['pytz_gal'][0]/1000.0,wrfles_data['pytz_gal'][0]/1000.0],
# #             color='red', linestyle='dashdot', linewidth=1.5)
# # ax[1].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [wrfles_data['pytz_gal'][int(wrfles_data['ix_rotor'])+3]/1000.0,
# #             wrfles_data['pytz_gal'][int(wrfles_data['ix_rotor'])+3]/1000.0],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[1].plot([wrfles_data['rotor_xloc'],wrfles_data['rotor_xloc']], [p_min,p_max],
# #             color='black', linestyle='dashed', linewidth=1.5)    
# # ax[1].set_xlim([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                 wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[1].set_xticks([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc'],
# #                     wrfles_data['rotor_xloc']+(5*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(10*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(15*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(20*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(25*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[1].set_ylim([p_min,p_max])
# # ax[1].set_xlabel(r'$x/D~[-]$', fontsize=fontsize) 
# # ax[1].set_ylabel(r'$P_{tot}~\textrm{[kPa]}$', fontsize=fontsize)
# # ax[1].tick_params(direction='in', length=6)
# # ax[1].axes.xaxis.set_ticklabels([r'$-3$', r'$x_{rotor}$', r'$5$', r'$10$', r'$15$', r'$20$', r'$25$', r'$30$'], fontsize=fontsize)

# # plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/wrfles_vel_pres_dist.png", bbox_inches="tight", dpi=600)
# # plt.show()

# # ###########################################################################

# # ###########################################################################

# # vmin = 0.6
# # vmax = 1.0
# # for i in range(0,len(wrfles_data['ux_0D_gal'])):
# #     print(i,'/',wrfles_data['ux_0D_gal'].shape[0]-1)
# #     fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.2, 5), constrained_layout = True)
# #     # y-z contour plot for wind speed
# #     cs0 = ax.pcolormesh(wrfles_data['Y3'], wrfles_data['Z3'], wrfles_data['ux_0D_gal'][i,:,:]/wrfles_data['uinf_gal'],
# #                         vmin=vmin, vmax=vmax, alpha=1, cmap='Spectral_r', shading='gouraud', rasterized=True)
# #     ax.plot(wrfles_data['bpy_gal'][i,:,0], wrfles_data['bpz_gal'][i,:,0], color='black', marker='o',
# #             markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
# #     ax.plot(wrfles_data['bpy_gal'][i,:,1], wrfles_data['bpz_gal'][i,:,1], color='red', marker='o',
# #             markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
# #     ax.plot(wrfles_data['bpy_gal'][i,:,2], wrfles_data['bpz_gal'][i,:,2], color='limegreen', marker='o',
# #             markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
# #     # ax.set_xlim([300, 462])
# #     # ax.set_ylim([300, 460])
# #     ax.set_xticks([])
# #     ax.set_yticks([])
# #     ax.axes.xaxis.set_ticklabels([])
# #     ax.axes.yaxis.set_ticklabels([])
# #     ax.invert_xaxis()

# #     plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/u_00"+str(i)+".tif",bbox_inches="tight",dpi=100)

# #     plt.show()
# #     plt.close()

# # grid2gif('/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/rotorPlane/*.tif',
# #          '/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/uvel.gif')

print('Done.')
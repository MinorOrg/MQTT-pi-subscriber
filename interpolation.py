import numpy as np


esp1data=np.array([[-91.33333333, -74.8       , -86.14285714, -90.55555556,
        -90.        , -86.27272727, -93.        ],
       [-84.45      , -49.61538462, -85.25      , -91.2       ,
        -86.45454545, -91.        , -89.        ],
       [-94.91304348, -69.16666667, -81.70588235, -82.26315789,
        -84.63157895, -90.59090909, -94.08333333],
       [-93.09302326, -94.09677419, -88.95652174, -90.52173913,
        -92.09677419, -91.57978723, -95.29545455],
       [-94.75      , -92.45454545, -94.10526316, -91.42105263,
        -98.5       , -94.7       , -92.47826087],
       [-96.        , -95.22580645, -92.5862069 , -93.90909091,
        -91.86666667, -92.625     , -94.5       ],
       [-95.05128205, -95.72727273, -95.25      , -95.        ,
        -94.57142857, -88.        , -91.93333333]])
esp2data=np.array([[-96.33333333, -94.2       , -92.22222222, -92.44444444,
        -87.2       , -90.53846154, -92.64      ],
       [-92.        , -87.34375   , -92.70588235, -90.47826087,
        -82.46153846, -90.22222222, -92.1       ],
       [-96.52380952, -92.58823529, -91.5       , -91.3       ,
        -79.13636364, -73.05555556, -81.6875    ],
       [-98.5       , -91.14634146, -93.51428571, -79.4       ,
        -76.17073171, -51.08247423, -74.20454545],
       [-97.        , -96.66666667, -93.27272727, -89.9       ,
        -95.5       , -84.        , -77.        ],
       [-95.36666667, -96.53333333, -91.91666667, -92.92307692,
        -97.53333333, -93.58823529, -92.48148148],
       [-92.65306122, -92.23076923, -93.46666667, -91.55555556,
        -94.22222222, -96.9       , -97.41666667]])
esp3data=np.array([[-90.93333333, -93.6       , -89.        , -89.5       ,
        -89.6       , -90.        , -92.6744186 ],
       [-87.44      , -92.57142857, -87.4375    , -92.125     ,
        -88.66666667, -86.97058824, -96.19047619],
       [-84.88      , -95.        , -85.29411765, -93.1       ,
        -89.92      , -92.24      , -95.41666667],
       [-89.97142857, -86.78947368, -90.05128205, -88.20512821,
        -86.5       , -92.34183673, -94.84848485],
       [-88.61538462, -74.04      , -78.        , -81.95      ,
        -90.58823529, -91.88235294, -91.6       ],
       [-78.88888889, -63.83163265, -76.80555556, -86.91666667,
        -89.06666667, -92.5       , -92.12      ],
       [-90.68181818, -84.69230769, -87.4       , -91.375     ,
        -95.55555556, -91.2       , -95.83870968]])

scale = 0.5
x = np.arange(7) * 0.5
y = np.arange(7) * 0.5

esp_x1,esp_y1=(1,1)
esp_x2,esp_y2=(3,5)
esp_x3,esp_y3=(5,1)

def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)

def interpolate_distance(rssi,espdata,espx,espy):
    distances =[]
    for i in range(7):
        for j in range(7):
            d = distance(x[i],y[j],espx,espy)
            distances.append((d,espdata[i][j]))
    distances.sort()
    #print(distances)
    Distances = [x[0] for x in distances]
    #print(Distances)
    rssi_values=[x[1] for x in distances]
    #print(rssi_values)
    dist = np.interp(rssi,rssi_values,Distances)
    return dist



def main():
    rssi=float(input("Enter RSSI value"))
    espdata = esp1data
    dist=interpolate_distance(rssi,espdata,esp_x1,esp_y1)
    print(dist)


if __name__=="__main__":
    main()
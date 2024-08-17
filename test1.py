import pandas as pd
import requests
import math

# 替换为你自己的高德地图API key
API_KEY = '8827cba1d0802ab62f7b6df4c985a622'

# 地理坐标转换相关代码
PI = 3.14159265358979324


class LatLng:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


def transformGCJ2WGS(gcjLat, gcjLon):
    d = deltas(gcjLat, gcjLon)
    wgsPoint = LatLng(gcjLat - d.latitude, gcjLon - d.longitude)
    return wgsPoint


def deltas(lat, lon):
    a = 6378245.0
    ee = 0.00669342162296594323
    dLat = transformLats(lon - 105.0, lat - 35.0)
    dLon = transformLons(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    return LatLng(dLat, dLon)


def transformLats(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret


def transformLons(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret


def wgs84ToCGCS2000(wgsLat, wgsLon):
    # 简化假设WGS-84直接转换为CGCS2000
    return LatLng(wgsLat, wgsLon)


def gcjToCGCS2000(gcjLat, gcjLon):
    wgsPoint = transformGCJ2WGS(gcjLat, gcjLon)
    return wgs84ToCGCS2000(wgsPoint.latitude, wgsPoint.longitude)


# 调用高德地图API获取GCJ-02坐标
def geocode(address, key):
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'address': address,
        'key': key,
        'output': 'json'
    }
    response = requests.get(url, params=params)
    result = response.json()

    if result['status'] == '1' and len(result['geocodes']) > 0:
        location = result['geocodes'][0]['location']
        lng, lat = map(float, location.split(','))
        return LatLng(lat, lng)
    else:
        return None


def process_factory_locations(input_file, output_file, key):
    df = pd.read_excel(input_file)

    # 假设工厂名称列为 "Factory Name"
    def process_row(factory_name):
        gcj_location = geocode(factory_name, key)
        if gcj_location:
            wgs_location = transformGCJ2WGS(gcj_location.latitude, gcj_location.longitude)
            cgcs2000_location = wgs84ToCGCS2000(wgs_location.latitude, wgs_location.longitude)
            return pd.Series({
                'GCJ_Longitude': gcj_location.longitude,
                'GCJ_Latitude': gcj_location.latitude,
                'WGS_Longitude': wgs_location.longitude,
                'WGS_Latitude': wgs_location.latitude,
                'CGCS2000_Longitude': cgcs2000_location.longitude,
                'CGCS2000_Latitude': cgcs2000_location.latitude
            })
        else:
            return pd.Series({
                'GCJ_Longitude': None,
                'GCJ_Latitude': None,
                'WGS_Longitude': None,
                'WGS_Latitude': None,
                'CGCS2000_Longitude': None,
                'CGCS2000_Latitude': None
            })

    coordinates_df = df['Factory Name'].apply(process_row)
    df = pd.concat([df, coordinates_df], axis=1)

    df.to_excel(output_file, index=False)
    print(f'Processed data has been saved to {output_file}')


# 输入文件路径和输出文件路径
input_file = 'factories.xlsx'  # 输入的Excel文件路径
output_file = 'factories_with_coordinates.xlsx'  # 输出的Excel文件路径

# 处理并生成坐标数据
process_factory_locations(input_file, output_file, API_KEY)

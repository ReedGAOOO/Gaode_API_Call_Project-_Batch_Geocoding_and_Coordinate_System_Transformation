import pandas as pd
import requests
import math

# 替换为你自己的高德地图API key
API_KEY = '你的高德API_KEY,一串数字'

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


# 高德地图API调用函数
def geocode(address, key):
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'address': address,
        'key': key,
        'output': 'json'
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"HTTP error: {response.status_code}")
        return None, None

    result = response.json()
    print("API Response:", result)

    if result['status'] == '1' and len(result['geocodes']) > 0:
        location = result['geocodes'][0]['location']
        formatted_address = result['geocodes'][0]['formatted_address']
        return formatted_address, location
    else:
        print(f"API error: {result.get('info', 'Unknown error')}")
        return None, None


# 读取CSV文件
input_file = 'an_example_of_place_name_list.CSV'
df = pd.read_csv(input_file, encoding='GB18030')

# 创建 location, coordinates, X, Y 列
df['location'] = ''
df['coordinates'] = ''
df['X'] = ''
df['Y'] = ''

# 处理所有企业地址
for index, row in df.iterrows():
    company_address = row['企业地址']
    print(f"Processing address: {company_address}")

    address, location = geocode(company_address, API_KEY)

    if address and location:
        df.at[index, 'location'] = address
        df.at[index, 'coordinates'] = location

        # 提取经纬度
        gcj_lon, gcj_lat = map(float, location.split(','))

        # GCJ-02转WGS-84再转CGCS2000
        cgcs2000_point = gcjToCGCS2000(gcj_lat, gcj_lon)

        # 将转换后的CGCS2000坐标填入X和Y列
        df.at[index, 'X'] = cgcs2000_point.longitude
        df.at[index, 'Y'] = cgcs2000_point.latitude
    else:
        print(f"No valid location or address returned from API for index {index}.")

# 显示处理后的前几行数据
print(df.head())

# 保存结果到新文件
output_file = 'output_list_with_locations_and_coordinates.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f'Processed data have been saved to {output_file}')

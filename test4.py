import pandas as pd
import requests

# 替换为你自己的高德地图API key
API_KEY = '8827cba1d0802ab62f7b6df4c985a622'


# 定义API调用函数
def geocode(address, key):
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'address': address,
        'key': key,
        'output': 'json'
    }
    response = requests.get(url, params=params)

    # 检查HTTP响应状态码
    if response.status_code != 200:
        print(f"HTTP error: {response.status_code}")
        return None, None

    result = response.json()

    # 输出API返回的原始结果以便调试
    print("API Response:", result)

    # 检查API返回的状态
    if result['status'] == '1' and len(result['geocodes']) > 0:
        location = result['geocodes'][0]['location']
        formatted_address = result['geocodes'][0]['formatted_address']
        return formatted_address, location
    else:
        print(f"API error: {result.get('info', 'Unknown error')}")
        return None, None


# 读取CSV文件
input_file = 'D:\\DESKTOP\\一分院\\industry company list.CSV'
df = pd.read_csv(input_file, encoding='GB18030')

# 创建 location, coordinates, X, Y 列
df['location'] = ''
df['coordinates'] = ''
df['X'] = ''
df['Y'] = ''

# 调试：只处理第一个企业地址
first_company_address = df['企业地址'].iloc[0]
print(f"Processing address: {first_company_address}")

address, location = geocode(first_company_address, API_KEY)

# 检查返回的地址和地理坐标
print(f"Formatted Address: {address}")
print(f"Coordinates: {location}")

# 如果有返回结果，则保存到DataFrame
if address and location:
    df.at[0, 'location'] = address
    df.at[0, 'coordinates'] = location

    # 提取经纬度并分别存入 X 和 Y 列
    lon, lat = map(float, location.split(','))
    df.at[0, 'X'] = lon
    df.at[0, 'Y'] = lat
else:
    print("No valid location or address returned from API.")

# 显示处理后的第一行数据
print(df.head(1))

# 保存结果到新文件
output_file = 'D:\\desktop\\一分院\\industry_company_list_with_coordinates.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f'Processed data for the first company has been saved to {output_file}')


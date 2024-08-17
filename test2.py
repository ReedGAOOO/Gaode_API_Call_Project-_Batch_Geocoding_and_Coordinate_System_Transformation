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
    result = response.json()

    if result['status'] == '1' and len(result['geocodes']) > 0:
        location = result['geocodes'][0]['location']
        formatted_address = result['geocodes'][0]['formatted_address']
        return formatted_address, location
    else:
        return None, None

# 读取CSV文件
input_file = 'D:\\DESKTOP\\一分院\\industry company list.CSV'
df = pd.read_csv(input_file, encoding='GB18030')

# 调试：只处理第一个企业名称
first_company_name = df['企业地址'].iloc[0]
address, location = geocode(first_company_name, API_KEY)

# 将结果保存回DataFrame的第一行
df.at[0, 'location'] = address
df.at[0, 'coordinates'] = location

# 显示处理后的第一行数据
print(df.head(1))

# 保存结果到新文件
output_file = 'D:\\desktop\\一分院\\industry_company_list_with_first_location.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f'Processed data for the first company has been saved to {output_file}')

该项目旨在通过调用高德地图API，使用表格*批量*根据地名获取对应的地理坐标信息（经纬度），并将其转换为CGCS2000坐标系。处理后的数据将保存到新的CSV文件中。项目代码包括地理坐标转换的实现、API调用的具体步骤以及数据处理流程。

This project aims to use the Gaode Map (AMAP) API to obtain geographic coordinates (latitude and longitude) *in bulk* based on company names and convert them to the CGCS2000 coordinate system. The processed data is then saved into a new CSV file. The project code includes the implementation of geographic coordinate transformation, steps for API calls, and data processing procedures.







1. 确保`an_example_of_place_name_list.CSV`文件和代码文件在同一目录下。
2. 运行`English Version.py`或`中文版.py`文件，程序将会读取CSV文件，调用高德API获取地址的地理坐标，并将转换后的CGCS2000坐标保存到新的CSV文件中。
3. 输出文件`output_list_with_locations_and_coordinates.csv`将会保存在同一目录下。 


- `pandas`: 用于处理CSV文件的数据处理库。
  **pandas**: A data processing library used to handle CSV files.

- `requests`: 用于与高德API进行HTTP请求的库。
  **requests**: A library used for making HTTP requests to the Gaode API.


- 在代码中，您需要替换为您自己的高德地图API密钥。
You need to replace the Gaode Map API key with your own in the code.

- 文件路径问题：如果代码与CSV文件位于不同目录，请确保在代码中使用正确的文件路径。
File Path Issues: If the code and CSV file are in different directories, ensure you use the correct file path in the code.



---



---

# 高德API调用项目 - 地名批量获取地理坐标 & 地理坐标系转化为标准坐标系 (Gaode API Call Project - Batch Geocoding & Coordinate System Transformation)
---

## 项目简介 Project Overview

该项目的核心功能包括：
1. **地名批量获取地理坐标**：通过调用高德地图API，根据多个企业地址批量获取对应的地理坐标信息（经纬度）。
2. **地理坐标系转化为标准坐标系**：将获取到的GCJ-02坐标系转换为WGS-84坐标系，并进一步转换为CGCS2000坐标系，方便后续使用。

The core functionalities of this project include:
1. **Batch Geocoding**: Using the Gaode Map API to batch retrieve geographic coordinates (latitude and longitude) based on multiple company addresses.
2. **Coordinate System Transformation**: Converting the retrieved GCJ-02 coordinates to the WGS-84 system and further to the CGCS2000 coordinate system for standardized usage.
---

## 文件结构 File Structure

- `an_example_of_place_name_list.CSV`: 输入的包含企业地址的CSV文件。  
   `an_example_of_place_name_list.CSV`: The input CSV file containing company addresses.

- `output_list_with_locations_and_coordinates.csv`: 输出的包含转换后标准坐标的CSV文件。  
  `output_list_with_locations_and_coordinates.csv`: The output CSV file containing the transformed standard coordinates.

- `English Version.py`: 使用英文注释的主代码文件。  
  `English Version.py`: The main code file with English comments.

- `中文版.py`: 使用中文注释的主代码文件。  
  `中文版.py`: The main code file with Chinese comments.

---

## 使用说明 Usage

1. 确保`an_example_of_place_name_list.CSV`文件和代码文件在同一目录下。
2. 运行`English Version.py`或`中文版.py`文件，程序将会批量处理CSV文件中的企业地址，调用高德API获取地理坐标，并将转换后的标准CGCS2000坐标保存到新的CSV文件中。
3. 输出文件`output_list_with_locations_and_coordinates.csv`将会保存在同一目录下。

- Ensure the `an_example_of_place_name_list.CSV` file and the code files are in the same directory.
- Run the `English Version.py` or `中文版.py` file. The program will batch process the company addresses in the CSV file, call the Gaode API to obtain geographic coordinates, and save the transformed standard CGCS2000 coordinates into a new CSV file.
- The output file `output_list_with_locations_and_coordinates.csv` will be saved in the same directory.
---

## 依赖项 Dependencies

- `pandas`: 用于处理CSV文件的数据处理库。  
  **pandas**: A data processing library used to handle CSV files.

- `requests`: 用于与高德API进行HTTP请求的库。  
  **requests**: A library used for making HTTP requests to the Gaode API.
---

## 注意事项 Notes

- 在代码中，您需要替换为您自己的高德地图API密钥。  
  You need to replace the Gaode Map API key with your own in the code.

- 文件路径问题：如果代码与CSV文件位于不同目录，请确保在代码中使用正确的文件路径。  
  File Path Issues: If the code and CSV file are in different directories, ensure you use the correct file path in the code.
---

## 作者 Author

该项目由[GAO Yijie (Reed GAO)]开发。  
This project was developed by [GAO Yijie (Reed GAO)].

---

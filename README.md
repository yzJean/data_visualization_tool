# Data visualization tools for csv file
## Usages
### Libraries
- `tool_painter.py`: A tool for data visualization
- `tool_reader.py`: A tool for reading `csv` file with user-specified headers
- `tool_writer.py`: A tool for writing out data in `csv` format
### Applications
- `main_gnss_data_preprocessor.py`: An example of `tool_reader.py` and `tool_writer.py`
  - Functionality: A parser to extract required GNSS data from the input file
- `main_xml_to_csv.py`: An example of `tool_reader.py` and `tool_writer.py`
  - Functionality: A parser to parse a file from `xml` to `csv` format
- `main_vis_sdmap_query.py`: An example of `tool_reader.py` and `tool_painter.py`
  - Functionality: A tool for visualizing a given map and match results

## Examples
- `main_gnss_data_preprocessor.py`
  ```
    python3 main_gnss_data_preprocessor.py -i ../sample_data/GNSS.csv
  ``` 
  - Results: An output file `GNSS_processed.csv`

- `main_vis_sdmap_query.py`
  1. Visualize a map
    ```
      python3 main_vis_sdmap_query.py -i ../sample_data/test1_map.csv -s <start-timestamp> -e <end-timestamp>
    ```
    - Results

      ![image](https://github.com/yzJean/csv_processing_tools/assets/59329465/e22a9ba9-ca77-40b0-a153-d5592c868037)


  2. Visualize matching results
    ```
      python3 main_vis_sdmap_query.py -i ../sample_data/test1_map.csv -u ../sample_data/test1_data.csv --sampling_rate=100 -s <start-timestamp> -e <end-timestamp>
    ```
  - Results

    a) Overall view

    ![image](https://github.com/yzJean/csv_processing_tools/assets/59329465/7a40f865-f63a-4643-b16c-b73257315a32)


    b) Matched & Unmatched

    ![image](https://github.com/yzJean/csv_processing_tools/assets/59329465/bccd82bf-cb42-40da-8c5e-0af559302de0)


- `main_xml_to_csv.py`
  ```
    python3 main_xml_to_csv.py -i ../sample_data/test2_map.osm
  ```
  - Results: An output file `test2_map.csv`

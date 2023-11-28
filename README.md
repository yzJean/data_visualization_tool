# Data processing tools for csv file
## Libraries
- `tool_painter.py`: A tool for data visualization
- `tool_reader.py`: A tool for reading `csv` file with user-specified headers
- `tool_writer.py`: A tool for writing out data in `csv` format

## Explanation
- `main_gnss_data_preprocessor.py`: An example of `tool_reader.py` and `tool_writer.py`
  - Functionality: A parser to extract required GNSS data from the input file
- `main_xml_to_csv.py`: An example of `tool_reader.py` and `tool_writer.py`
  - Functionality: A parser to parse a file from `xml` to `csv` format
- `main_vis_sdmap_query.py`: An example of `tool_reader.py` and `tool_painter.py`
  - Functionality: A tool for visualizing a given map and match results

## Examples
- `main_gnss_data_preprocessor.py`
  ```
    python3 main_gnss_data_preprocessor.py -i ../test/GNSS.csv
  ``` 
  - Results: An output file `GNSS_processed.csv`

- `main_vis_sdmap_query.py`
  1. Visualize a map
    ```
      python3 main_vis_sdmap_query.py -i ../test/test1_map.csv -s <start-timestamp> -e <end-timestamp>
    ```
    - Results

      ![image](https://github.com/yzJean/csv_processing_tools/assets/59329465/808b414b-f243-4068-a664-40198af83c25)

  2. Visualize matching results
    ```
      python3 main_vis_sdmap_query.py -i ../test/test1_map.csv -u ../test/test1_data.csv --sampling_rate=100 -s <start-timestamp> -e <end-timestamp>
    ```
  - Results
    a) Overall view

    ![image](https://github.com/yzJean/csv_processing_tools/assets/59329465/b59ae00c-541d-4b3a-af08-d10d284a772c)

    b) Matched & Unmatched

    ![image](https://github.com/yzJean/csv_processing_tools/assets/59329465/8d23a58e-c994-4df8-bc57-3fcee57fc936)

- `main_xml_to_csv.py`
  ```
    python3 main_xml_to_csv.py -i ../test/test2_map.osm
  ```
  - Results: An output file `test2_map.csv`

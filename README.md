# Sensor Readings

A small interactive Python program for generating or loading sensor readings. It prints summary statistics, reports values above a chosen threshold, and displays a readings plot and histogram.

## Requirements

- Python 3
- NumPy
- Matplotlib

Install the required packages:

```bash
python -m pip install numpy matplotlib
```

## Run

```bash
python main.py
```

Choose whether to generate readings or load them from a CSV file, then follow the prompts to enter the sensor type and threshold. When generating readings, you will also enter the number of readings and their minimum and maximum values. Generated readings are saved to `sensor_readings.csv`.

## CSV format

To load readings, provide a path to a CSV file with a `sensor_reading` column. For example:

```csv
sample_number,sensor_reading
0,12.5
1,14.2
2,9.8
```

The program calculates the count, mean, minimum, maximum, and standard deviation, and flags readings greater than the threshold.

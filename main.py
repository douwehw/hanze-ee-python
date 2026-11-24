import random, csv
from typing import Literal, Any
import numpy as numpy
import matplotlib.pyplot as plt

random.seed(4)

def input_to_float(prompt: str) -> float:
	"""Get's user input and converts it to a data type of choice (float by default)"""
	while True:
			try:
				return float(input(prompt)) # Float by default
			except ValueError:
				print("Please enter a number...")

def get_user_input() -> tuple[Literal["1"], str, float, int, float, float, None] | tuple[Literal["2"], str, float, None, None, None, str]:
	"""Get's the user's input for all the variables to generate plots."""
	while True:
		reading_choice = input("Generate new readings (1), or load csv (2): ").strip()
		if reading_choice in ("1", "2"):
			break
		print("Please enter either 1 or 2.")

	sensor_type = input("What sensor type we measuring boss?\n>").strip()
	if not sensor_type:
		sensor_type = "placeholder sensor"

	threshold = input_to_float("What's the threshold value boss?\n>")

	if reading_choice == "1":
		while True:
			num_readings = int(input_to_float("How many readings boss?\n>"))
			if num_readings > 0:
				break
			print("You need at least 1 reading cuzzo")

		while True:
			min = input_to_float("Minimum value boss?\n>")
			max = input_to_float("Maximum value boss?\n>")
			if min < max:
				break
			print("The minimum gotta be bigger than the maximum, you understand that right boss?")
			while True:
				quick_question = input("Do you understand? (yes or no)\n>").strip()
				if quick_question == "yes":
					break
				print("you gotta say yes")
		return reading_choice, sensor_type, threshold, num_readings, min, max, None # Return everything but a filename

	filename = input("CSV file path boss?\n>").strip()
	return reading_choice, sensor_type, threshold, None, None, None, filename # Return only the semantic information, readings come from CSV

def generate_readings(num_readings: int, min: float, max: float) -> list[float]:
	"""Generates randomised dummy info for sensor readings"""
	return [random.uniform(min, max) for _ in range(num_readings)] # _ because we aren't accessing the variable

def calculate_statistics(readings: list[float])-> dict[str, Any]:
	"""Uses Numpy to return the count, mean, min, max, and standard deviation"""
	values = numpy.asarray(readings, dtype=float)
	return {
		"count": int(values.size),
		"mean": float(values.mean()),
		"min": float(values.min()),
		"max": float(values.max()),
		"standard_deviation": float(values.std())
	}

def detect_outliers(readings: list[float], threshold: float) -> list[tuple[int, Any]]:
	"""Detects any values in a reading that are above the threshold value"""
	return [
		(index, value)
		for index, value in enumerate(readings)
		if value > threshold
	]

def save_readings(filename: str, readings: list[float]) -> None:
	"""Writes the readings to a CSV file named `sensor_reading.csv`"""
	with open(filename, "w", newline="", encoding="utf-8") as file:
		writer = csv.writer(file)
		writer.writerow(["sample_number", "sensor_reading"])
		writer.writerows(
			(index, value)
			for index, value in enumerate(readings)
		)

def load_readings(filename: str)-> list[Any]:
	"""Loads readings from a CSV file. Searches by pathname so file extention is required"""
	readings = []
	with open(filename, "r", newline="", encoding="utf-8") as csvfile:
			reader = csv.DictReader(csvfile)
			if not reader.fieldnames or "sensor_reading" not in reader.fieldnames:
				raise ValueError("CSV must contain a 'sensor_reading' column.")
			for row_number, row in enumerate(reader, start=2):
				try:
					readings.append(float(row["sensor_reading"]))
				except (TypeError, ValueError):
					raise ValueError(f"Invalid sensor reading on CSV row {row_number}.")
	if not readings:
			raise ValueError("The CSV file contains no readings.")
	return readings

def plot_readings(readings: list[float], threshold: float, sensor_type: str) -> None:
	"""Plot a sensor's readings in a nice graph with a threshold line"""
	sample_numbers = numpy.arange(1, len(readings) + 1)
	plt.figure()
	plt.plot(sample_numbers, readings, label="Sensor Reading")
	plt.axhline(threshold, color="red", linestyle="dashed", label="Threshold")
	plt.title(f"{sensor_type} readings")
	plt.xlabel("Sample number")
	plt.ylabel(f"{sensor_type} value")
	plt.grid(True)
	plt.legend()

def plot_histogram(readings: list[float], sensor_type: str) -> None:
	"""Plots a sensor's reading in a nice histogram with bins that don't touch each other"""
	plt.figure()
	plt.hist(readings, bins=20, rwidth=0.75) # rwidth < 1 so the bins don't touch eachother
	plt.title(f"Distribution of {sensor_type} Readings")
	plt.xlabel(f"{sensor_type} value")
	plt.ylabel("Frequency")
	plt.grid(True)

def main() -> None:
	reading_choice, sensor_type, threshold, num_readings, min, max, filename = get_user_input()
	if (reading_choice) == "1" and num_readings is not None and min is not None and max is not None:
		readings = generate_readings(num_readings, min, max)
	else:
		if filename is not None:
			try:
				readings = load_readings(filename)
			except (OSError, ValueError) as error:
				print(f"Could not load readings: {error}")
				return

	statistics = calculate_statistics(readings)
	print(f"\n{sensor_type} statistics:")
	print(f"Number of readings: {statistics['count']}")
	print(f"Mean: {statistics['mean']:.2f}")
	print(f"Minimum: {statistics['min']:.2f}")
	print(f"Maximum value: {statistics['max']:.2f}")
	print(f"Standard deviation: {statistics['standard_deviation']:.2f}")

	outliers = detect_outliers(readings, threshold)
	print(f"There are {len(outliers)} readings above the threshold of {threshold}")
	if outliers:
		print("The readings in question (sample number, value):")
		for sample_num, value in outliers:
			print(f"{sample_num}\t{value:.2f}")
	else:
		print("None! There are no values above the threshold!")

	if reading_choice == "1":
		try:
			save_readings("sensor_readings.csv", readings)
			print("Saved readings to 'sensor_readings.csv")
		except OSError as error:
			print(f"Could not save readings to csv: {error}")

	plot_readings(readings, threshold, sensor_type)
	plot_histogram(readings, sensor_type)
	plt.show()

if __name__ == "__main__":
	main()

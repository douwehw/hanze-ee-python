import random, csv
import numpy as numpy
import matplotlib.pyplot as plt

random.seed(4)

def input_to_number(prompt, convert=float):
	while True:
			try:
				return convert(input(prompt))
			except ValueError:
				print("Please enter a number...")

def get_user_input():
	while True:
		reading_choice = input("Generate new readings (1), or load csv (2): ").strip()
		if reading_choice in ("1", "2"):
			break
		print("Please enter either 1 or 2.")

	sensor_type = input("What sensor type we measuring boss?\n>").strip()
	if not sensor_type:
		sensor_type = "placeholder sensor"

	threshold = input_to_number("What's the threshold value boss?\n>")

	if reading_choice == "1":
		while True:
			num_readings = input_to_number("How many readings boss?\n>", int)
			if num_readings > 0:
				break
			print("You need at least 1 reading cuzzo")

		while True:
			min = input_to_number("Minimum value boss?\n>")
			max = input_to_number("Maximum value boss?\n>")
			if min < max:
				break
			print("The minimum gotta be bigger than the maximum, you understand that right boss?")
			while True:
				quick_question = input("Do you understand? (yes or no)\n>").strip()
				if quick_question == "yes":
					break
				print("you gotta say yes")
		return reading_choice, sensor_type, threshold, num_readings, min, max, None

	filename = input("CSV file path boss?\n>").strip()
	return reading_choice, sensor_type, threshold, None, None, None, filename

def generate_readings(num_readings, min, max):
	return [random.uniform(min, max) for _ in range(num_readings)] # _ because we aren't accessing the variable

def calculate_statistics(readings):
	values = numpy.asarray(readings, dtype=float)
	return {
		"count": int(values.size),
		"mean": float(values.mean()),
		"min": float(values.min()),
		"max": float(values.max()),
		"standard_deviation": float(values.std())
	}

def detect_outliers(num_readings, threshold):
	return [
		(index, value)
		for index, value in enumerate(num_readings)
		if value > threshold
	]

def save_readings(filename, readings):
	with open(filename, "w", newline="", encoding="utf-8") as file:
		writer = csv.writer(file)
		writer.writerow(["sample_number", "sensor_reading"])
		writer.writerows(
			(index, value)
			for index, value in enumerate(readings)
		)

def load_readings(filename):
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

def plot_readings(readings, threshold, sensor_type):
	sample_numbers = numpy.arange(1, len(readings) + 1)
	plt.figure()
	plt.plot(sample_numbers, readings, label="Sensor Reading")
	plt.axhline(threshold, color="red", linestyle="dashed", label="Threshold")
	plt.title(f"{sensor_type} readings")
	plt.xlabel("Sample number")
	plt.ylabel(f"{sensor_type} value")
	plt.grid(True)
	plt.legend()

def plot_histogram(readings, sensor_type):
	plt.figure()
	plt.hist(readings, bins=20, rwidth=0.75)
	plt.title(f"Distribution of {sensor_type} Readings")
	plt.xlabel(f"{sensor_type} value")
	plt.ylabel("Frequency")
	plt.grid(True)

def main():
	reading_choice, sensor_type, threshold, num_readings, min, max, filename = get_user_input()
	if (reading_choice) == "1":
		readings = generate_readings(num_readings, min, max)
	else:
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

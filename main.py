import random

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
			num_readings = input_to_number("How many readings boss?\n>")
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

get_user_input()
print("I aint doing allat")

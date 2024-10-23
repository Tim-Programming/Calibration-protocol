import re
def create_dictionary_from_user_input(keys):
    # Define the keys for the dictionary entries
    #keys = ["U_anz", "U_ist"]
    # Initialize an empty list to store the measurement points
    measurement_points = []

    while True:
        # Create a new dictionary for each entry
        entry = {}
        for key in keys:
            # Prompt the user for the value corresponding to each key
            value = input(f"Enter the value for {key} (or 'exit' to quit): ")
            if value.lower() == 'exit':
                return measurement_points
            entry[key] = value
        # Append the entry to the list of measurement points
        measurement_points.append(entry)

    return measurement_points


def to_volt(value_str: str) -> float:
    # Remove whitespace
    value_str = value_str.strip()
    if "mV" in value_str and value_str.endswith("mV"):
        number = value_str[:-2].strip()
        return float(number) / 1000.0  # Convert mV to V
    elif "µV" in value_str and value_str.endswith("µV"):
        number = value_str[:-2].strip()
        return float(number) / 1e6  # Convert µV to V
    elif "V" in value_str and value_str.endswith("V"):
        number = value_str[:-1].strip()
        return float(number)  # No conversion needed
    else:
        raise ValueError(f"Unknown unit in '{value_str}'")

def volt_to_string(result, range_factor):
    # Format the result based on its magnitude
    if abs(result) >= 1/range_factor:
        result_str = f"{result:.3f} V"
    elif abs(result) >= 1e-3/range_factor:
        result_str = f"{result * 1000:.3f} mV"
    else:
        result_str = f"{result * 1e6:.3f} µV"

    return result_str

def extract_percentage_and_number(input_string):
    # Pattern to extract percentage and integer
    pattern = r'([\d\.]+)\s*%\s*\+\s*(\d+)'
    match = re.search(pattern, input_string)

    if match:
        percentage = float(match.group(1))/100  # Convert percentage to float
        number = int(match.group(2))  # Convert integer value
        return percentage, number
    else:
        return None


def calculate_measurement_error(u_anz: str, u_ref: str) -> str:
    """Calculates the measurement error of the device and returns it as a string with a unit."""

    # Convert to volts
    u_anz_volt = to_volt(u_anz)
    u_ref_volt = to_volt(u_ref)

    # Calculate the deviation
    deviation = u_anz_volt - u_ref_volt
    return volt_to_string(deviation, 1000)


def calculate_test_interval(u_ref, accuracy_percentage, digits):
    return False

def calculateAccuracy(u_anz, characteristics, output_range):
    u_anz = to_volt(u_anz)
    result = 0

    range_value = to_volt(characteristics[0]["range"])
    resolution = to_volt(characteristics[0]["resolution"])
    (percentage, digits) = extract_percentage_and_number(characteristics[0]["accuracy"])
    result = percentage * u_anz + digits * resolution

    index = 0
    while u_anz > range_value:
        if index >= len(characteristics):
            break  # Safe Backup
        range_value = to_volt(characteristics[index]["range"])
        resolution = to_volt(characteristics[index]["resolution"])
        (percentage, digits) = extract_percentage_and_number(characteristics[index]["accuracy"])
        result = percentage * u_anz + digits * resolution

        index += 1

    return volt_to_string(result, output_range)

def calculate_emax(u_anz, characteristics):
    return calculateAccuracy(u_anz, characteristics, 1)

def calculate_Uref(u_anz, characteristics):
    return calculateAccuracy(u_anz, characteristics, 1)


def perform_calibration(u_anz, u_ref):
    """Performs the calibration and returns the result."""
    deviation = calculate_measurement_error(u_anz, u_ref)
    return deviation


def calibration_report():
    print("Calibration report for Voltcraft VC 175\n")

    date = input("Enter the calibration date (e.g. 19.10.2024): ")
    device = input("Enter the type of device being tested (e.g. Voltcraft VC 175): ")
    reference = input("Enter the type of reference device (e.g. Agilent U3402A): ")

    # Measurement points and corresponding accuracy values (percentage and digits)
    measurement_points = [
        {"U_anz": "0.000 V", "U_ist": "0.000 mV"},
        {"U_anz": "0.100 V", "U_ist": "0.10097 V"},
        {"U_anz": "0.500 V", "U_ist": "0.50003 V"},
        {"U_anz": "1.000 V", "U_ist": "1.00016 V"},
        {"U_anz": "5.00 V", "U_ist": "4.8000 V"},
    ]

    #print("Enter the Measurement points")
    #keys_measure_points = ["U_anz", "U_ist"]
    # Call the function and store the result
    #measurement_points = create_dictionary_from_user_input(keys_measure_points)

    device_characteristics = [
        {"range": "4.000 V", "resolution": "1 mV", "accuracy": "0.8% + 8"},
        {"range": "40.00 V", "resolution": "10 mV", "accuracy": "0.8% + 8"},
        {"range": "400.00 V", "resolution": "100 mV", "accuracy": "0.8% + 8"},
        {"range": "600.00 V", "resolution": "1 V", "accuracy": "0.8% + 8"}
    ]

    # print("Enter the device characteristics")
    # keys_device_characteristics = ["range", "resolution", "accuracy"]
    # # Call the function and store the result
    # device_characteristics = create_dictionary_from_user_input(keys_device_characteristics)

    reference_characteristics = [
        {"range": "120.000 mV", "resolution": "1 µV", "accuracy": "0.012% + 8"},
        {"range": "1.20000 V", "resolution": "10 µV", "accuracy": "0.012% + 5"},
        {"range": "12.0000 V", "resolution": "100 µV", "accuracy": "0.012% + 5"},
        {"range": "120.000 V", "resolution": "1 mV", "accuracy": "0.012% + 5"},
        {"range": "1000.00 V", "resolution": "10 mV", "accuracy": "0.012% + 5"}
    ]

    # print("Enter the reference characteristics")
    # keys_reference_characteristics = ["range", "resolution", "accuracy"]
    # # Call the function and store the result
    # reference_characteristics = create_dictionary_from_user_input(keys_reference_characteristics)

    print("\nCalibration results:")
    print(f"Device: {device}\nReference device: {reference}\nDate: {date}\n")

    # Table header
    print(f"| {'ID':<12} | {'Device (U_anz)':<20} | {'Reference (U_ist)':<20} | "
          f"{'Measurement Deviation (e)':<25} | {'Allowed Interval (emax)':<25} | {'Uref':<25} | "
          f"{'Test Interval (±eprüf1)':<25} | {'Result':<15} |")
    print(f"|{'-' * 14}|{'-' * 22}|{'-' * 22}|{'-' * 27}|{'-' * 27}|{'-' * 27}|{'-' * 27}|{'-' * 17}|")

    for i, measurement_point in enumerate(measurement_points):
        u_anz = measurement_point["U_anz"]
        u_ist = measurement_point["U_ist"]

        deviation = perform_calibration(u_anz, u_ist)
        emax = calculate_emax(u_anz, device_characteristics)
        Uref = calculate_Uref(u_ist, reference_characteristics)
        epruef = abs(to_volt(emax)) - abs(to_volt(Uref))

        if to_volt(deviation) < epruef:
            result = "within limits"
        else:
            result = "out of limits"

        epruef = volt_to_string(epruef, 1)

        # Print results in table form
        print(f"| {str(i):<12} | {str(u_anz):<20} | {str(u_ist):<20} | {str(deviation):<25} | {str(emax):<25} | "
              f"{str(Uref):<25} | {str(epruef):<25} | {str(result):<15} |")

    print("\nCalibration complete.")
    print("Result: All measurement points checked.")


if __name__ == "__main__":
    calibration_report()

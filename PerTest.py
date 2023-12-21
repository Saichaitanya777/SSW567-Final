import json
import time
import csv
from MRTD import decode_mrz_line1, decode_mrz_line2, encodeMRZ  # Adjust based on your actual function names

def measure_execution_time_encode(process_function, records, num_records, document_type):
    start_time = time.time()
    for i in range(min(num_records, len(records['records_decoded']))):
        record = records['records_decoded'][i]
        # Extract fields from both line1 and line2 dictionaries
        line1 = record['line1']
        line2 = record['line2']

        # Prepare arguments for the encodeMRZ function
        issuing_country = line1['issuing_country']
        last_name = line1['last_name']
        given_name = line1['given_name']
        passport_number = line2['passport_number']
        country_code = line2['country_code']
        birth_date = line2['birth_date']
        sex = line2['sex']
        expiration_date = line2['expiration_date']
        personal_number = line2['personal_number']

        # Call the encodeMRZ function with the extracted arguments
        process_function(document_type, issuing_country, last_name, given_name, passport_number,
                         country_code, birth_date, sex, expiration_date, personal_number)
    end_time = time.time()
    return end_time - start_time

def measure_execution_time_decode(process_function, records, num_records):
    start_time = time.time()
    for i in range(min(num_records, len(records['records_encoded']))):
        record = records['records_encoded'][i]
        # Assuming that each record contains a single encoded MRZ line
        process_function(record)
    end_time = time.time()
    return end_time - start_time



def load_json_records(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Load encoded and decoded records
    encoded_records = load_json_records('records_encoded.json')
    decoded_records = load_json_records('records_decoded.json')

    document_type = "P"  # Assuming 'P' for passport; adjust as necessary

    ## encode & decode testing
    with open('performance_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number of lines read', 'Execution time for encoding', 'Execution time for decoding'])

        for num_records in range(100, 10001, 1000):
            # Measure execution time for decoding (using either decode_mrz_line1 or decode_mrz_line2)
            # Adjust the function used based on your specific needs
            exec_time_for_decoding = measure_execution_time_decode(decode_mrz_line1, encoded_records, num_records)
            # Measure execution time for encoding
            exec_time_for_encoding = measure_execution_time_encode(encodeMRZ, decoded_records, num_records, document_type)


            writer.writerow([num_records, exec_time_for_encoding, exec_time_for_decoding])

if __name__ == '__main__':
    main()

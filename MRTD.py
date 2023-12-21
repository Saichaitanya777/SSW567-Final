from mrz.checker.td3 import TD3CodeChecker
from mrz.generator.td3 import TD3CodeGenerator
from string import ascii_uppercase, digits
import iso3166

country_list = iso3166.countries_by_alpha3.keys()


# Function to scan MRZ (Placeholder)
def scan_mrz():
    pass


# Function to validate MRZ details
def validateMRZ(encoded_mrz):
    try:
        return bool(TD3CodeChecker(encoded_mrz))
    except Exception as err:
        return False


def decode_mrz_line1(encoded_mrz_line1):
    """
    Decodes the first line of the MRZ.
    """
    #document_type = encoded_mrz_line1[0:1]
    country = encoded_mrz_line1[2:5]
    name_field = encoded_mrz_line1[5:44].replace('<', ' ').strip().split('  ')
    last_name = name_field[0].strip()
    given_names = ' '.join(name_field[1:]).strip()

    return {
        #"document_type": document_type,
        "issuing_country": country,
        "last_name": last_name,
        "given_name": given_names
    }


# Function to decode MRZ Line 2
def decode_mrz_line2(encoded_mrz_line2):
    """
    Decodes the second line of the MRZ.
    """
    passport_number = encoded_mrz_line2[0:9]
    nationality = encoded_mrz_line2[10:13]
    birth_date = encoded_mrz_line2[13:19]
    sex = encoded_mrz_line2[20]
    expiration_date = encoded_mrz_line2[21:27]
    personal_number = encoded_mrz_line2[28:37]

    return {
        "passport_number": passport_number,
        "nationality": nationality,
        "birth_date": birth_date,
        "sex": sex,
        "expiration_date": expiration_date,
        "personal_number": personal_number
    }


def calculate_check_digit(input_string: str):
    valid_characters = digits + ascii_uppercase
    formatted_string = input_string.upper().replace("<", "0")
    weights = [7, 3, 1]

    checksum_total = 0
    for index, character in enumerate(formatted_string):
        if character not in valid_characters:
            raise ValueError(f"Invalid character '{character}' in input string.")
        character_value = valid_characters.index(character)
        checksum_total += character_value * weights[index % 3]
    return checksum_total % 10


# Function for encoding the lines
def encodeMRZ(document_type, issuing_country, last_name, given_name, passport_number,
              country_code, birth_date, sex, expiration_date, personal_number):
    try:
        encoded_mrz = TD3CodeGenerator(document_type, issuing_country, last_name, given_name, passport_number,
                                       country_code, birth_date, sex, expiration_date, personal_number)
        full_mrz = encoded_mrz.__str__()
        # Splitting the MRZ into two lines
        line1, line2 = full_mrz.split('\n')
        return line1, line2
    except Exception as err:
        # Handling specific errors and providing appropriate messages
        if err.args[0].startswith('String was not recognized as a valid country code'):
            if issuing_country != country_code:
                return "issuing_country not equal to country_code", None
            if issuing_country not in country_list:
                return "illegal issuing_country", None
        return str(err), None


def verify_checkdigits(mrz_line2, passport_number, birth_date, expiration_date, personal_number):
    # Calculating check digits for each part
    check_digits = [str(calculate_check_digit(passport_number)),
                    str(calculate_check_digit(birth_date)),
                    str(calculate_check_digit(expiration_date)),
                    str(calculate_check_digit(personal_number))]

    # Corresponding positions in the MRZ line
    check_positions = [9, 19, 27, 43]

    # Corresponding error messages
    error_messages = ["Incorrect Passport check digit!",
                      "Incorrect birth date check digit!",
                      "Incorrect Passport expiration date check digit!",
                      "Incorrect personal number check digit!"]

    # Check each part against its corresponding MRZ line position
    for check_digit, position, error_message in zip(check_digits, check_positions, error_messages):
        if mrz_line2[position] != check_digit:
            return error_message

    return "Check Digits are correct"


if __name__ == "__main__":
    scan_mrz()

    # Encode MRZ
    line1, line2 = encodeMRZ("P", "REU", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M", "690413",
                             "UK128819I")
    print("Encoded Line 1:", line1)
    print("Encoded Line 2:", line2)

    # Decode example MRZ lines and print decoded information
    example_line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
    example_line2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<10"
    print("Decoded Line 1:", decode_mrz_line1(example_line1))
    print("Decoded Line 2:", decode_mrz_line2(example_line2))

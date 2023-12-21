import unittest
from unittest.mock import patch
import MRTD


class TestMRTDModule(unittest.TestCase):

    @patch('MRTD.scan_mrz')
    def test_scan_mrz(self, mock_scan_mrz):
        mock_scan_mrz.return_value = 'Mocked MRZ Data'
        self.assertEqual(MRTD.scan_mrz(), 'Mocked MRZ Data')

    def test_validate_mrz_valid(self):
        valid_mrz = 'P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\nL898902C36UTO7408122F1204159ZE184226B<<<<<10'
        self.assertTrue(MRTD.validateMRZ(valid_mrz))

    def test_validate_mrz_invalid(self):
        invalid_mrz = 'InvalidMRZString'
        self.assertFalse(MRTD.validateMRZ(invalid_mrz))

    def test_decode_mrz_line1(self):
        line1 = 'P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<'
        expected_output = {
            "document_type": "P",
            "issuing_country": "UTO",
            "last_name": "ERIKSSON",
            "given_name": "ANNA MARIA"
        }
        self.assertEqual(MRTD.decode_mrz_line1(line1), expected_output)

    def test_decode_mrz_line2(self):
        line2 = 'L898902C36UTO7408122F1204159ZE184226B<<<<<10'
        expected_output = {
            "passport_number": "L898902C3",
            "nationality": "UTO",
            "birth_date": "740812",
            "sex": "F",
            "expiration_date": "120415",
            "personal_number": "ZE184226B"
        }
        self.assertEqual(MRTD.decode_mrz_line2(line2), expected_output)

    def test_encode_mrz(self):
        line1, line2 = MRTD.encodeMRZ("P", "REU", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M",
                                      "690413", "UK128819I")
        self.assertTrue(line1.startswith('P<REU'))
        self.assertTrue(line2.startswith('Q683170H1'))

    def test_successful_MRZ_encoding(self):
        self.assertEqual(
            MRTD.encodeMRZ("P", "REU", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M", "690413",
                           "UK128819I"),
            ('P<REUMCFARLAND<<TRINITY<AMITY<<<<<<<<<<<<<<<','Q683170H11REU6403131M6904133UK128819I<<<<<94'))

    def test_wrong_country_code_encoding(self):
        self.assertEqual(
            MRTD.encodeMRZ("P", "ABC", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M", "690413",
                           "UK128819I"),
            ('issuing_country not equal to country_code', None))


    def test_verify_checkdigits_incorrect(self):
        self.assertNotEqual(
            MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<10", "L898902C3", "740812", "120415",
                                    "WRONG"), "Check Digits are correct")

    def test_calculate_check_digit_special_chars(self):
        # Testing with special characters which are not part of MRZ standard
        with self.assertRaises(ValueError):
            MRTD.calculate_check_digit('!@#')

    def test_valid_input(self):
        input_string = "AB123"
        expected_check_digit = 7
        self.assertEqual(MRTD.calculate_check_digit(input_string), expected_check_digit)


    def test_decode_mrz_line1_valid(self):
        valid_mrz_line1 = 'P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<'
        expected_result = {'document_type': 'P', 'issuing_country': 'UTO', 'last_name': 'ERIKSSON',
                           'given_name': 'ANNA MARIA'}
        self.assertEqual(MRTD.decode_mrz_line1(valid_mrz_line1), expected_result)

    def test_decode_mrz_line1_invalid(self):
        invalid_mrz_line1 = 'InvalidLine1Data'
        result = MRTD.decode_mrz_line1(invalid_mrz_line1)
        expected_result = {'document_type': 'I', 'issuing_country': 'val', 'last_name': 'idLine1Data', 'given_name': ''}
        self.assertEqual(result, expected_result)

    def test_incorrect_personal_number_check_digit(self):
        self.assertEqual(MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<10", "L898902C3", "740812",
                                                 "120415", "ZE184226B"), 'Incorrect personal number check digit!')

    def test_correct_check_digits(self):
        self.assertEqual(MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<<1", "L898902C3", "740812",
                                                 "120415", "ZE184226B"), "Check Digits are correct")

    def test_incorrect_birth_date_check_digit(self):
        self.assertEqual(MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<<10", "L898902C3", "74081",
                                                 "120415", "ZE184226B"), "Incorrect birth date check digit!")

    class TestCalculateCheckDigit(unittest.TestCase):

        def test_invalid_character_error(self):
            # Test to ensure that an invalid character causes a ValueError
            invalid_input = "AB12#3"  # Including a character '#' that's not in digits or ascii_uppercase
            with self.assertRaises(ValueError):
               MRTD.calculate_check_digit(invalid_input)

if __name__ == '__main__':
    unittest.main()

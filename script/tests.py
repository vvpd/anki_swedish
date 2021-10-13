import os
import unittest

# Imports to test
from sanitize import Sanitizer

class TestSanitize(unittest.TestCase):
    def setUp(self):
        self.sanitizer = Sanitizer("sv", "de", os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'ignores.json'))

    def test_object_duplicate(self):
        self.assertTrue(self.sanitizer.is_object_duplicate('Jag är hungrig', 'Jag är hungrig'))
        self.assertTrue(self.sanitizer.is_object_duplicate('Jag är hungrig', 'Du är hungrig'))
        self.assertTrue(self.sanitizer.is_object_duplicate('Jag är hungrig.', 'Du är hungrig'))
        self.assertTrue(self.sanitizer.is_object_duplicate('Du älskar henne', 'Vi älskar er'))
        self.assertFalse(self.sanitizer.is_object_duplicate('Du älskar henne', 'Huset är gammalt'))

    def test_id_duplicate(self):
        self.assertTrue(self.sanitizer.is_id_duplicate('1234', '1234'))
        self.assertTrue(self.sanitizer.is_id_duplicate(1234, 1234))
        self.assertTrue(self.sanitizer.is_id_duplicate('1234', 1234))
        self.assertFalse(self.sanitizer.is_id_duplicate(1237,32112))

    def test_too_short(self):
        self.assertTrue(self.sanitizer.is_too_short('Jag är hungrig'))
        self.assertTrue(self.sanitizer.is_too_short('Mormor var gammal'))
        self.assertTrue(self.sanitizer.is_too_short('Pappa har läst min bok'))
        self.assertFalse(self.sanitizer.is_too_short('Det här är en ganska lång mening'))

    def test_too_long(self):
        self.assertTrue(self.sanitizer.is_too_long('Det här är en ganska lång mening och det finns även en bisatz som gör den även längre'))
        self.assertFalse(self.sanitizer.is_too_long('Det här är en bra mening'))

    def test_too_boring(self):
        self.assertTrue(self.sanitizer.is_too_boring('Din mamma älskar dig väldigt mycket'))
        self.assertFalse(self.sanitizer.is_too_boring('Varför behöver du småpengar?'))

if __name__ == '__main__':
    unittest.main()

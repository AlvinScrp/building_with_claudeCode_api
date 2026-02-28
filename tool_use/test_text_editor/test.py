import unittest
from main import add


class TestAddFunction(unittest.TestCase):
    """测试 add 函数的单元测试"""
    
    def test_add_positive_numbers(self):
        """测试两个正数相加"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, 20), 30)
    
    def test_add_negative_numbers(self):
        """测试两个负数相加"""
        self.assertEqual(add(-5, -3), -8)
        self.assertEqual(add(-10, -20), -30)
    
    def test_add_mixed_numbers(self):
        """测试正负数混合相加"""
        self.assertEqual(add(5, -3), 2)
        self.assertEqual(add(-5, 3), -2)
    
    def test_add_zero(self):
        """测试与零相加"""
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, 5), 5)
    
    def test_add_floats(self):
        """测试浮点数相加"""
        self.assertAlmostEqual(add(2.5, 3.7), 6.2)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


if __name__ == '__main__':
    unittest.main()

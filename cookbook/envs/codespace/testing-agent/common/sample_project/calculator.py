"""
简单计算器模块
包含基本的数学运算函数，用于演示测试用例的编写
"""

class Calculator:
    """计算器类，提供基本的数学运算功能"""
    
    def add(self, a, b):
        """
        计算两个数的和
        
        Args:
            a (int/float): 第一个数
            b (int/float): 第二个数
        
        Returns:
            int/float: 两个数的和
        """
        return a + b

    def subtract(self, a, b):
        """
        计算两个数的差
        
        Args:
            a (int/float): 被减数
            b (int/float): 减数
        
        Returns:
            int/float: 两个数的差
        """
        return a - b

    def multiply(self, a, b):
        """
        计算两个数的积
        
        Args:
            a (int/float): 第一个数
            b (int/float): 第二个数
        
        Returns:
            int/float: 两个数的积
        """
        return a * b

    def divide(self, a, b):
        """
        计算两个数的商
        
        Args:
            a (int/float): 被除数
            b (int/float): 除数
        
        Returns:
            float: 两个数的商
        
        Raises:
            ValueError: 当除数为0时抛出异常
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


def add(a, b):
    """
    计算两个数的和
    
    Args:
        a (int/float): 第一个数
        b (int/float): 第二个数
    
    Returns:
        int/float: 两个数的和
    """
    return a + b

def subtract(a, b):
    """
    计算两个数的差
    
    Args:
        a (int/float): 被减数
        b (int/float): 减数
    
    Returns:
        int/float: 两个数的差
    """
    return a - b

def multiply(a, b):
    """
    计算两个数的积
    
    Args:
        a (int/float): 第一个数
        b (int/float): 第二个数
    
    Returns:
        int/float: 两个数的积
    """
    return a * b

def divide(a, b):
    """
    计算两个数的商
    
    Args:
        a (int/float): 被除数
        b (int/float): 除数
    
    Returns:
        float: 两个数的商
    
    Raises:
        ZeroDivisionError: 当除数为0时抛出异常
    """
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b

def is_even(number):
    """
    判断一个数是否为偶数
    
    Args:
        number (int): 待判断的数
    
    Returns:
        bool: 如果是偶数返回True，否则返回False
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer")
    return number % 2 == 0

if __name__ == "__main__":
    # 简单的演示
    calc = Calculator()
    print("使用Calculator类:")
    print("加法: 3 + 5 =", calc.add(3, 5))
    print("减法: 10 - 3 =", calc.subtract(10, 3))
    print("乘法: 4 * 6 =", calc.multiply(4, 6))
    print("除法: 15 / 3 =", calc.divide(15, 3))
    
    print("\n使用独立函数:")
    print("加法: 3 + 5 =", add(3, 5))
    print("减法: 10 - 3 =", subtract(10, 3))
    print("乘法: 4 * 6 =", multiply(4, 6))
    print("除法: 15 / 3 =", divide(15, 3))
    print("判断偶数: 4是偶数吗?", is_even(4))
    print("判断偶数: 5是偶数吗?", is_even(5))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行脚本
用于运行项目中的各类测试
"""

import os
import sys
import subprocess


def run_unit_tests():
    """运行单元测试"""
    print("运行单元测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/unit", "-v"
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行单元测试时出错: {e}")
        return False


def run_integration_tests():
    """运行集成测试"""
    print("运行集成测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/integration", "-v"
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行集成测试时出错: {e}")
        return False


def run_utils_tests():
    """运行工具测试"""
    print("运行工具测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/utils", "-v"
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行工具测试时出错: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("运行所有测试...")
    success = True
    
    # 运行各类测试
    test_functions = [
        ("单元测试", run_unit_tests),
        ("集成测试", run_integration_tests),
        ("工具测试", run_utils_tests)
    ]
    
    for test_name, test_func in test_functions:
        print(f"\n{'='*50}")
        print(f"运行 {test_name}")
        print('='*50)
        
        if not test_func():
            success = False
    
    if success:
        print("\n所有测试运行完成！")
    else:
        print("\n部分测试失败，请检查错误信息。")
    
    return success


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == "unit":
            run_unit_tests()
        elif test_type == "integration":
            run_integration_tests()
        elif test_type == "utils":
            run_utils_tests()
        else:
            print("用法: python run_tests.py [unit|integration|utils|all]")
    else:
        run_all_tests()
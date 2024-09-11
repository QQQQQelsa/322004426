import pytest
import main
from main import short_analyse, long_ans, simhash_demo, save_data
import os
import argparse

# 命令行参数解析
def parse_arguments():
    parser = argparse.ArgumentParser(description="命令行输入文件路径进行相似度测试")
    parser.add_argument('o_file', type=str, help='原文文件的绝对路径')
    parser.add_argument('c_file', type=str, help='抄袭文件的绝对路径')
    parser.add_argument('output_file', type=str, help='输出结果文件的绝对路径')
    return parser.parse_args()

def test_short_analyse(o_file, c_file):
    """测试 short_analyse 函数的相似度"""
    result = short_analyse(o_file, c_file)
    assert 0 <= result <= 1, "短文本相似度应在 0 到 1 之间"
    print(f"短文本相似度: {result}")


def test_long_ans(o_file, c_file):
    """测试 long_ans 函数的相似度"""
    result = long_ans(o_file, c_file)
    assert 0 <= result <= 1, "长文本相似度应在 0 到 1 之间"
    print(f"长文本相似度: {result}")


def test_simhash_demo(o_file, c_file):
    """测试 simhash_demo 函数的相似度"""
    result = simhash_demo(o_file, c_file)
    assert 0 <= result <= 1, "Simhash 相似度应在 0 到 1 之间"
    print(f"Simhash 相似度: {result}")


def test_save_data(o_file, c_file, output_file):
    """测试 save_data 函数，并验证数据正确写入文件"""
    short_similarity = short_analyse(o_file, c_file)
    long_similarity = long_ans(o_file, c_file)
    simhash_similarity = simhash_demo(o_file, c_file)

    # 保存到文件
    save_data(output_file, short_similarity, long_similarity, simhash_similarity, o_file, c_file)

    # 验证文件内容是否正确
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "短文本分析的相似度为" in content
        assert "长文本分析的相似度为" in content
        assert "Simhash分析的相似度为" in content
        print(f"文件 {output_file} 写入成功，内容为：\n{content}")


if __name__ == '__main__':
    # 解析命令行参数
    args = parse_arguments()

    # 获取文件路径
    o_file = args.o_file
    c_file = args.c_file
    output_file = args.output_file

    # 运行测试
    print("=== 开始测试短文本相似度 ===")
    test_short_analyse(o_file, c_file)

    print("=== 开始测试长文本相似度 ===")
    test_long_ans(o_file, c_file)

    print("=== 开始测试Simhash相似度 ===")
    test_simhash_demo(o_file, c_file)

    print("=== 开始测试保存数据到文件 ===")
    test_save_data(o_file, c_file, output_file)

    print("所有测试完成！")


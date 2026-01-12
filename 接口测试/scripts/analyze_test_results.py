#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析意图识别测试结果，生成详细报告"""

import csv
from collections import defaultdict, Counter
import json
from datetime import datetime
import argparse
import os

def load_test_data(csv_file):
    """加载测试数据，建立索引"""
    test_data = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            description = row.get('description', '')
            if description:
                test_data[description] = row
    return test_data

def extract_text_from_history(history_str):
    """从history字段中提取text值"""
    try:
        history = json.loads(history_str)
        if history and isinstance(history, list) and len(history) > 0:
            first_item = history[0]
            if isinstance(first_item, dict) and 'text' in first_item:
                return first_item['text']
    except:
        pass
    return ''

def analyze_jtl_file(jtl_file, test_data):
    """分析 JTL 结果文件"""
    results = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'url': '',
        'port': '',
        'by_intent': defaultdict(lambda: {'total': 0, 'success': 0, 'failed': 0, 'failures': []}),
        'by_emotion': defaultdict(lambda: {'total': 0, 'success': 0, 'failed': 0, 'failures': []}),
        'failure_types': defaultdict(list),
        'failed_cases': [],
        'response_times': [],
        'success_response_times': [],
        'failed_response_times': []
    }
    
    with open(jtl_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 提取URL和端口信息（从第一条记录中获取）
            if not results['url'] and 'URL' in row:
                url = row['URL']
                results['url'] = url
                # 从URL中提取端口号
                if ':' in url:
                    try:
                        port = url.split(':')[-1].split('/')[0]
                        results['port'] = port
                    except:
                        pass
            
            results['total'] += 1
            
            # 收集响应时间
            response_time = int(row.get('elapsed', 0))
            results['response_times'].append(response_time)
            
            # 提取意图和情绪信息
            label = row['label']
            success = row['success'] == 'true'
            
            # 从测试数据中获取对应的输入文本
            input_text = ''
            if label in test_data:
                history = test_data[label].get('history', '')
                input_text = extract_text_from_history(history)
            
            # 解析标签中的意图和情绪
            if 'SEARCH' in label:
                intent = 'SEARCH'
            elif 'CHAT' in label:
                intent = 'CHAT'
            elif 'MEMORY' in label:
                intent = 'MEMORY'
            elif 'RECOMMEND' in label:
                intent = 'RECOMMEND'
            elif 'VISION' in label:
                intent = 'VISION'
            else:
                intent = 'UNKNOWN'
            
            # 提取预期情绪
            if '-开心' in label:
                expected_emotion = '开心'
            elif '-愤怒' in label:
                expected_emotion = '愤怒'
            elif '-悲伤' in label:
                expected_emotion = '悲伤'
            elif '-关切' in label:
                expected_emotion = '关切'
            elif '-疑问' in label:
                expected_emotion = '疑问'
            elif '-惊奇' in label:
                expected_emotion = '惊奇'
            elif '-厌恶' in label:
                expected_emotion = '厌恶'
            elif '-平淡' in label:
                expected_emotion = '平淡'
            else:
                expected_emotion = 'UNKNOWN'
            
            results['by_intent'][intent]['total'] += 1
            results['by_emotion'][expected_emotion]['total'] += 1
            
            if success:
                results['success'] += 1
                results['by_intent'][intent]['success'] += 1
                results['by_emotion'][expected_emotion]['success'] += 1
                results['success_response_times'].append(response_time)
            else:
                results['failed'] += 1
                results['by_intent'][intent]['failed'] += 1
                results['by_emotion'][expected_emotion]['failed'] += 1
                results['failed_response_times'].append(response_time)
                
                # 记录失败原因
                failure_message = row.get('failureMessage', '')
                if 'Label mismatch' in failure_message:
                    results['failure_types']['意图标签不匹配'].append({
                        'label': label,
                        'message': failure_message,
                        'response_code': row['responseCode']
                    })
                elif 'Emotion mismatch' in failure_message:
                    results['failure_types']['情绪不匹配'].append({
                        'label': label,
                        'message': failure_message,
                        'response_code': row['responseCode']
                    })
                elif 'HTTP状态码' in failure_message:
                    results['failure_types']['HTTP状态码不符'].append({
                        'label': label,
                        'message': failure_message,
                        'response_code': row['responseCode']
                    })
                else:
                    results['failure_types']['其他错误'].append({
                        'label': label,
                        'message': failure_message,
                        'response_code': row['responseCode']
                    })
                
                # 记录失败用例
                results['failed_cases'].append({
                    'label': label,
                    'intent': intent,
                    'expected_emotion': expected_emotion,
                    'failure_message': failure_message,
                    'response_code': row['responseCode'],
                    'response_time': row['elapsed'],
                    'input_text': input_text
                })
    
    return results

def calculate_response_time_stats(response_times):
    """计算响应时间统计指标"""
    if not response_times:
        return {
            'min': 0,
            'max': 0,
            'avg': 0,
            'p50': 0,
            'p90': 0,
            'p95': 0,
            'p99': 0
        }
    
    sorted_times = sorted(response_times)
    n = len(sorted_times)
    
    def percentile(p):
        """计算百分位数"""
        index = int(n * p / 100)
        if index >= n:
            index = n - 1
        return sorted_times[index]
    
    return {
        'min': min(response_times),
        'max': max(response_times),
        'avg': sum(response_times) / n,
        'p50': percentile(50),
        'p90': percentile(90),
        'p95': percentile(95),
        'p99': percentile(99)
    }

def generate_report(results, output_file, test_data):
    """生成详细报告"""
    report = []
    report.append("# 意图识别接口测试结果分析报告")
    report.append(f"\n**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 添加URL和端口信息
    if results['url']:
        report.append(f"**测试URL**: {results['url']}")
    if results['port']:
        report.append(f"**测试端口**: {results['port']}")
    
    report.append(f"**测试用例总数**: {results['total']}")
    report.append(f"**成功用例数**: {results['success']}")
    report.append(f"**失败用例数**: {results['failed']}")
    report.append(f"**通过率**: {results['success']/results['total']*100:.2f}%")
    report.append(f"**失败率**: {results['failed']/results['total']*100:.2f}%")
    
    # 响应时间统计
    report.append("\n## 响应时间统计")
    
    # 总体响应时间统计
    overall_stats = calculate_response_time_stats(results['response_times'])
    report.append("\n### 总体响应时间")
    report.append("| 指标 | 数值 |")
    report.append("|------|------|")
    report.append(f"| 最小值 | {overall_stats['min']} ms |")
    report.append(f"| 最大值 | {overall_stats['max']} ms |")
    report.append(f"| 平均值 | {overall_stats['avg']:.2f} ms |")
    report.append(f"| 中位数 (P50) | {overall_stats['p50']} ms |")
    report.append(f"| 90分位 (P90) | {overall_stats['p90']} ms |")
    report.append(f"| 95分位 (P95) | {overall_stats['p95']} ms |")
    report.append(f"| 99分位 (P99) | {overall_stats['p99']} ms |")
    
    # 成功用例响应时间统计
    success_stats = calculate_response_time_stats(results['success_response_times'])
    report.append("\n### 成功用例响应时间")
    report.append("| 指标 | 数值 |")
    report.append("|------|------|")
    report.append(f"| 最小值 | {success_stats['min']} ms |")
    report.append(f"| 最大值 | {success_stats['max']} ms |")
    report.append(f"| 平均值 | {success_stats['avg']:.2f} ms |")
    report.append(f"| 中位数 (P50) | {success_stats['p50']} ms |")
    report.append(f"| 90分位 (P90) | {success_stats['p90']} ms |")
    report.append(f"| 95分位 (P95) | {success_stats['p95']} ms |")
    report.append(f"| 99分位 (P99) | {success_stats['p99']} ms |")
    
    # 失败用例响应时间统计
    failed_stats = calculate_response_time_stats(results['failed_response_times'])
    report.append("\n### 失败用例响应时间")
    report.append("| 指标 | 数值 |")
    report.append("|------|------|")
    report.append(f"| 最小值 | {failed_stats['min']} ms |")
    report.append(f"| 最大值 | {failed_stats['max']} ms |")
    report.append(f"| 平均值 | {failed_stats['avg']:.2f} ms |")
    report.append(f"| 中位数 (P50) | {failed_stats['p50']} ms |")
    report.append(f"| 90分位 (P90) | {failed_stats['p90']} ms |")
    report.append(f"| 95分位 (P95) | {failed_stats['p95']} ms |")
    report.append(f"| 99分位 (P99) | {failed_stats['p99']} ms |")
    
    # 按意图分类统计
    report.append("\n## 一、按意图分类统计")
    report.append("\n| 意图类型 | 总数 | 成功 | 失败 | 通过率 | 失败率 |")
    report.append("|---------|------|------|------|--------|--------|")
    
    for intent in ['SEARCH', 'CHAT', 'MEMORY', 'RECOMMEND', 'VISION']:
        data = results['by_intent'][intent]
        if data['total'] > 0:
            success_rate = data['success']/data['total']*100
            fail_rate = data['failed']/data['total']*100
            report.append(f"| {intent} | {data['total']} | {data['success']} | {data['failed']} | {success_rate:.2f}% | {fail_rate:.2f}% |")
    
    # 按情绪分类统计
    report.append("\n## 二、按情绪分类统计")
    report.append("\n| 情绪类型 | 总数 | 成功 | 失败 | 通过率 | 失败率 |")
    report.append("|---------|------|------|------|--------|--------|")
    
    emotions = ['开心', '愤怒', '悲伤', '关切', '疑问', '惊奇', '厌恶', '平淡']
    for emotion in emotions:
        data = results['by_emotion'][emotion]
        if data['total'] > 0:
            success_rate = data['success']/data['total']*100
            fail_rate = data['failed']/data['total']*100
            report.append(f"| {emotion} | {data['total']} | {data['success']} | {data['failed']} | {success_rate:.2f}% | {fail_rate:.2f}% |")
    
    # 失败类型分析
    report.append("\n## 三、失败类型分析")
    for fail_type, cases in results['failure_types'].items():
        report.append(f"\n### {fail_type} ({len(cases)} 个)")
        report.append(f"**占比**: {len(cases)/results['failed']*100:.2f}%")
        
        # 显示前 10 个失败用例
        report.append("\n**失败用例示例**（前10个）:")
        report.append("| 序号 | 用例标签 | 输入内容 | 失败原因 | 响应码 |")
        report.append("|------|---------|---------|---------|--------|")
        
        for i, case in enumerate(cases[:10], 1):
            # 查找对应的输入文本
            input_text = ''
            if case['label'] in test_data:
                history = test_data[case['label']].get('history', '')
                input_text = extract_text_from_history(history)
            
            # 截断过长的文本
            if len(input_text) > 50:
                input_text = input_text[:47] + '...'
            
            report.append(f"| {i} | {case['label']} | {input_text} | {case['message']} | {case['response_code']} |")
    
    # 详细失败用例列表
    report.append("\n## 四、详细失败用例列表")
    for i, case in enumerate(results['failed_cases'], 1):
        report.append(f"\n### 用例 {i}: {case['label']}")
        report.append(f"- **意图**: {case['intent']}")
        report.append(f"- **预期情绪**: {case['expected_emotion']}")
        report.append(f"- **输入内容**: {case['input_text']}")
        report.append(f"- **失败原因**: {case['failure_message']}")
        report.append(f"- **响应码**: {case['response_code']}")
        report.append(f"- **响应时间**: {case['response_time']}ms")
    
    # 问题分析与建议
    report.append("\n## 五、问题分析与建议")
    
    # 分析情绪不匹配问题
    emotion_mismatches = results['failure_types'].get('情绪不匹配', [])
    if emotion_mismatches:
        report.append("\n### 情绪不匹配问题")
        report.append(f"**数量**: {len(emotion_mismatches)} 个")
        report.append(f"**占比**: {len(emotion_mismatches)/results['failed']*100:.2f}%")
        
        # 统计最常见的情绪不匹配模式
        emotion_patterns = Counter()
        for case in emotion_mismatches:
            message = case['message']
            if 'Expected:' in message and 'Actual:' in message:
                try:
                    expected = message.split('Expected:')[1].split(',')[0].strip()
                    actual = message.split('Actual:')[1].strip()
                    pattern = f"{expected} -> {actual}"
                    emotion_patterns[pattern] += 1
                except:
                    pass
        
        if emotion_patterns:
            report.append("\n**最常见的情绪不匹配模式**:")
            for pattern, count in emotion_patterns.most_common(10):
                report.append(f"- {pattern}: {count} 次")
        
        report.append("\n**可能原因**:")
        report.append("1. 情绪识别模型对某些表达方式的理解与预期不一致")
        report.append("2. 测试数据中的情绪标注可能存在偏差")
        report.append("3. 模型对上下文的理解可能影响情绪判断")
        
        report.append("\n**建议**:")
        report.append("1. 重新审视情绪不匹配的测试用例，确认预期情绪是否合理")
        report.append("2. 收集更多真实场景的情绪标注数据，提高标注质量")
        report.append("3. 考虑优化情绪识别模型，提高对特定表达方式的识别准确率")
    
    # 分析意图标签不匹配问题
    label_mismatches = results['failure_types'].get('意图标签不匹配', [])
    if label_mismatches:
        report.append("\n### 意图标签不匹配问题")
        report.append(f"**数量**: {len(label_mismatches)} 个")
        report.append(f"**占比**: {len(label_mismatches)/results['failed']*100:.2f}%")
        
        # 统计最常见的意图不匹配模式
        label_patterns = Counter()
        for case in label_mismatches:
            message = case['message']
            if 'Expected:' in message and 'Actual:' in message:
                try:
                    expected = message.split('Expected:')[1].split(',')[0].strip()
                    actual = message.split('Actual:')[1].strip()
                    pattern = f"{expected} -> {actual}"
                    label_patterns[pattern] += 1
                except:
                    pass
        
        if label_patterns:
            report.append("\n**最常见的意图不匹配模式**:")
            for pattern, count in label_patterns.most_common(10):
                report.append(f"- {pattern}: {count} 次")
        
        report.append("\n**可能原因**:")
        report.append("1. 意图识别的边界定义不够清晰，导致某些用例的意图归类存在歧义")
        report.append("2. 模型对某些特定表达方式的理解与预期意图不一致")
        report.append("3. 测试数据中的意图标注可能存在偏差")
        
        report.append("\n**建议**:")
        report.append("1. 重新审视意图不匹配的测试用例，确认预期意图是否合理")
        report.append("2. 明确各意图类型的边界定义，减少歧义")
        report.append("3. 收集更多真实场景的意图标注数据，提高标注质量")
        report.append("4. 考虑优化意图识别模型，提高对特定表达方式的识别准确率")
    
    # 分析 HTTP 状态码问题
    http_errors = results['failure_types'].get('HTTP状态码不符', [])
    if http_errors:
        report.append("\n### HTTP 状态码不符问题")
        report.append(f"**数量**: {len(http_errors)} 个")
        report.append(f"**占比**: {len(http_errors)/results['failed']*100:.2f}%")
        
        report.append("\n**可能原因**:")
        report.append("1. 测试数据设计存在缺陷，预期状态码设置不合理")
        report.append("2. 接口对某些异常情况的处理逻辑与预期不符")
        
        report.append("\n**建议**:")
        report.append("1. 重新审视 HTTP 状态码不符的测试用例，确认预期状态码是否合理")
        report.append("2. 检查接口对异常情况的处理逻辑是否符合预期")
    
    # 总体建议
    report.append("\n## 六、总体建议")
    report.append("\n### 短期优化建议")
    report.append("1. **优先处理情绪不匹配问题**: 情绪不匹配占失败用例的比例较高，建议优先解决")
    report.append("2. **重新审视意图边界定义**: 意图标签不匹配问题表明意图边界定义需要更清晰")
    report.append("3. **优化测试数据**: 根据测试结果，调整测试数据中的预期情绪和意图标注")
    
    report.append("\n### 长期优化建议")
    report.append("1. **建立持续测试机制**: 定期执行测试，跟踪模型性能变化")
    report.append("2. **收集更多真实数据**: 收集更多真实场景的对话数据，提高测试数据的代表性")
    report.append("3. **优化模型训练**: 根据测试结果，针对性地优化模型训练数据和算法")
    report.append("4. **建立测试数据管理机制**: 建立测试数据的版本管理和更新机制")
    
    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='分析意图识别测试结果，生成详细报告')
    parser.add_argument('--jtl-file', type=str, help='JTL结果文件路径')
    parser.add_argument('--data-file', type=str, help='测试数据CSV文件路径')
    parser.add_argument('--output', type=str, help='输出报告文件路径')
    
    args = parser.parse_args()
    
    # 如果没有提供命令行参数，使用默认值
    jtl_file = args.jtl_file if args.jtl_file else r'e:\AI测试用例\接口测试\reports\intent_recognition_test_results_20260112_170614.jtl'
    test_data_file = args.data_file if args.data_file else r'e:\AI测试用例\接口测试\data\intent_recognition_test_data_v2.csv'
    output_file = args.output if args.output else r'e:\AI测试用例\接口测试\reports\test_report_20260112.md'
    
    # 转换为绝对路径
    jtl_file = os.path.abspath(jtl_file)
    test_data_file = os.path.abspath(test_data_file)
    output_file = os.path.abspath(output_file)
    
    print("正在加载测试数据...")
    test_data = load_test_data(test_data_file)
    print(f"已加载 {len(test_data)} 条测试数据")
    
    print("正在分析测试结果...")
    results = analyze_jtl_file(jtl_file, test_data)
    
    print("正在生成报告...")
    report = generate_report(results, output_file, test_data)
    
    print(f"报告已生成: {output_file}")
    print(f"\n测试结果摘要:")
    print(f"- 总用例数: {results['total']}")
    print(f"- 成功用例: {results['success']}")
    print(f"- 失败用例: {results['failed']}")
    print(f"- 通过率: {results['success']/results['total']*100:.2f}%")
    print(f"- 失败率: {results['failed']/results['total']*100:.2f}%")

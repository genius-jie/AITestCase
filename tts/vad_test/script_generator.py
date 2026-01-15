#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
话术生成器 - 基于规则和模板生成完全不同的话术
"""

import json
import csv
import random
from typing import Dict, List, Set
from pathlib import Path


class ScriptGenerator:
    """话术生成器"""

    def __init__(self, csv_file_path: str):
        self.csv_file_path = Path(csv_file_path)
        self.scenario_data: Dict[str, Dict] = {}
        self.used_scripts: Dict[str, Set[str]] = {}
        self.templates = {
            # 正常无停顿
            "normal_no_pause": [
                "这个项目方案设计得挺合理的",
                "这个需求分析得很透彻",
                "这个代码写得很规范",
                "这个测试用例覆盖得很全面",
                "这个文档写得很详细"
            ],
            # 正常短句
            "normal_short": [
                "喂，你好啊",
                "嗨，早上好",
                "哎，在吗",
                "嗯，你好",
                "哈，你好"
            ],
            # 正常长句
            "normal_long": [
                "这个项目方案相当不错，要不咱们一起研究一下？顺便完善一下细节呗",
                "这个需求分析得挺到位，要不咱们一起讨论一下？顺便完善一下方案呗",
                "这个代码实现得挺规范，要不咱们一起review一下？顺便优化一下逻辑呗",
                "这个测试用例覆盖得挺全面，要不咱们一起检查一下？顺便补充一下场景呗",
                "这个文档写得很详细，要不咱们一起看一下？顺便完善一下内容呗"
            ],
            # 正常问句
            "normal_question": [
                "哎，你看这份报告了没？",
                "哎，你看了这个需求没？",
                "哎，你了解这个方案没？",
                "哎，你知道这个功能没？",
                "哎，你见过这个设计没？"
            ],
            # 正常感叹句
            "normal_exclamation": [
                "哇，这个方案太棒了！",
                "哇，这个功能太强了！",
                "哇，这个设计太美了！",
                "哇，这个代码太牛了！",
                "哇，这个测试太全了！"
            ],
            # 极短停顿
            "very_short_pause": [
                "嗯...这个需求文档写得挺清楚的",
                "嗯...这个代码逻辑挺清晰的",
                "嗯...这个测试方案挺完整的",
                "嗯...这个设计文档挺详细的",
                "嗯...这个接口文档挺规范的"
            ],
            # 短停顿
            "short_pause": [
                "那个...这个代码逻辑有点问题",
                "那个...这个需求有点复杂",
                "那个...这个设计有点不足",
                "那个...这个测试有点遗漏",
                "那个...这个文档有点简略"
            ],
            # 中等停顿
            "medium_pause": [
                "嗯...这个测试用例覆盖得挺全面",
                "嗯...这个需求分析得挺到位",
                "嗯...这个代码实现得挺规范",
                "嗯...这个设计考虑得挺周全",
                "嗯...这个文档写得挺详细"
            ],
            # 长停顿
            "long_pause": [
                "那个...这个接口文档需要更新一下",
                "那个...这个需求文档需要完善一下",
                "那个...这个代码注释需要补充一下",
                "那个...这个测试用例需要优化一下",
                "那个...这个设计方案需要调整一下"
            ],
            # 极长停顿
            "very_long_pause": [
                "嗯...那个...这个数据库设计挺合理的",
                "嗯...那个...这个系统架构挺稳定的",
                "嗯...那个...这个算法实现挺高效的",
                "嗯...那个...这个安全机制挺完善的",
                "嗯...那个...这个性能优化挺有效的"
            ],
            # 句首停顿短
            "sentence_start_short": [
                "嗯...今天的会议开得挺顺利",
                "嗯...今天的测试跑得挺顺利",
                "嗯...今天的代码写得挺顺利",
                "嗯...今天的文档写得挺顺利",
                "嗯...今天的部署做得挺顺利"
            ],
            # 句首停顿中
            "sentence_start_medium": [
                "那个...这个Bug修复得挺快",
                "那个...这个需求做得挺快",
                "那个...这个功能做得挺快",
                "那个...这个测试做得挺快",
                "那个...这个文档写得挺快"
            ],
            # 句首停顿长
            "sentence_start_long": [
                "嗯...那个...这个版本发布很成功",
                "嗯...那个...这个项目上线很成功",
                "嗯...那个...这个功能上线很成功",
                "嗯...那个...这个测试通过很成功",
                "嗯...那个...这个部署完成很成功"
            ],
            # 句中停顿短
            "sentence_middle_short": [
                "这个需求...嗯...有点复杂",
                "这个代码...嗯...有点复杂",
                "这个设计...嗯...有点复杂",
                "这个测试...嗯...有点复杂",
                "这个文档...嗯...有点复杂"
            ],
            # 句中停顿中
            "sentence_middle_medium": [
                "这个代码...那个...写得挺规范",
                "这个需求...那个...分析得挺到位",
                "这个设计...那个...考虑得挺周全",
                "这个测试...那个...覆盖得挺全面",
                "这个文档...那个...写得挺详细"
            ],
            # 句中停顿长
            "sentence_middle_long": [
                "这个测试...嗯...那个...做得挺仔细",
                "这个代码...嗯...那个...写得挺仔细",
                "这个需求...嗯...那个...分析得挺仔细",
                "这个设计...嗯...那个...考虑得挺仔细",
                "这个文档...嗯...那个...写得挺仔细"
            ],
            # 句尾停顿短
            "sentence_end_short": [
                "这个功能上线了...嗯",
                "这个需求完成了...嗯",
                "这个代码写完了...嗯",
                "这个测试通过了...嗯",
                "这个文档写完了...嗯"
            ],
            # 句尾停顿中
            "sentence_end_medium": [
                "这个任务完成了...那个...",
                "这个需求完成了...那个...",
                "这个代码完成了...那个...",
                "这个测试完成了...那个...",
                "这个文档完成了...那个..."
            ],
            # 句尾停顿长
            "sentence_end_long": [
                "这个项目验收通过了...嗯...那个...",
                "这个功能验收通过了...嗯...那个...",
                "这个需求验收通过了...嗯...那个...",
                "这个代码验收通过了...嗯...那个...",
                "这个测试验收通过了...嗯...那个..."
            ],
            # 多句首停顿
            "multiple_start_pause": [
                "嗯...这个需求挺重要，咱们一起讨论讨论",
                "嗯...这个代码挺重要，咱们一起review review",
                "嗯...这个设计挺重要，咱们一起看看",
                "嗯...这个测试挺重要，咱们一起检查",
                "嗯...这个文档挺重要，咱们一起审阅"
            ],
            # 多句中停顿
            "multiple_middle_pause": [
                "这个方案...嗯...挺不错，咱们一起讨论讨论",
                "这个需求...嗯...挺不错，咱们一起研究研究",
                "这个代码...嗯...挺不错，咱们一起看看",
                "这个设计...嗯...挺不错，咱们一起分析",
                "这个测试...嗯...挺不错，咱们一起检查"
            ],
            # 多句尾停顿
            "multiple_end_pause": [
                "这个计划真不错，咱们一起讨论讨论...嗯",
                "这个方案真不错，咱们一起研究研究...嗯",
                "这个需求真不错，咱们一起看看...嗯",
                "这个代码真不错，咱们一起review...嗯",
                "这个设计真不错，咱们一起分析...嗯"
            ],
            # 零停顿
            "zero_pause": [
                "这个想法真不错啊",
                "这个建议真不错啊",
                "这个方案真不错啊",
                "这个设计真不错啊",
                "这个代码真不错啊"
            ],
            # 边界停顿最小
            "boundary_min_pause": [
                "嗯...这个建议挺有价值的",
                "嗯...这个方案挺有价值的",
                "嗯...这个需求挺有价值的",
                "嗯...这个设计挺有价值的",
                "嗯...这个代码挺有价值的"
            ],
            # 边界停顿最大
            "boundary_max_pause": [
                "嗯...那个...这个解决方案很完美",
                "嗯...那个...这个设计方案很完美",
                "嗯...那个...这个实现方案很完美",
                "嗯...那个...这个测试方案很完美",
                "嗯...那个...这个优化方案很完美"
            ],
            # 弱杂音无停顿
            "weak_noise_no_pause": [
                "哎，这个产品设计得真不错啊",
                "哎，这个功能设计得真不错啊",
                "哎，这个界面设计得真不错啊",
                "哎，这个交互设计得真不错啊",
                "哎，这个体验设计得真不错啊"
            ],
            # 中杂音无停顿
            "medium_noise_no_pause": [
                "哎，这个用户体验做得真好",
                "哎，这个功能体验做得真好",
                "哎，这个界面体验做得真好",
                "哎，这个交互体验做得真好",
                "哎，这个操作体验做得真好"
            ],
            # 强杂音无停顿
            "strong_noise_no_pause": [
                "哎，这个界面设计很漂亮",
                "哎，这个布局设计很漂亮",
                "哎，这个配色设计很漂亮",
                "哎，这个图标设计很漂亮",
                "哎，这个动效设计很漂亮"
            ],
            # 弱杂音句首停顿
            "weak_noise_start_pause": [
                "嗯...哎，这个交互设计很流畅",
                "嗯...哎，这个操作设计很流畅",
                "嗯...哎，这个流程设计很流畅",
                "嗯...哎，这个体验设计很流畅",
                "嗯...哎，这个功能设计很流畅"
            ],
            # 中杂音句首停顿
            "medium_noise_start_pause": [
                "嗯...哎，这个功能实现很稳定",
                "嗯...哎，这个系统实现很稳定",
                "嗯...哎，这个服务实现很稳定",
                "嗯...哎，这个接口实现很稳定",
                "嗯...哎，这个模块实现很稳定"
            ],
            # 强杂音句首停顿
            "strong_noise_start_pause": [
                "嗯...哎，这个性能优化很有效",
                "嗯...哎，这个内存优化很有效",
                "嗯...哎，这个CPU优化很有效",
                "嗯...哎，这个IO优化很有效",
                "嗯...哎，这个网络优化很有效"
            ],
            # 弱杂音句中停顿
            "weak_noise_middle_pause": [
                "哎，这个架构...嗯...设计得很合理",
                "哎，这个系统...嗯...设计得很合理",
                "哎，这个模块...嗯...设计得很合理",
                "哎，这个接口...嗯...设计得很合理",
                "哎，这个数据库...嗯...设计得很合理"
            ],
            # 中杂音句中停顿
            "medium_noise_middle_pause": [
                "哎，这个算法...嗯...实现得很高效",
                "哎，这个逻辑...嗯...实现得很高效",
                "哎，这个功能...嗯...实现得很高效",
                "哎，这个服务...嗯...实现得很高效",
                "哎，这个接口...嗯...实现得很高效"
            ],
            # 强杂音句中停顿
            "strong_noise_middle_pause": [
                "哎，这个安全机制...嗯...做得很到位",
                "哎，这个权限机制...嗯...做得很到位",
                "哎，这个加密机制...嗯...做得很到位",
                "哎，这个认证机制...嗯...做得很到位",
                "哎，这个审计机制...嗯...做得很到位"
            ],
            # 弱杂音句尾停顿
            "weak_noise_end_pause": [
                "哎，这个测试覆盖率...嗯...挺高的",
                "哎，这个代码覆盖率...嗯...挺高的",
                "哎，这个需求覆盖率...嗯...挺高的",
                "哎，这个场景覆盖率...嗯...挺高的",
                "哎，这个功能覆盖率...嗯...挺高的"
            ],
            # 中杂音句尾停顿
            "medium_noise_end_pause": [
                "哎，这个文档质量...嗯...很好",
                "哎，这个代码质量...嗯...很好",
                "哎，这个测试质量...嗯...很好",
                "哎，这个设计质量...嗯...很好",
                "哎，这个需求质量...嗯...很好"
            ],
            # 强杂音句尾停顿
            "strong_noise_end_pause": [
                "哎，这个代码注释...嗯...很详细",
                "哎，这个函数注释...嗯...很详细",
                "哎，这个类注释...嗯...很详细",
                "哎，这个模块注释...嗯...很详细",
                "哎，这个接口注释...嗯...很详细"
            ],
            # 无杂音句首停顿
            "no_noise_start_pause": [
                "嗯...这个需求分析得很透彻",
                "嗯...这个代码分析得很透彻",
                "嗯...这个设计分析得很透彻",
                "嗯...这个测试分析得很透彻",
                "嗯...这个文档分析得很透彻"
            ],
            # 无杂音句中停顿
            "no_noise_middle_pause": [
                "这个设计...嗯...考虑得很周全",
                "这个需求...嗯...考虑得很周全",
                "这个代码...嗯...考虑得很周全",
                "这个测试...嗯...考虑得很周全",
                "这个文档...嗯...考虑得很周全"
            ],
            # 无杂音句尾停顿
            "no_noise_end_pause": [
                "这个实现...嗯...做得很规范",
                "这个代码...嗯...做得很规范",
                "这个需求...嗯...做得很规范",
                "这个设计...嗯...做得很规范",
                "这个测试...嗯...做得很规范"
            ],
            # 正常语气
            "normal_tone": [
                "今天天气真不错啊",
                "今天心情真不错啊",
                "今天状态真不错啊",
                "今天效率真不错啊",
                "今天运气真不错啊"
            ],
            # 开心语气
            "cheerful_tone": [
                "哈哈，今天真是太开心了！",
                "哈哈，这个结果真是太开心了！",
                "哈哈，这个消息真是太开心了！",
                "哈哈，这个成就真是太开心了！",
                "哈哈，这个收获真是太开心了！"
            ],
            # 严肃语气
            "serious_tone": [
                "这个通知很重要，请知悉。",
                "这个消息很重要，请知悉。",
                "这个要求很重要，请知悉。",
                "这个规定很重要，请知悉。",
                "这个决定很重要，请知悉。"
            ],
            # 悲伤语气
            "sad_tone": [
                "唉，今天真倒霉...",
                "唉，今天真遗憾...",
                "唉，今天真失望...",
                "唉，今天真难过...",
                "唉，今天真可惜..."
            ],
            # 兴奋语气
            "excited_tone": [
                "哇塞！今天太激动了！",
                "哇塞！这个结果太激动了！",
                "哇塞！这个消息太激动了！",
                "哇塞！这个成就太激动了！",
                "哇塞！这个收获太激动了！"
            ],
            # 愤怒语气
            "angry_tone": [
                "我靠，今天真气人！",
                "我靠，这个结果真气人！",
                "我靠，这个消息真气人！",
                "我靠，这个情况真气人！",
                "我靠，这个事情真气人！"
            ],
            # 温柔语气
            "gentle_tone": [
                "这个礼物真好呢",
                "这个想法真好呢",
                "这个建议真好呢",
                "这个方案真好呢",
                "这个设计真好呢"
            ],
            # 客服语气
            "customer_service_tone": [
                "您好，请问有什么可以帮您？",
                "您好，请问有什么需要帮忙？",
                "您好，请问有什么可以协助？",
                "您好，请问有什么可以支持？",
                "您好，请问有什么可以服务？"
            ],
            # 开心停顿
            "cheerful_pause": [
                "哇！太棒了！终于放假了！",
                "哇！太好了！终于完成了！",
                "哇！太强了！终于成功了！",
                "哇！太美了！终于实现了！",
                "哇！太牛了！终于搞定了！"
            ],
            # 悲伤停顿
            "sad_pause": [
                "唉...我太伤心了，错过了这次机会...",
                "唉...我太遗憾了，错过了这次机会...",
                "唉...我太失望了，错过了这次机会...",
                "唉...我太难过，错过了这次机会...",
                "唉...我太可惜了，错过了这次机会..."
            ],
            # 愤怒停顿
            "angry_pause": [
                "我靠...怎么这都不明白啊",
                "我靠...怎么这都不理解啊",
                "我靠...怎么这都不知道啊",
                "我靠...怎么这都不清楚啊",
                "我靠...怎么这都不明白啊"
            ],
            # 兴奋停顿
            "excited_pause": [
                "哇！太激动了！我中奖了！",
                "哇！太兴奋了！我成功了！",
                "哇！太开心了！我完成了！",
                "哇！太激动了！我实现了！",
                "哇！太兴奋了！我搞定了！"
            ]
        }

        # 场景类型到模板的映射
        self.scenario_to_template = {
            "正常无停顿": "normal_no_pause",
            "正常短句": "normal_short",
            "正常长句": "normal_long",
            "正常问句": "normal_question",
            "正常感叹句": "normal_exclamation",
            "纯标点": "normal_short",
            "数字文本": "normal_short",
            "英文文本": "normal_short",
            "混合文本": "normal_short",
            "极短停顿": "very_short_pause",
            "短停顿": "short_pause",
            "中等停顿": "medium_pause",
            "长停顿": "long_pause",
            "极长停顿": "very_long_pause",
            "句首停顿短": "sentence_start_short",
            "句首停顿中": "sentence_start_medium",
            "句首停顿长": "sentence_start_long",
            "句中停顿短": "sentence_middle_short",
            "句中停顿中": "sentence_middle_medium",
            "句中停顿长": "sentence_middle_long",
            "句尾停顿短": "sentence_end_short",
            "句尾停顿中": "sentence_end_medium",
            "句尾停顿长": "sentence_end_long",
            "多句首停顿": "multiple_start_pause",
            "多句中停顿": "multiple_middle_pause",
            "多句尾停顿": "multiple_end_pause",
            "零停顿": "zero_pause",
            "边界停顿最小": "boundary_min_pause",
            "边界停顿最大": "boundary_max_pause",
            "弱杂音无停顿": "weak_noise_no_pause",
            "中杂音无停顿": "medium_noise_no_pause",
            "强杂音无停顿": "strong_noise_no_pause",
            "弱杂音句首停顿": "weak_noise_start_pause",
            "中杂音句首停顿": "medium_noise_start_pause",
            "强杂音句首停顿": "strong_noise_start_pause",
            "弱杂音句中停顿": "weak_noise_middle_pause",
            "中杂音句中停顿": "medium_noise_middle_pause",
            "强杂音句中停顿": "strong_noise_middle_pause",
            "弱杂音句尾停顿": "weak_noise_end_pause",
            "中杂音句尾停顿": "medium_noise_end_pause",
            "强杂音句尾停顿": "strong_noise_end_pause",
            "无杂音句首停顿": "no_noise_start_pause",
            "无杂音句中停顿": "no_noise_middle_pause",
            "无杂音句尾停顿": "no_noise_end_pause",
            "正常语气": "normal_tone",
            "开心语气": "cheerful_tone",
            "严肃语气": "serious_tone",
            "悲伤语气": "sad_tone",
            "兴奋语气": "excited_tone",
            "愤怒语气": "angry_tone",
            "温柔语气": "gentle_tone",
            "客服语气": "customer_service_tone",
            "开心停顿": "cheerful_pause",
            "悲伤停顿": "sad_pause",
            "愤怒停顿": "angry_pause",
            "兴奋停顿": "excited_pause"
        }

    def read_csv_data(self) -> bool:
        """
        读取CSV测试数据

        Returns:
            是否成功
        """
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    scenario_id = row.get('scenario_id', '')
                    if scenario_id and not scenario_id.startswith('#'):
                        self.scenario_data[scenario_id] = row

            print(f"✅ 成功读取 {len(self.scenario_data)} 条测试数据")
            return True
        except Exception as e:
            print(f"❌ 读取CSV文件失败: {e}")
            return False

    def generate_script(self, scenario_id: str, scenario_type: str, old_text: str) -> str:
        """
        为指定场景生成话术

        Args:
            scenario_id: 场景ID
            scenario_type: 场景类型
            old_text: 原始文本

        Returns:
            生成的话术
        """
        # 获取对应的模板类型
        template_type = self.scenario_to_template.get(scenario_type, "normal_short")

        # 获取模板列表
        templates = self.templates.get(template_type, ["这个功能挺不错的"])

        # 初始化该场景类型的已使用集合
        if template_type not in self.used_scripts:
            self.used_scripts[template_type] = set()

        # 随机选择一个未使用的模板
        available_templates = [t for t in templates if t not in self.used_scripts[template_type]]

        if not available_templates:
            # 如果所有模板都用过了，重置该场景类型的已使用集合
            self.used_scripts[template_type].clear()
            available_templates = templates

        new_text = random.choice(available_templates)
        self.used_scripts[template_type].add(new_text)

        return new_text

    def generate_json_file(self, template_file: str, output_file: str) -> bool:
        """
        生成完整的JSON修改文件

        Args:
            template_file: 模板文件路径
            output_file: 输出文件路径

        Returns:
            是否成功
        """
        try:
            # 读取CSV数据
            if not self.read_csv_data():
                return False

            # 读取模板文件
            with open(template_file, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            # 为每个场景生成新话术
            for modification in template_data['modifications']:
                scenario_id = modification['scenario_id']
                old_text = modification['old_text']

                # 从CSV数据中获取场景类型
                scenario_data = self.scenario_data.get(scenario_id, {})
                scenario_type = scenario_data.get('scenario_name', '正常短句')

                # 生成新话术
                new_text = self.generate_script(scenario_id, scenario_type, old_text)

                # 更新modification
                modification['new_text'] = new_text
                modification['reason'] = f"基于规则生成：{scenario_type}场景的多样化话术"

            # 保存到输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)

            print(f"✅ JSON文件已生成: {output_file}")
            return True

        except Exception as e:
            print(f"❌ 生成JSON文件失败: {e}")
            return False


def main():
    """主函数"""
    csv_file = "e:\\AI测试用例\\语音生成\\vad_test\\vad_test_data_noise_comparison.csv"
    generator = ScriptGenerator(csv_file)

    # 生成JSON文件
    template_file = "e:\\AI测试用例\\语音生成\\vad_test\\text_modifications_template.json"
    output_file = "e:\\AI测试用例\\语音生成\\vad_test\\text_modifications_v6.0.json"

    success = generator.generate_json_file(template_file, output_file)

    if success:
        print("✅ 话术生成完成！")
    else:
        print("❌ 话术生成失败！")


if __name__ == "__main__":
    main()

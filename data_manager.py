# data_manager.py
import csv
import os
import random
import re


class DataManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path

        # 检查文件是否存在
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV数据文件未找到: {csv_path}")

        # 加载数据
        self.attractions = []
        self.load_data()

    def load_data(self):
        """从CSV文件加载数据，更健壮的实现"""
        try:
            with open(self.csv_path, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()

                # 跳过空行
                lines = [line.strip() for line in lines if line.strip()]

                # 处理每一行数据
                for i, line in enumerate(lines):
                    if i == 0:  # 跳过表头
                        continue

                    # 分割字段，我们知道每行有8个主要字段
                    parts = line.split('\t')

                    if len(parts) < 2:  # 尝试用空格分割
                        parts = line.split()

                    # 创建景点字典
                    attraction = {}

                    # 根据你提供的CSV，我们采用更直接的方式解析
                    # 去掉每个字段前后的空格
                    cleaned_parts = []
                    current_part = ""

                    # 识别数字编号作为ID
                    if parts and parts[0].strip().isdigit():
                        attraction['id'] = int(parts[0].strip())
                        # 移除ID部分
                        line = line.lstrip(parts[0]).strip()

                    # 使用自定义方法分割，因为数据格式复杂
                    fields = self._custom_split(line)

                    # 确保至少有基本字段
                    if len(fields) >= 6:
                        attraction['Attraction'] = fields[0].strip() if fields[0] else f"景点{i}"
                        attraction['Attraction_EN'] = fields[1].strip() if len(fields) > 1 and fields[1] else ""
                        attraction['Category'] = fields[2].strip() if len(fields) > 2 and fields[2] else "未分类"
                        attraction['Category_EN'] = fields[3].strip() if len(fields) > 3 and fields[3] else ""
                        attraction['District'] = fields[4].strip() if len(fields) > 4 and fields[4] else "未知区域"
                        attraction['District_EN'] = fields[5].strip() if len(fields) > 5 and fields[5] else ""

                        # Google地图链接可能很长，但它总是一个URL
                        if len(fields) > 6 and "google.com/maps" in fields[6]:
                            attraction['Google Map Link'] = fields[6].strip()
                        else:
                            attraction['Google Map Link'] = ""

                        # 备注字段可能存在也可能不存在
                        if len(fields) > 7:
                            attraction['Remarks'] = fields[7].strip()
                        else:
                            attraction['Remarks'] = ""

                        # 将景点添加到列表中
                        self.attractions.append(attraction)
                    elif 'id' in attraction:
                        # 如果只有ID，也添加一个基本景点
                        attraction['Attraction'] = f"景点{attraction['id']}"
                        attraction['Attraction_EN'] = f"Attraction {attraction['id']}"
                        attraction['Category'] = "未分类"
                        attraction['Category_EN'] = "Uncategorized"
                        attraction['District'] = "未知区域"
                        attraction['District_EN'] = "Unknown Area"
                        attraction['Google Map Link'] = ""
                        attraction['Remarks'] = ""
                        self.attractions.append(attraction)

            if not self.attractions:
                raise ValueError("未能从CSV文件中解析出任何景点数据")

            print(f"已成功加载 {len(self.attractions)} 个景点数据")

        except Exception as e:
            print(f"加载CSV文件时出错: {e}")
            # 创建一些样本数据，以便应用程序可以继续运行
            self.create_sample_data()

    def _custom_split(self, line):
        """自定义分割方法，处理特殊格式的CSV行"""
        # 我们知道原始格式是用\t分隔主要字段
        # 但也可能使用其他分隔符

        # 先尝试简单的分隔方式
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 6:
                return parts

        # 尝试使用双分号分割
        if ';;' in line:
            parts = line.split(';;')
            return parts

        # 尝试提取数据的模式可能更复杂
        # 根据你提供的CSV样本构建一个更健壮的解析器

        # 模式：每行有ID、中文名、英文名、类别(中)、类别(英)、区域(中)、区域(英)、地图链接、备注
        # 使用正则表达式匹配
        pattern = r'(\d+)\s+(.+?)\s+(.+?)\s+(打卡|文化體驗|觀光|娛樂|美食|購物)\s+(\w+)\s+(.+?)\s+(.+?)\s+(https://.+?)(?:\s+(.+))?$'
        match = re.match(pattern, line)

        if match:
            # 0: ID, 1: 中文名, 2: 英文名, 3: 类别(中), 4: 类别(英), 5: 区域(中), 6: 区域(英), 7: 地图链接, 8: 备注(可选)
            return list(match.groups()[1:])  # 不包括ID，因为我们已经单独处理了

        # 如果上述方法都失败，则尝试最基本的分割
        # 先按空格分割，再尝试重组
        words = line.split()
        if not words:
            return ["未知景点"]

        # 将第一个单词作为景点名称
        attraction_name = words[0]
        result = [attraction_name]

        # 检测关键词来推断字段
        category_keywords = ["打卡", "文化體驗", "觀光", "娛樂", "美食", "購物", "PhotoTaking", "Culture",
                             "Sightseeing", "Entertainment", "Delicacy", "Shopping"]
        district_keywords = ["區", "区", "District"]
        url_keywords = ["http", "www", "google"]

        # 构建结果列表
        category = next((word for word in words if any(keyword in word for keyword in category_keywords)), "未分类")
        district = next((word for word in words if any(keyword in word for keyword in district_keywords)), "未知区域")
        url = next((word for word in words if any(keyword in word for keyword in url_keywords)), "")

        # 组装最基本的字段
        basic_fields = [attraction_name, "", category, "", district, "", url, ""]

        # 返回基本字段
        return basic_fields

    def parse_csv_directly(self):
        """直接解析你提供的CSV数据格式"""
        try:
            with open(self.csv_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                lines = content.strip().split('\n')

                for i, line in enumerate(lines):
                    if i == 0:  # 跳过表头
                        continue

                    # 分割每一行
                    parts = []
                    current_part = ""
                    in_quotes = False

                    for char in line:
                        if char == '\t':
                            if not in_quotes:
                                parts.append(current_part)
                                current_part = ""
                            else:
                                current_part += char
                        elif char == '"':
                            in_quotes = not in_quotes
                        else:
                            current_part += char

                    # 添加最后一部分
                    parts.append(current_part)

                    # 确保我们至少有8个部分
                    while len(parts) < 8:
                        parts.append("")

                    # 创建景点字典
                    attraction = {
                        'id': int(parts[0]) if parts[0].strip().isdigit() else i,
                        'Attraction': parts[1].strip(),
                        'Attraction_EN': parts[2].strip(),
                        'Category': parts[3].strip(),
                        'Category_EN': parts[4].strip(),
                        'District': parts[5].strip(),
                        'District_EN': parts[6].strip(),
                        'Google Map Link': parts[7].strip()
                    }

                    # 如果有备注，添加备注
                    if len(parts) > 8:
                        attraction['Remarks'] = parts[8].strip()
                    else:
                        attraction['Remarks'] = ""

                    self.attractions.append(attraction)

                print(f"已成功加载 {len(self.attractions)} 个景点数据")

        except Exception as e:
            print(f"直接解析CSV时出错: {e}")
            self.create_sample_data()

    def create_sample_data(self):
        """创建样本数据"""
        print("创建样本数据以便应用程序可以继续运行")
        self.attractions = [
            {
                'id': 1,
                'Attraction': '怪獸大廈',
                'Attraction_EN': 'Monster Building',
                'Category': '打卡',
                'Category_EN': 'PhotoTaking',
                'District': '東 區',
                'District_EN': 'Eastern',
                'Google Map Link': 'https://www.google.com/maps/place/%E7%9B%8A%E6%98%8C%E5%A4%A7%E5%BB%88/@22.2836592,114.2068258,15.75z',
                'Remarks': ''
            },
            {
                'id': 2,
                'Attraction': '中環至半山扶手電梯',
                'Attraction_EN': 'Central-Mid-Levels Escalator and Walkway System',
                'Category': '打卡',
                'Category_EN': 'PhotoTaking',
                'District': '中西區',
                'District_EN': 'Central and Western',
                'Google Map Link': 'https://www.google.com/maps/place/%E4%B8%AD%E7%92%B0%E5%8D%8A%E5%B1%B1%E6%89%B6%E6%89%8B%E9%9B%BB%E6%A2%AF/@22.2838513,114.152394,17z',
                'Remarks': ''
            },
            {
                'id': 21,
                'Attraction': '太平山山頂',
                'Attraction_EN': 'Victoria Peak',
                'Category': '觀光',
                'Category_EN': 'Sightseeing',
                'District': '中西區',
                'District_EN': 'Central and Western',
                'Google Map Link': 'https://www.google.com.hk/maps/place/%E5%A4%AA%E5%B9%B3%E5%B1%B1/@22.275893,114.1403821,16z',
                'Remarks': '香港著名观景点，可俯瞰维多利亚港'
            },
            {
                'id': 31,
                'Attraction': '香港迪士尼樂園',
                'Attraction_EN': 'Hong Kong Disneyland',
                'Category': '娛樂',
                'Category_EN': 'Entertainment',
                'District': '離島區',
                'District_EN': 'Islands',
                'Google Map Link': 'https://www.google.com/maps/place/%E9%A6%99%E6%B8%AF%E8%BF%AA%E5%A3%AB%E5%B0%BC%E6%A8%82%E5%9C%92/@22.3129666,114.038707,17z',
                'Remarks': '香港著名主题乐园'
            },
            {
                'id': 37,
                'Attraction': '甘牌燒鵝',
                'Attraction_EN': 'Kam\'s Roast Goose',
                'Category': '美食',
                'Category_EN': 'Delicacy',
                'District': '灣 仔',
                'District_EN': 'Wan Chai',
                'Google Map Link': 'https://www.google.com/maps/place/%E7%94%98%E7%89%8C%E7%87%92%E9%B5%9D/@22.277642,114.1727301,17z',
                'Remarks': '米其林星级餐厅'
            },
            {
                'id': 42,
                'Attraction': '葵涌廣場',
                'Attraction_EN': 'Kwai Chung Plaza',
                'Category': '購物',
                'Category_EN': 'Shopping',
                'District': '葵青區',
                'District_EN': 'Kwai Tsing',
                'Google Map Link': 'https://www.google.com.hk/maps/place/Kwai+Chung+Plaza/@22.358021,114.1253288,17z',
                'Remarks': '购物天堂'
            }
        ]

    def load_from_raw_data(self, raw_data):
        """从原始数据字符串加载"""
        try:
            lines = raw_data.strip().split('\n')

            # 处理每一行数据
            for i, line in enumerate(lines):
                if i == 0:  # 跳过表头
                    continue

                # 分割字段
                parts = line.split('\t')

                # 确保至少有8个字段
                if len(parts) < 8:
                    continue

                # 创建景点字典
                attraction = {
                    'id': int(parts[0]) if parts[0].strip().isdigit() else i,
                    'Attraction': parts[1].strip(),
                    'Attraction_EN': parts[2].strip(),
                    'Category': parts[3].strip(),
                    'Category_EN': parts[4].strip(),
                    'District': parts[5].strip(),
                    'District_EN': parts[6].strip(),
                    'Google Map Link': parts[7].strip()
                }

                # 如果有备注，添加备注
                if len(parts) > 8:
                    attraction['Remarks'] = parts[8].strip()
                else:
                    attraction['Remarks'] = ""

                self.attractions.append(attraction)

            print(f"已从原始数据加载 {len(self.attractions)} 个景点")

        except Exception as e:
            print(f"从原始数据加载时出错: {e}")
            self.create_sample_data()

    def get_all_attractions(self):
        """获取所有景点"""
        return self.attractions

    def get_unique_categories(self):
        """获取所有独特的类别"""
        # 返回中文类别
        categories = set()
        for attraction in self.attractions:
            cat = attraction.get('Category', '')
            if cat:
                categories.add(cat)
        return list(categories)

    def get_unique_districts(self):
        """获取所有独特的区域"""
        districts = set()
        for attraction in self.attractions:
            district = attraction.get('District', '')
            if district:
                districts.add(district)
        return list(districts)

    def get_attractions_by_category(self, category):
        """根据类别获取景点"""
        return [a for a in self.attractions if category in a.get('Category', '')]

    def get_attractions_by_district(self, district):
        """根据区域获取景点"""
        return [a for a in self.attractions if district in a.get('District', '')]

    def get_attraction_by_id(self, attraction_id):
        """根据ID获取景点"""
        for attraction in self.attractions:
            if attraction.get('id') == attraction_id:
                return attraction
        return None

    def get_featured_attractions(self, limit=4):
        """获取推荐景点"""
        # 尝试从每个类别中选择一个景点
        featured = []
        categories = self.get_unique_categories()

        for category in categories:
            category_attractions = self.get_attractions_by_category(category)
            if category_attractions:
                featured.append(random.choice(category_attractions))
                if len(featured) >= limit:
                    break

        # 如果推荐的景点不足，随机添加
        if len(featured) < limit:
            remaining = limit - len(featured)
            available = [a for a in self.attractions if a not in featured]
            if available:
                featured.extend(random.sample(available, min(remaining, len(available))))

        return featured

    def generate_random_route(self, count=5):
        """生成随机路线"""
        if count > len(self.attractions):
            count = len(self.attractions)
        # 随机选择指定数量的景点
        return random.sample(self.attractions, count)
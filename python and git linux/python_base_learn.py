# ==================== Python 基础学习笔记 ====================
# 作者：XYQIXIN
# 日期：2026年
# 用途：Python 基础知识复习总结


# ==================== 第一章：字符串与输出 ====================
# 【知识点总结】
# 1. 字符串定义：用单引号、双引号或三引号括起来的文本
# 2. 转义字符：\n(换行)、\t(制表符)、\'(单引号)、\"(双引号)
# 3. 字符串拼接：使用 + 号连接多个字符串
# 4. print() 函数：输出内容到控制台

# 简单字符串输出
# print("Dad!!")
# print("爸！！")

# 字符串拼接示例
# print("你好" + " 这是一句代码" + " 哈哈")

# 转义字符：当字符串中包含引号时需要转义
# print('Let\'s go')  # 输出：Let's go

# 换行符示例
# print("我是第一行\n我是第二行")

# 三引号字符串（支持多行文本）
# print("""白日依山尽
# 黄河入海流
# 欲穷千里目
# 更上一层楼
# """)


# ==================== 第二章：变量与赋值 ====================
# 【知识点总结】
# 1. 变量：存储数据的容器，无需声明类型（动态类型语言）
# 2. 命名规范：推荐下划线命名法（snake_case），见名知意
# 3. 赋值：使用 = 号将值赋给变量

# greet = "您好，吃了么"        # 字符串变量
# greet_chinese = greet         # 变量赋值
# greet_english = "Yo what's up"
# print(greet_english + " 张三")
# print(greet_chinese + " 王五")

# 下划线命名法示例：user_name, total_count, max_value


# ==================== 第三章：数学运算与模块导入 ====================
# 【知识点总结】
# 1. 基本运算：+ - * / **(幂运算)
# 2. 模块导入：import 模块名
# 3. math 模块常用函数：sqrt(开平方)、sin、cos、pi 等

# import math
# a = -1  # 一元二次方程 ax² + bx + c = 0 的系数
# b = -2
# c = 3

# delta = b**2 - 4 * a * c  # 判别式
# print((-b + math.sqrt(delta)) / (2 * a))  # 第一个根
# print((-b - math.sqrt(delta)) / (2 * a))  # 第二个根


# ==================== 第四章：数据类型详解 ====================
# 【知识点总结】
# Python 五大基本数据类型：
# 1. str（字符串）：文本数据
# 2. int（整数）：不带小数点的数字
# 3. float（浮点数）：带小数点的数字
# 4. bool（布尔值）：True / False
# 5. NoneType（空值）：None

# 字符串操作
# s = "hello world!"
# print(len(s))          # 获取字符串长度：12
# print(s[0])            # 通过索引获取字符（索引从 0 开始）
# print(s[-1])           # 负数索引表示倒数第一个字符
# print(type(s))         # <class 'str'>

# 布尔类型
# b1 = True
# b2 = False
# print(type(b1))        # <class 'bool'>

# 空值类型
# n = None
# print(type(n))         # <class 'NoneType'>


# ==================== 第五章：输入与类型转换 ====================
# 【知识点总结】
# 1. input()：获取用户输入，返回字符串类型
# 2. 类型转换：int()、float()、str()

# BMI 计算器示例（体重 / 身高²）
# user_weight = float(input("请输入你的体重（单位：kg）："))
# user_height = float(input("请输入你的身高（单位：m）："))
# user_BMI = user_weight / user_height ** 2
# print("您的BMI值为：" + str(user_BMI))


# ==================== 第六章：条件判断语句 ====================
# 【知识点总结】
# 1. 条件运算符：==(等于)、!=(不等于)、>(大于)、<(小于)、>=(大于等于)、<=(小于等于)
# 2. if-else 结构：根据条件执行不同代码块
# 3. 嵌套条件：if 语句中可以嵌套另一个 if 语句

# 简单条件判断
# mood_index = int(input("对象今天的心情指数："))
# if mood_index >= 60:
#     print("恭喜，今晚应该可以打游戏，去吧皮卡丘！")
# else:
#     print("为了自己小命，还是别打了。")

# 嵌套条件语句（BMI 分类）
# user_weight = float(input("请输入你的体重（kg）："))
# user_height = float(input("请输入你的身高（m）："))
# user_BMI = user_weight / user_height ** 2
# print("您的BMI值为：" + str(user_BMI))
# if user_BMI < 18.5:
#     print("您的BMI结果为偏瘦")
# elif user_BMI >= 18.5 and user_BMI <= 25:
#     print("您的BMI结果为正常")
# elif user_BMI >= 25 and user_BMI <= 30:
#     print("您的BMI结果为偏胖")
# else:
#     print("您的BMI结果为肥胖")


# ==================== 第七章：逻辑运算符 ====================
# 【知识点总结】
# 1. and（与）：所有条件都为 True 时结果为 True
# 2. or（或）：只要有一个条件为 True 结果为 True
# 3. not（非）：取反
# 优先级：not > and > or


# ==================== 第八章：列表（List） ====================
# 【知识点总结】
# 1. 列表定义：用方括号 [] 表示，元素用逗号分隔
# 2. 列表特性：有序、可变、可包含不同类型元素
# 3. 常用方法：append() 添加、remove() 删除、len() 长度
# 4. 索引访问：list[index]，索引从 0 开始

# 购物清单示例
# shopping_list = []
# shopping_list.append("键盘")   # 添加元素
# shopping_list.append("键帽")
# shopping_list.remove("键帽")   # 删除元素
# shopping_list.append("音响")
# shopping_list.append("电竞椅")
# shopping_list[1] = "硬盘"      # 修改元素
# print(shopping_list)           # 输出列表内容
# print(len(shopping_list))      # 获取列表长度

# 列表常用函数
# price = [799, 1024, 200, 800]
# print(max(price))      # 最大值
# print(min(price))      # 最小值
# print(sorted(price))   # 排序（返回新列表）


# ==================== 第九章：字典（Dictionary） ====================
# 【知识点总结】
# 1. 字典定义：用大括号 {} 表示，键值对形式 key:value
# 2. 字典特性：无序（Python 3.7+有序）、键唯一、值可重复
# 3. 访问方式：dict[key] 获取值，dict.keys() 获取所有键
# 4. dict.values() 获取所有值，dict.items() 获取所有键值对

# 电子词典示例
# slang_dict = {
#     "无源域自适应": "不访问源域数据，仅用预训练模型适应目标域。",
#     "师生模型": "教师生成伪标签，学生学习，通过指数移动平均更新。"
# }
# slang_dict["目标域增强模块"] = "用自适应实例归一化将目标域图像变为自身典型风格。"
# slang_dict["协同更新机制"] = "每个epoch结束用教师反向更新学生，形成双向约束。"

# query = input("请输入你想查询的毕设名词:")
# if query in slang_dict:
#     print("您查询的" + query + "含义如下")
#     print(slang_dict[query])
# else:
#     print("您查询的毕设名词暂未收录")
#     print("当前字典收录的词条数为" + str(len(slang_dict)) + "条")


# ==================== 第十章：循环语句 ====================
# 【知识点总结】
# 1. for 循环：for 变量 in 可迭代对象
# 2. while 循环：while 条件: 执行语句
# 3. range() 函数：生成整数序列，range(start, end, step)

# 求平均值程序（while 循环）
# print("哈喽呀,我是一个求平均值的程序")
# total = 0
# count = 0
# user_input = input("请输入数字(完成所有数字输入后,请输入q终止程序) : ")
# while user_input != "q":
#     num = float(user_input)
#     total += num      # 累加总和
#     count += 1        # 计数
#     user_input = input("请输入数字(完成所有数字输入后,请输入q终止程序) : ")
# if count == 0:
#     result = 0
# else:
#     result = total / count
# print("您输入的数字平均值为" + str(result))


# ==================== 第十一章：函数定义 ====================
# 【知识点总结】
# 1. 函数定义：def 函数名(参数):
# 2. 返回值：return 语句
# 3. 函数调用：函数名(参数)

# BMI 计算函数
# def calculate_BMI(weight, height):
#     BMI = weight / (height * height)
#     if BMI <= 18.5:
#         category = "偏瘦"
#     elif BMI >= 18.5 and BMI <= 25:
#         category = "正常"
#     elif BMI >= 25 and BMI <= 30:
#         category = "偏胖"
#     else:
#         category = "肥胖"
#     print(f"您的BMI分类为:{category}")
#     return BMI  # 返回计算结果

# result = calculate_BMI(60, 1.70)


# ==================== 第十二章：模块导入 ====================
# 【知识点总结】
# 1. import 模块名：导入整个模块
# 2. from 模块名 import 函数名：导入特定函数
# 3. from 模块名 import *：导入所有内容（不推荐）


# ==================== 第十三章：面向对象编程 ====================
# 【知识点总结】
# 1. 类定义：class 类名:
# 2. 构造方法：__init__(self, 参数)
# 3. 属性：self.属性名
# 4. 方法：def 方法名(self, 参数)
# 5. 继承：class 子类名(父类名)

# 简单类示例
# class CuteCat:
#     def __init__(self, name, age):
#         self.name = name  # 属性
#         self.age = age
# cat1 = CuteCat("xiaomu", 18)
# print(f"小猫{cat1.name}的年龄是{cat1.age}岁")

# 学生类示例
# class Student:
#     def __init__(self, name, student_id):
#         self.name = name
#         self.student_id = student_id
#         self.grades = {"语文": 0, "数学": 0, "英语": 0}
    
#     def set_grades(self, course, grade):
#         if course in self.grades:
#             self.grades[course] = grade
    
#     def print_grades(self):
#         print(f"学生{self.name}({self.student_id})的成绩为")
#         for course in self.grades:
#             print(f"{course}:{self.grades[course]}分")

# xu = Student("xu", 1)
# chen = Student("chen", 2)
# chen.set_grades("语文", 95)
# chen.set_grades("数学", 93)
# chen.set_grades("英语", 93)
# xu.set_grades("数学", 95)

# 继承示例（员工类）
# class Employee:
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id
    
#     def print_info(self):
#         print(f"员工名字:{self.name},工号:{self.id}")

# class FullTimeEmployee(Employee):
#     def __init__(self, name, id, monthly_salary):
#         super().__init__(name, id)  # 调用父类构造方法
#         self.monthly_salary = monthly_salary
    
#     def calculate_monthly_salary(self):
#         return self.monthly_salary

# class PartTimeEmployee(Employee):
#     def __init__(self, name, id, daily_salary, work_days):
#         super().__init__(name, id)
#         self.daily_salary = daily_salary
#         self.work_days = work_days
    
#     def calculate_monthly_salary(self):
#         return self.daily_salary * self.work_days

# ZS = FullTimeEmployee("张三", "101", 10000)
# LS = PartTimeEmployee("李四", "103", 300, 28)


# ==================== 第十四章：文件操作 ====================
# 【知识点总结】
# 1. 文件打开：open(file_path, mode, encoding)
# 2. 打开模式：r(只读)、w(写入)、a(追加)
# 3. 推荐方式：with 语句（自动关闭文件）
# 4. 读取方法：read()、readline()、readlines()
# 5. 写入方法：write()

# 读取文件
# with open("./data.txt", "r", encoding="utf-8") as f:
#     print(f.readlines())  # 按行读取所有内容

# 写入文件（覆盖原有内容）
# with open("./poem.txt", "w", encoding="utf-8") as f:
#     f.write("我欲乘风归去,\n又恐琼楼玉宇,\n高处不胜寒。")

# 追加内容
# with open("./poem.txt", "a", encoding="utf-8") as f:
#     f.write("起舞弄清影,\n")
#     f.write("何似在人间")


# ==================== 第十五章：测试与调试 ====================
# 【知识点总结】
# 1. assert 语句：用于调试，assert 条件, "错误信息"
# 2. unittest 模块：Python 标准测试库
# 3. 测试方法：setUp()、tearDown()、test_xxx()

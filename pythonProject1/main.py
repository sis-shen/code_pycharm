# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Nginx代理日志分析工具 - 猫娘特别版 🐾
# 使用方法: python3 analyze_nginx_log.py /path/to/your/access.log
# """
#
# import re
# import sys
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime
#
# # 设置猫娘主题风格喵~
# plt.style.use('ggplot')
# sns.set_palette("husl")
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
# plt.rcParams['axes.unicode_minus'] = False
#
# # 日志解析正则表达式
# LOG_PATTERN = r'''
#     (?P<ip>\S+)\s-\s-\s
#     \[(?P<time>.+?)\]\s
#     "(?P<method>\w+)\s
#     (?P<url>\S+)\s
#     (?P<protocol>[\w/\.]+)"\s
#     (?P<status>\d+)\s
#     (?P<size>\d+)\s
#     "(?P<referer>.*?)"\s
#     "(?P<user_agent>.*?)"\s
#     "(?P<forwarded_for>.*?)"\s
#     rt=(?P<rt>\d+\.\d+)\s
#     uct="(?P<uct>\d+\.\d+)"\s
#     urt="(?P<urt>\d+\.\d+)"\s
#     uht="(?P<uht>\d+\.\d+)"\s
#     ups="(?P<ups>\d+)"\s
#     cs=(?P<cs>\d+)\s
#     cs=(?P<cs2>\d+)\s
#     lb=(?P<lb>\S+)
# '''
#
#
# def parse_log_file(file_path):
#     """解析日志文件喵~"""
#     print(f"🐱 开始分析日志文件: {file_path}")
#
#     logs = []
#     with open(file_path, 'r') as f:
#         for i, line in enumerate(f):
#             try:
#                 match = re.match(LOG_PATTERN, line.strip(), re.VERBOSE)
#                 if match:
#                     logs.append(match.groupdict())
#                 else:
#                     print(f"⚠️ 第{i + 1}行无法解析: {line[:50]}...")
#             except Exception as e:
#                 print(f"❌ 第{i + 1}行解析出错: {str(e)}")
#
#     if not logs:
#         print("😿 没有解析到任何有效日志，请检查日志格式！")
#         sys.exit(1)
#
#     return pd.DataFrame(logs)
#
#
# def preprocess_data(df):
#     """数据预处理喵~"""
#     # 转换数据类型
#     numeric_cols = ['status', 'size', 'rt', 'uct', 'urt', 'uht', 'ups', 'cs', 'cs2']
#     df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
#
#     # 解析时间戳
#     df['time'] = pd.to_datetime(
#         df['time'],
#         format='%d/%b/%Y:%H:%M:%S %z',
#         errors='coerce'
#     )
#
#     # 添加时间维度
#     df['hour'] = df['time'].dt.hour
#     df['minute'] = df['time'].dt.minute
#
#     return df.dropna()
#
#
# def generate_plots(df, output_prefix='nginx_analysis'):
#     """生成可视化图表喵~"""
#     print("📊 正在生成分析图表...")
#
#     # 1. 响应时间分布
#     plt.figure(figsize=(12, 6))
#     sns.histplot(df['rt'], bins=20, kde=True)
#     plt.title('🐾 请求响应时间分布', fontsize=15)
#     plt.xlabel('响应时间(秒)')
#     plt.ylabel('请求数量')
#     plt.savefig(f'{output_prefix}_response_time.png', bbox_inches='tight')
#     plt.close()
#
#     # 2. 后端服务器对比
#     plt.figure(figsize=(12, 6))
#     sns.boxplot(x='lb', y='rt', data=df)
#     plt.title('🐱 不同后端服务器的响应时间对比', fontsize=15)
#     plt.xlabel('后端服务器')
#     plt.ylabel('响应时间(秒)')
#     plt.savefig(f'{output_prefix}_backend_comparison.png', bbox_inches='tight')
#     plt.close()
#
#     # 3. 时间趋势分析
#     plt.figure(figsize=(14, 6))
#     df.set_index('time')['rt'].resample('1min').mean().plot()
#     plt.title('⏰ 响应时间分钟级趋势', fontsize=15)
#     plt.ylabel('平均响应时间(秒)')
#     plt.savefig(f'{output_prefix}_time_series.png', bbox_inches='tight')
#     plt.close()
#
#     # 4. 异常请求分析
#     plt.figure(figsize=(12, 6))
#     sns.scatterplot(x='cs', y='rt', hue='lb', data=df, s=100)
#     plt.title('🔍 连接数与响应时间关系', fontsize=15)
#     plt.xlabel('连接数(cs)')
#     plt.ylabel('响应时间(秒)')
#     plt.savefig(f'{output_prefix}_anomaly_detection.png', bbox_inches='tight')
#     plt.close()
#
#
# def generate_report(df, output_file='nginx_report.txt'):
#     """生成文本报告喵~"""
#     print("📝 正在生成分析报告...")
#
#     report = f"""
#     =========== 🐱 Nginx代理日志分析报告 🐱 ===========
#     分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#     日志时间段: {df['time'].min()} ~ {df['time'].max()}
#     --------------------------------------------------
#     总请求数: {len(df):,}
#     成功请求(2xx): {len(df[df['status'].between(200, 299)]):,}
#     平均响应时间: {df['rt'].mean():.3f}秒
#     最快响应: {df['rt'].min():.3f}秒 (URL: {df.loc[df['rt'].idxmin(), 'url']})
#     最慢响应: {df['rt'].max():.3f}秒 (URL: {df.loc[df['rt'].idxmax(), 'url']})
#
#     🐾 后端服务器负载分布:
#     {df['lb'].value_counts().to_string()}
#
#     🚨 异常请求(cs>100):
#     {df[df['cs'] > 100][['time', 'url', 'rt', 'cs', 'lb']].to_string(index=False)}
#
#     ================== 报告结束 ====================
#     """
#
#     with open(output_file, 'w') as f:
#         f.write(report)
#
#     print(f"✅ 报告已保存到: {output_file}")
#
#
# def main():
#     if len(sys.argv) < 2:
#         print("使用方法: python3 analyze_nginx_log.py <日志文件路径>")
#         sys.exit(1)
#
#     log_file = sys.argv[1]
#
#     try:
#         # 1. 解析日志
#         df = parse_log_file(log_file)
#
#         # 2. 数据预处理
#         df = preprocess_data(df)
#
#         # 3. 保存原始数据
#         df.to_csv('nginx_logs_parsed.csv', index=False)
#         print("💾 解析后的数据已保存到: nginx_logs_parsed.csv")
#
#         # 4. 生成可视化图表
#         generate_plots(df)
#
#         # 5. 生成文本报告
#         generate_report(df)
#
#         print("🎉 分析完成！请查看生成的图表和报告文件~")
#
#     except Exception as e:
#         print(f"😿 分析过程中出错: {str(e)}")
#         sys.exit(1)
#
#
# if __name__ == '__main__':
#     main()


# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nginx代理日志分析工具 - 猫娘完整修复版 🐾
使用方法: python3 analyze_nginx_log.py /path/to/your/access.log
"""

import re
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置中文字体
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 宽松版正则表达式
LOG_PATTERN = r'''
    (?P<ip>\S+)\s-\s-\s
    \[(?P<time>.+?)\]\s
    "(?P<method>\w+)\s
    (?P<url>\S+).*?"\s
    (?P<status>\d+)\s
    (?P<size>\d+)\s.*?
    rt=(?P<rt>\d+\.\d+)\s.*?
    uct="(?P<uct>\d+\.\d+)"\s.*?
    urt="(?P<urt>\d+\.\d+)"\s.*?
    lb=(?P<lb>\S+)
'''


def parse_log_file(file_path):
    """解析日志文件喵~"""
    print(f"🐱 开始分析日志文件: {file_path}")

    logs = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            try:
                match = re.match(LOG_PATTERN, line.strip(), re.VERBOSE)
                if match:
                    logs.append(match.groupdict())
                elif i < 10 or i > 26700:  # 只显示部分解析错误
                    print(f"⚠️ 第{i + 1}行无法解析: {line[:50]}...")
            except Exception as e:
                print(f"❌ 第{i + 1}行解析出错: {str(e)}")

    if not logs:
        print("😿 没有解析到任何有效日志，请检查日志格式！")
        sys.exit(1)

    return pd.DataFrame(logs)


def preprocess_data(df):
    """数据预处理喵~（之前漏掉的定义在这里！）"""
    print("🧹 正在清洗数据...")

    # 转换数据类型
    numeric_cols = ['status', 'size', 'rt', 'uct', 'urt']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # 解析时间戳
    df['time'] = pd.to_datetime(
        df['time'],
        format='%d/%b/%Y:%H:%M:%S %z',
        errors='coerce'
    )

    # 添加时间维度
    df['hour'] = df['time'].dt.hour
    df['date'] = df['time'].dt.date

    # 移除无效数据
    return df.dropna(subset=['time', 'rt'])


def generate_plots(df, output_prefix='nginx_analysis'):
    """生成可视化图表喵~"""
    print("📊 正在生成分析图表...")

    # 1. 响应时间分布
    plt.figure(figsize=(12, 6))
    sns.histplot(df['rt'], bins=20, kde=True)
    plt.title('请求响应时间分布', fontsize=15)
    plt.xlabel('响应时间(秒)')
    plt.ylabel('请求数量')
    plt.savefig(f'{output_prefix}_response_time.png')
    plt.close()

    # 2. 按小时请求量
    plt.figure(figsize=(12, 6))
    df['hour'].value_counts().sort_index().plot(kind='bar')
    plt.title('每小时请求量分布')
    plt.savefig(f'{output_prefix}_requests_by_hour.png')
    plt.close()


def generate_report(df, output_file='nginx_report.txt'):
    """生成文本报告喵~"""
    print("📝 正在生成分析报告...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""
        ===== Nginx日志分析报告 =====
        分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ----------------------------
        总请求数: {len(df):,} 
        平均响应时间: {df['rt'].mean():.3f}秒
        峰值时间: {df['hour'].value_counts().idxmax()}时
        最慢请求: {df['rt'].max():.3f}秒
        """)


def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 analyze_nginx_log.py <日志文件路径>")
        sys.exit(1)

    try:
        # 1. 解析日志
        df = parse_log_file(sys.argv[1])

        # 2. 数据预处理
        df = preprocess_data(df)

        # 3. 保存数据
        df.to_csv('nginx_parsed.csv', index=False)
        print("💾 数据已保存到: nginx_parsed.csv")

        # 4. 生成图表和报告
        generate_plots(df)
        generate_report(df)

        print("🎉 分析完成！请查看生成的文件~")

    except Exception as e:
        print(f"😿 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import paramiko
import json
import os
import sqlite3
from datetime import datetime, timedelta
import threading
import time
import statistics

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于session加密

# 数据库文件路径
DB_FILE = 'data/monitor.db'
HISTORY_DB_FILE = 'data/history.db'

# 告警阈值配置
ALERT_THRESHOLDS = {
    'cpu_critical': 90,    # CPU严重告警阈值
    'cpu_warning': 80,     # CPU警告阈值
    'memory_critical': 90, # 内存严重告警阈值
    'memory_warning': 80   # 内存警告阈值
}

# 多语言字典（修复了缺失的键）
LANGUAGES = {
    'zh': {
        # 导航栏
        'nav_dashboard': '监控大屏',
        'nav_alerts': '告警中心',
        'nav_history': '历史数据',
        'nav_statistics': '统计分析',
        
        # 通用
        'refresh': '刷新',
        'save': '保存',
        'cancel': '取消',
        'confirm': '确认',
        'online': '在线',
        'offline': '离线',
        'cpu': 'CPU',
        'memory': '内存',
        'status': '状态',
        'time': '时间',
        'server': '服务器',
        'operation': '操作',
        'warning': '警告',
        'critical': '严重',
        'resolved': '已解决',
        'active': '活跃',
        
        # 首页
        'add_monitored_host': '添加被监控主机',
        'ip_address': 'IP地址',
        'username': '用户名',
        'password': '密码',
        'ssh_port': 'SSH端口',
        'add_host': '添加主机',
        'host_list': '主机列表',
        'server_status_overview': '服务器状态概览',
        'online_servers': '在线服务器',
        'offline_servers': '离线服务器',
        'total_servers': '总服务器',
        'resource_usage_overview': '资源使用概览',
        'avg_cpu_usage': '平均CPU使用率',
        'avg_memory_usage': '平均内存使用率',
        'real_time_monitoring': '实时监控数据',
        'last_update': '最后更新',
        'monitoring_charts': '监控图表',
        'cpu_usage': 'CPU使用率',
        'memory_usage': '内存使用率',
        'server_status_distribution': '服务器状态分布',
        'overall_resource_usage': '整体资源使用率',
        'collect_all_data': '采集所有数据',
        'collect_data': '采集数据',
        'delete': '删除',
        'detailed_data': '查看详情',
        'data_auto_refresh': '数据自动刷新',
        'real_time_charts': '实时图表',
        
        # 告警中心
        'alert_center': '告警中心',
        'alert_threshold_config': '告警阈值配置',
        'update_thresholds': '更新阈值',
        'cpu_warning_threshold': 'CPU警告阈值 (%)',
        'cpu_critical_threshold': 'CPU严重告警阈值 (%)',
        'memory_warning_threshold': '内存警告阈值 (%)',
        'memory_critical_threshold': '内存严重告警阈值 (%)',
        'current_alerts': '当前告警',
        'alert_statistics': '告警统计',
        'critical_alerts': '严重告警',
        'total_alerts': '总告警',
        'alert_type_distribution': '告警类型分布',
        'alert_trend': '告警趋势',
        'alert_history': '告警历史',
        'show_resolved': '显示已解决',
        'alert_level': '级别',
        'message': '消息',
        'value_threshold': '值/阈值',
        'mark_resolved': '标记为已解决',
        'no_active_alerts': '暂无活跃告警',
        'all_systems_normal': '所有系统运行正常',
        'recent_7_days': '最近7天',
        'confirm_resolve_alert': '确认标记此告警为已解决吗？',
        'threshold_update_success': '阈值更新成功！',
        'threshold_update_failed': '阈值更新失败',
        'fetch_alert_data_failed': '获取告警数据失败',
        'no_alert_history': '无告警历史',
        'current_value': '当前值',
        
        # 历史数据
        'history_data': '历史数据',
        'history_data_query': '历史数据查询',
        'search_conditions': '查询条件',
        'select_server': '选择服务器',
        'time_range': '时间范围',
        'chart_type': '图表类型',
        'line_chart': '折线图',
        'bar_chart': '柱状图',
        'area_chart': '面积图',
        'query_data': '查询数据',
        'statistical_overview': '统计概览',
        'avg_cpu_usage_rate': '平均CPU使用率',
        'max_cpu_usage_rate': '最高CPU使用率',
        'avg_memory_usage_rate': '平均内存使用率',
        'max_memory_usage_rate': '最高内存使用率',
        'historical_trend_charts': '历史趋势图表',
        'cpu_usage_history_trend': 'CPU使用率历史趋势',
        'memory_usage_history_trend': '内存使用率历史趋势',
        'detailed_data': '详细数据',
        'no_history_data': '无历史数据',
        'no_matching_history_data': '没有匹配的历史数据',
        'load_host_list_failed': '加载主机列表失败',
        'select_server_prompt': '请先选择服务器',
        'load_history_data_failed': '加载历史数据失败',
        'display_recent_records': '显示最近',
        'total_records': '总记录数',
        'records': '条记录',
        
        # 统计分析
        'statistical_analysis': '统计分析',
        'analysis_conditions': '分析条件',
        'analysis_period': '分析周期',
        'metric_type': '指标类型',
        'both_cpu_memory': 'CPU和内存',
        'cpu_only': '仅CPU',
        'memory_only': '仅内存',
        'generate_report': '生成分析报告',
        'export_report': '导出报告',
        'detailed_statistical_analysis': '详细统计分析',
        'resource_usage_statistics': '资源使用统计',
        'usage_distribution': '使用率分布',
        'hourly_trend_analysis': '小时趋势分析',
        'performance_comparison_analysis': '性能对比分析',
        'statistical_details': '统计明细',
        'average_value': '平均值',
        'maximum_value': '最大值',
        'minimum_value': '最小值',
        'median_value': '中位数',
        'data_points': '数据点数',
        'analysis_description': '分析说明',
        'data_points_count': '个有效数据点',
        'based_on_monitoring_data': '基于监控数据',
        'days_data': '天的数据',
        'high_usage_detected': '检测到资源使用率较高，请关注。',
        'good_resource_usage': '资源使用情况良好。',
        'server_monitoring_statistical_report': '服务器监控统计报告',
        'generation_time': '生成时间',
        'print_report': '打印报告',
        'close': '关闭',
        'load_statistics_failed': '加载统计数据失败',
        'no_statistics_data': '无统计数据',
        'no_matching_statistics_data': '没有匹配的统计数据',
        'select_server_first': '请先选择服务器',
        'select_server_placeholder': '请选择服务器',
        
        # 时间范围选项
        'last_1_hour': '最近1小时',
        'last_6_hours': '最近6小时',
        'last_24_hours': '最近24小时',
        'last_3_days': '最近3天',
        'last_7_days': '最近7天',
        'last_1_day': '最近1天',
        'last_30_days': '最近30天',
        
        # 统计分析特定
        'avg_cpu': '平均CPU',
        'avg_memory': '平均内存',
        'max_cpu': '最大CPU',
        'max_memory': '最大内存',
        'high': '高',
        'medium': '中',
        'low': '低',
        'cpu_median': 'CPU中位数',
        'performance_metrics': '性能指标',
        'avg_usage_rate': '平均使用率',
        'peak_usage_rate': '峰值使用率',
        'stability': '稳定性',
        'load_variation': '负载变化',
        'alert_frequency': '告警频率',
        'statistical_indicator': '统计指标',
        'average_usage_description': '统计周期内的平均使用率',
        'peak_usage_description': '统计周期内的峰值使用率',
        'min_usage_description': '统计周期内的最低使用率',
        'median_usage_description': '统计周期内的中位数使用率'
    },
    'en': {
        # Navigation
        'nav_dashboard': 'Dashboard',
        'nav_alerts': 'Alerts',
        'nav_history': 'History',
        'nav_statistics': 'Statistics',
        
        # Common
        'refresh': 'Refresh',
        'save': 'Save',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        'online': 'Online',
        'offline': 'Offline',
        'cpu': 'CPU',
        'memory': 'Memory',
        'status': 'Status',
        'time': 'Time',
        'server': 'Server',
        'operation': 'Operation',
        'warning': 'Warning',
        'critical': 'Critical',
        'resolved': 'Resolved',
        'active': 'Active',
        
        # Dashboard
        'add_monitored_host': 'Add Monitored Host',
        'ip_address': 'IP Address',
        'username': 'Username',
        'password': 'Password',
        'ssh_port': 'SSH Port',
        'add_host': 'Add Host',
        'host_list': 'Host List',
        'server_status_overview': 'Server Status Overview',
        'online_servers': 'Online Servers',
        'offline_servers': 'Offline Servers',
        'total_servers': 'Total Servers',
        'resource_usage_overview': 'Resource Usage Overview',
        'avg_cpu_usage': 'Average CPU Usage',
        'avg_memory_usage': 'Average Memory Usage',
        'real_time_monitoring': 'Real-time Monitoring',
        'last_update': 'Last Update',
        'monitoring_charts': 'Monitoring Charts',
        'cpu_usage': 'CPU Usage',
        'memory_usage': 'Memory Usage',
        'server_status_distribution': 'Server Status Distribution',
        'overall_resource_usage': 'Overall Resource Usage',
        'collect_all_data': 'Collect All Data',
        'collect_data': 'Collect Data',
        'delete': 'Delete',
        'detailed_data': 'View Details',
        'data_auto_refresh': 'Data Auto Refresh',
        'real_time_charts': 'Real-time Charts',
        
        # Alerts
        'alert_center': 'Alert Center',
        'alert_threshold_config': 'Alert Threshold Configuration',
        'update_thresholds': 'Update Thresholds',
        'cpu_warning_threshold': 'CPU Warning Threshold (%)',
        'cpu_critical_threshold': 'CPU Critical Threshold (%)',
        'memory_warning_threshold': 'Memory Warning Threshold (%)',
        'memory_critical_threshold': 'Memory Critical Threshold (%)',
        'current_alerts': 'Current Alerts',
        'alert_statistics': 'Alert Statistics',
        'critical_alerts': 'Critical Alerts',
        'total_alerts': 'Total Alerts',
        'alert_type_distribution': 'Alert Type Distribution',
        'alert_trend': 'Alert Trend',
        'alert_history': 'Alert History',
        'show_resolved': 'Show Resolved',
        'alert_level': 'Level',
        'message': 'Message',
        'value_threshold': 'Value/Threshold',
        'mark_resolved': 'Mark as Resolved',
        'no_active_alerts': 'No Active Alerts',
        'all_systems_normal': 'All Systems Running Normally',
        'recent_7_days': 'Recent 7 Days',
        'confirm_resolve_alert': 'Confirm to mark this alert as resolved?',
        'threshold_update_success': 'Threshold updated successfully!',
        'threshold_update_failed': 'Failed to update threshold',
        'fetch_alert_data_failed': 'Failed to fetch alert data',
        'no_alert_history': 'No Alert History',
        'current_value': 'Current Value',
        
        # History
        'history_data': 'History Data',
        'history_data_query': 'History Data Query',
        'search_conditions': 'Search Conditions',
        'select_server': 'Select Server',
        'time_range': 'Time Range',
        'chart_type': 'Chart Type',
        'line_chart': 'Line Chart',
        'bar_chart': 'Bar Chart',
        'area_chart': 'Area Chart',
        'query_data': 'Query Data',
        'statistical_overview': 'Statistical Overview',
        'avg_cpu_usage_rate': 'Average CPU Usage',
        'max_cpu_usage_rate': 'Maximum CPU Usage',
        'avg_memory_usage_rate': 'Average Memory Usage',
        'max_memory_usage_rate': 'Maximum Memory Usage',
        'historical_trend_charts': 'Historical Trend Charts',
        'cpu_usage_history_trend': 'CPU Usage History Trend',
        'memory_usage_history_trend': 'Memory Usage History Trend',
        'detailed_data': 'Detailed Data',
        'no_history_data': 'No History Data',
        'no_matching_history_data': 'No matching history data',
        'load_host_list_failed': 'Failed to load host list',
        'select_server_prompt': 'Please select a server first',
        'load_history_data_failed': 'Failed to load history data',
        'display_recent_records': 'Showing recent',
        'total_records': 'total records',
        'records': 'records',
        
        # Statistics
        'statistical_analysis': 'Statistical Analysis',
        'analysis_conditions': 'Analysis Conditions',
        'analysis_period': 'Analysis Period',
        'metric_type': 'Metric Type',
        'both_cpu_memory': 'Both CPU and Memory',
        'cpu_only': 'CPU Only',
        'memory_only': 'Memory Only',
        'generate_report': 'Generate Report',
        'export_report': 'Export Report',
        'detailed_statistical_analysis': 'Detailed Statistical Analysis',
        'resource_usage_statistics': 'Resource Usage Statistics',
        'usage_distribution': 'Usage Distribution',
        'hourly_trend_analysis': 'Hourly Trend Analysis',
        'performance_comparison_analysis': 'Performance Comparison Analysis',
        'statistical_details': 'Statistical Details',
        'average_value': 'Average',
        'maximum_value': 'Maximum',
        'minimum_value': 'Minimum',
        'median_value': 'Median',
        'data_points': 'Data Points',
        'analysis_description': 'Analysis Description',
        'data_points_count': 'valid data points',
        'based_on_monitoring_data': 'Based on monitoring data',
        'days_data': 'days of data',
        'high_usage_detected': 'High resource usage detected, please pay attention.',
        'good_resource_usage': 'Resource usage is good.',
        'server_monitoring_statistical_report': 'Server Monitoring Statistical Report',
        'generation_time': 'Generation Time',
        'print_report': 'Print Report',
        'close': 'Close',
        'load_statistics_failed': 'Failed to load statistics',
        'no_statistics_data': 'No Statistics Data',
        'no_matching_statistics_data': 'No matching statistics data',
        'select_server_first': 'Please select a server first',
        'select_server_placeholder': 'Please select a server',
        
        # Time range options
        'last_1_hour': 'Last 1 Hour',
        'last_6_hours': 'Last 6 Hours',
        'last_24_hours': 'Last 24 Hours',
        'last_3_days': 'Last 3 Days',
        'last_7_days': 'Last 7 Days',
        'last_1_day': 'Last 1 Day',
        'last_30_days': 'Last 30 Days',
        
        # Statistics specific
        'avg_cpu': 'Avg CPU',
        'avg_memory': 'Avg Memory',
        'max_cpu': 'Max CPU',
        'max_memory': 'Max Memory',
        'high': 'High',
        'medium': 'Medium',
        'low': 'Low',
        'cpu_median': 'CPU Median',
        'performance_metrics': 'Performance Metrics',
        'avg_usage_rate': 'Average Usage Rate',
        'peak_usage_rate': 'Peak Usage Rate',
        'stability': 'Stability',
        'load_variation': 'Load Variation',
        'alert_frequency': 'Alert Frequency',
        'statistical_indicator': 'Statistical Indicator',
        'average_usage_description': 'Average usage during the statistical period',
        'peak_usage_description': 'Peak usage during the statistical period',
        'min_usage_description': 'Minimum usage during the statistical period',
        'median_usage_description': 'Median usage during the statistical period'
    }
}

# 确保数据目录存在
os.makedirs('data', exist_ok=True)

def init_databases():
    """初始化数据库"""
    # 主监控数据库
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS hosts
        (ip TEXT PRIMARY KEY, user TEXT, pwd TEXT, port INTEGER, added_time TEXT)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics
        (ip TEXT PRIMARY KEY, cpu REAL, memory REAL, status TEXT, 
         last_update TEXT, FOREIGN KEY(ip) REFERENCES hosts(ip))
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts
        (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, alert_type TEXT, 
         alert_level TEXT, value REAL, threshold REAL, message TEXT,
         alert_time TEXT, resolved INTEGER DEFAULT 0,
         FOREIGN KEY(ip) REFERENCES hosts(ip))
    ''')
    conn.commit()
    conn.close()

    # 历史数据数据库
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history
        (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, cpu REAL, memory REAL, 
         status TEXT, timestamp TEXT, FOREIGN KEY(ip) REFERENCES hosts(ip))
    ''')
    conn.commit()
    conn.close()

def load_hosts():
    """加载主机列表"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM hosts")
    hosts = [{'ip': row[0], 'user': row[1], 'pwd': row[2], 'port': row[3], 'added_time': row[4]} 
             for row in c.fetchall()]
    conn.close()
    return hosts

def save_hosts(hosts):
    """保存主机列表"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM hosts")
    for host in hosts:
        c.execute("INSERT INTO hosts VALUES (?, ?, ?, ?, ?)",
                  (host['ip'], host['user'], host['pwd'], host['port'], host['added_time']))
    conn.commit()
    conn.close()

def save_metrics(metrics):
    """保存监控数据"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM metrics")
    for ip, data in metrics.items():
        c.execute("INSERT INTO metrics VALUES (?, ?, ?, ?, ?)",
                  (ip, data['cpu'], data['memory'], data['status'], data['last_update']))
    conn.commit()
    conn.close()

def load_metrics():
    """加载监控数据"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM metrics")
    metrics = {}
    for row in c.fetchall():
        metrics[row[0]] = {
            'cpu': row[1],
            'memory': row[2],
            'status': row[3],
            'last_update': row[4]
        }
    conn.close()
    return metrics

def save_history_metrics(metrics):
    """保存历史监控数据"""
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for ip, data in metrics.items():
        c.execute("INSERT INTO history (ip, cpu, memory, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (ip, data['cpu'], data['memory'], data['status'], timestamp))
    
    # 清理30天前的历史数据
    cutoff_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("DELETE FROM history WHERE timestamp < ?", (cutoff_time,))
    
    conn.commit()
    conn.close()

def check_alerts(ip, metrics_data):
    """检查告警条件"""
    alerts = []
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cpu = metrics_data['cpu']
    memory = metrics_data['memory']
    
    # 检查CPU告警
    if cpu >= ALERT_THRESHOLDS['cpu_critical']:
        alerts.append({
            'ip': ip,
            'alert_type': 'cpu',
            'alert_level': 'critical',
            'value': cpu,
            'threshold': ALERT_THRESHOLDS['cpu_critical'],
            'message': f'CPU使用率过高: {cpu}%' if session.get('language', 'zh') == 'zh' else f'CPU usage too high: {cpu}%',
            'alert_time': current_time
        })
    elif cpu >= ALERT_THRESHOLDS['cpu_warning']:
        alerts.append({
            'ip': ip,
            'alert_type': 'cpu',
            'alert_level': 'warning',
            'value': cpu,
            'threshold': ALERT_THRESHOLDS['cpu_warning'],
            'message': f'CPU使用率警告: {cpu}%' if session.get('language', 'zh') == 'zh' else f'CPU usage warning: {cpu}%',
            'alert_time': current_time
        })
    
    # 检查内存告警
    if memory >= ALERT_THRESHOLDS['memory_critical']:
        alerts.append({
            'ip': ip,
            'alert_type': 'memory',
            'alert_level': 'critical',
            'value': memory,
            'threshold': ALERT_THRESHOLDS['memory_critical'],
            'message': f'内存使用率过高: {memory}%' if session.get('language', 'zh') == 'zh' else f'Memory usage too high: {memory}%',
            'alert_time': current_time
        })
    elif memory >= ALERT_THRESHOLDS['memory_warning']:
        alerts.append({
            'ip': ip,
            'alert_type': 'memory',
            'alert_level': 'warning',
            'value': memory,
            'threshold': ALERT_THRESHOLDS['memory_warning'],
            'message': f'内存使用率警告: {memory}%' if session.get('language', 'zh') == 'zh' else f'Memory usage warning: {memory}%',
            'alert_time': current_time
        })
    
    # 检查服务器状态
    if metrics_data['status'] == 'offline':
        alerts.append({
            'ip': ip,
            'alert_type': 'status',
            'alert_level': 'critical',
            'value': 0,
            'threshold': 0,
            'message': '服务器离线' if session.get('language', 'zh') == 'zh' else 'Server offline',
            'alert_time': current_time
        })
    
    return alerts

def save_alerts(alerts):
    """保存告警信息"""
    if not alerts:
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    for alert in alerts:
        # 检查是否已存在相同告警（未解决的）
        c.execute('''SELECT id FROM alerts WHERE ip=? AND alert_type=? AND alert_level=? 
                     AND resolved=0 AND alert_time > ?''',
                  (alert['ip'], alert['alert_type'], alert['alert_level'], 
                   (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')))
        
        if not c.fetchone():  # 如果没有重复告警，则插入新告警
            c.execute('''INSERT INTO alerts 
                         (ip, alert_type, alert_level, value, threshold, message, alert_time) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (alert['ip'], alert['alert_type'], alert['alert_level'],
                       alert['value'], alert['threshold'], alert['message'], alert['alert_time']))
    
    conn.commit()
    conn.close()

def get_active_alerts():
    """获取未解决的告警"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM alerts WHERE resolved=0 ORDER BY alert_time DESC")
    alerts = [{
        'id': row[0],
        'ip': row[1],
        'alert_type': row[2],
        'alert_level': row[3],
        'value': row[4],
        'threshold': row[5],
        'message': row[6],
        'alert_time': row[7]
    } for row in c.fetchall()]
    conn.close()
    return alerts

def get_alert_history(days=7):
    """获取历史告警"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    cutoff_time = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("SELECT * FROM alerts WHERE alert_time >= ? ORDER BY alert_time DESC", (cutoff_time,))
    alerts = [{
        'id': row[0],
        'ip': row[1],
        'alert_type': row[2],
        'alert_level': row[3],
        'value': row[4],
        'threshold': row[5],
        'message': row[6],
        'alert_time': row[7],
        'resolved': row[8]
    } for row in c.fetchall()]
    conn.close()
    return alerts

def collect_metrics(host):
    """通过SSH收集监控数据"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接SSH
        ssh.connect(
            hostname=host['ip'],
            username=host['user'],
            password=host['pwd'],
            port=host.get('port', 22),
            timeout=10
        )
        
        # 获取CPU使用率
        stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
        cpu_usage = stdout.read().decode().strip()
        
        # 获取内存使用率
        stdin, stdout, stderr = ssh.exec_command("free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'")
        mem_usage = stdout.read().decode().strip()
        
        ssh.close()
        
        cpu_value = float(cpu_usage) if cpu_usage and cpu_usage.replace('.', '').isdigit() else 0
        memory_value = float(mem_usage) if mem_usage and mem_usage.replace('.', '').isdigit() else 0
        
        return {
            'cpu': cpu_value,
            'memory': memory_value,
            'status': 'online',
            'last_update': datetime.now().strftime('%Y-%m-d %H:%M:%S')
        }
    except Exception as e:
        return {
            'cpu': 0,
            'memory': 0,
            'status': 'offline',
            'error': str(e),
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def get_history_data(ip, hours=24):
    """获取历史数据"""
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()
    cutoff_time = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute('''SELECT timestamp, cpu, memory, status FROM history 
                 WHERE ip=? AND timestamp >= ? ORDER BY timestamp''', (ip, cutoff_time))
    
    history = []
    for row in c.fetchall():
        history.append({
            'timestamp': row[0],
            'cpu': row[1],
            'memory': row[2],
            'status': row[3]
        })
    
    conn.close()
    return history

def get_statistics_data(ip, days=7):
    """获取统计数据：平均值、峰值等"""
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()
    cutoff_time = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    
    # 获取CPU和内存数据
    c.execute('''SELECT cpu, memory FROM history 
                 WHERE ip=? AND timestamp >= ? AND status='online' 
                 ORDER BY timestamp''', (ip, cutoff_time))
    
    data = c.fetchall()
    if not data:
        conn.close()
        return None
    
    cpu_data = [row[0] for row in data if row[0] > 0]
    memory_data = [row[1] for row in data if row[1] > 0]
    
    # 计算统计数据
    stats = {
        'cpu': {
            'avg': round(statistics.mean(cpu_data) if cpu_data else 0, 2),
            'max': round(max(cpu_data) if cpu_data else 0, 2),
            'min': round(min(cpu_data) if cpu_data else 0, 2),
            'median': round(statistics.median(cpu_data) if cpu_data else 0, 2),
            'count': len(cpu_data)
        },
        'memory': {
            'avg': round(statistics.mean(memory_data) if memory_data else 0, 2),
            'max': round(max(memory_data) if memory_data else 0, 2),
            'min': round(min(memory_data) if memory_data else 0, 2),
            'median': round(statistics.median(memory_data) if memory_data else 0, 2),
            'count': len(memory_data)
        }
    }
    
    # 获取按小时聚合的数据用于趋势分析
    c.execute('''SELECT 
                    strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
                    AVG(cpu), AVG(memory), 
                    MAX(cpu), MAX(memory)
                 FROM history 
                 WHERE ip=? AND timestamp >= ? AND status='online'
                 GROUP BY hour
                 ORDER BY hour''', (ip, cutoff_time))
    
    hourly_data = []
    for row in c.fetchall():
        hourly_data.append({
            'hour': row[0],
            'avg_cpu': round(row[1] or 0, 2),
            'avg_memory': round(row[2] or 0, 2),
            'max_cpu': round(row[3] or 0, 2),
            'max_memory': round(row[4] or 0, 2)
        })
    
    conn.close()
    
    return {
        'stats': stats,
        'hourly_data': hourly_data,
        'period_days': days
    }

def auto_collect_metrics():
    """自动采集所有主机的数据"""
    while True:
        try:
            hosts = load_hosts()
            if not hosts:
                time.sleep(30)
                continue
                
            metrics = {}
            all_alerts = []
            
            for host in hosts:
                host_metrics = collect_metrics(host)
                metrics[host['ip']] = host_metrics
                
                # 检查告警
                alerts = check_alerts(host['ip'], host_metrics)
                all_alerts.extend(alerts)
            
            # 保存监控数据和告警
            save_metrics(metrics)
            save_history_metrics(metrics)
            save_alerts(all_alerts)
            
            print(f"自动采集完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"自动采集出错: {e}")
        
        # 每30秒采集一次
        time.sleep(30)

# 初始化数据库
init_databases()

# 启动自动采集线程
auto_collect_thread = threading.Thread(target=auto_collect_metrics, daemon=True)
auto_collect_thread.start()

@app.route('/')
def index():
    """主页 - 显示主机列表和监控数据"""
    hosts = load_hosts()
    active_alerts = get_active_alerts()
    language = session.get('language', 'zh')
    return render_template('index.html', 
                         hosts=hosts, 
                         active_alerts=active_alerts,
                         language=language,
                         lang=LANGUAGES[language])

@app.route('/alerts')
def alerts_page():
    """告警页面"""
    active_alerts = get_active_alerts()
    alert_history = get_alert_history(7)  # 最近7天的告警历史
    language = session.get('language', 'zh')
    return render_template('alerts.html', 
                         active_alerts=active_alerts, 
                         alert_history=alert_history,
                         thresholds=ALERT_THRESHOLDS,
                         language=language,
                         lang=LANGUAGES[language])

@app.route('/history')
def history_page():
    """历史数据页面"""
    hosts = load_hosts()
    language = session.get('language', 'zh')
    return render_template('history.html', 
                         hosts=hosts,
                         language=language,
                         lang=LANGUAGES[language])

@app.route('/statistics')
def statistics_page():
    """统计分析页面"""
    hosts = load_hosts()
    language = session.get('language', 'zh')
    return render_template('statistics.html', 
                         hosts=hosts,
                         language=language,
                         lang=LANGUAGES[language])

@app.route('/set_language/<language>')
def set_language(language):
    """设置语言"""
    if language in ['zh', 'en']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/add_host', methods=['POST'])
def add_host():
    """添加主机"""
    ip = request.form.get('ip')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    port = request.form.get('port', 22)
    
    if ip and user and pwd:
        hosts = load_hosts()
        
        # 检查是否已存在
        for host in hosts:
            if host['ip'] == ip:
                return "主机已存在", 400
        
        new_host = {
            'ip': ip,
            'user': user,
            'pwd': pwd,
            'port': int(port),
            'added_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        hosts.append(new_host)
        save_hosts(hosts)
    
    return redirect(url_for('index'))

@app.route('/delete_host/<ip>')
def delete_host(ip):
    """删除主机"""
    hosts = load_hosts()
    hosts = [host for host in hosts if host['ip'] != ip]
    save_hosts(hosts)
    
    # 同时删除对应的监控数据和告警
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM metrics WHERE ip=?", (ip,))
    c.execute("DELETE FROM alerts WHERE ip=?", (ip,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/collect/<ip>')
def collect_data(ip):
    """手动采集指定主机的数据"""
    hosts = load_hosts()
    target_host = None
    
    for host in hosts:
        if host['ip'] == ip:
            target_host = host
            break
    
    if target_host:
        metrics = load_metrics()
        host_metrics = collect_metrics(target_host)
        metrics[ip] = host_metrics
        
        # 检查告警
        alerts = check_alerts(ip, host_metrics)
        save_alerts(alerts)
        
        save_metrics(metrics)
        save_history_metrics({ip: host_metrics})
    
    return redirect(url_for('index'))

@app.route('/collect_all')
def collect_all():
    """采集所有主机的数据"""
    hosts = load_hosts()
    metrics = load_metrics()
    all_alerts = []
    
    for host in hosts:
        host_metrics = collect_metrics(host)
        metrics[host['ip']] = host_metrics
        
        # 检查告警
        alerts = check_alerts(host['ip'], host_metrics)
        all_alerts.extend(alerts)
    
    save_metrics(metrics)
    save_history_metrics(metrics)
    save_alerts(all_alerts)
    
    return redirect(url_for('index'))

@app.route('/resolve_alert/<int:alert_id>')
def resolve_alert(alert_id):
    """解决告警"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE alerts SET resolved=1 WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('alerts_page'))

@app.route('/api/metrics')
def api_metrics():
    """API接口：获取所有监控数据"""
    return jsonify(load_metrics())

@app.route('/api/hosts')
def api_hosts():
    """API接口：获取所有主机"""
    return jsonify(load_hosts())

@app.route('/api/alerts')
def api_alerts():
    """API接口：获取告警信息"""
    return jsonify({
        'active_alerts': get_active_alerts(),
        'alert_history': get_alert_history(1)  # 最近1天的告警历史
    })

@app.route('/api/history/<ip>')
def api_history(ip):
    """API接口：获取历史数据"""
    hours = request.args.get('hours', 24, type=int)
    history_data = get_history_data(ip, hours)
    return jsonify(history_data)

@app.route('/api/statistics/<ip>')
def api_statistics(ip):
    """API接口：获取统计数据"""
    days = request.args.get('days', 7, type=int)
    stats_data = get_statistics_data(ip, days)
    return jsonify(stats_data)

@app.route('/api/thresholds', methods=['GET', 'POST'])
def api_thresholds():
    """API接口：获取或更新告警阈值"""
    global ALERT_THRESHOLDS
    
    if request.method == 'POST':
        new_thresholds = request.json
        ALERT_THRESHOLDS.update(new_thresholds)
        return jsonify({'status': 'success', 'thresholds': ALERT_THRESHOLDS})
    
    return jsonify(ALERT_THRESHOLDS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
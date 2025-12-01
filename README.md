# 🖥️ 服务器监控系统

> 一个现代化、功能全面的服务器监控解决方案，通过SSH连接远程服务器，提供实时监控、智能告警和深度数据分析。

https://img.shields.io/badge/license-MIT-blue.svg
[https://img.shields.io/badge/python-3.8%252B-green.svg](https://img.shields.io/badge/python-3.8%2B-green.svg)
[https://img.shields.io/badge/flask-2.0%252B-lightgrey.svg](https://img.shields.io/badge/flask-2.0%2B-lightgrey.svg)
https://img.shields.io/badge/docker-ready-blue.svg

## ✨ 核心特性

### 🚀 实时监控

- **多服务器管理** - 同时监控多台服务器的运行状态
- **实时数据采集** - 每30秒自动采集CPU和内存使用率
- **状态可视化** - 直观的在线/离线状态指示
- **手动采集** - 支持即时手动数据采集

### 📊 高级可视化

- **动态图表** - 使用ECharts提供流畅的图表体验
- **多种图表类型** - 折线图、柱状图、面积图、饼图、仪表盘
- **响应式设计** - 完美适配桌面和移动设备
- **实时更新** - 图表数据自动刷新

### 🔔 智能告警系统

- **阈值配置** - 可自定义CPU和内存告警阈值
- **多级告警** - 警告级别（80%）和严重级别（90%）
- **告警统计** - 告警类型分布和趋势分析
- **历史记录** - 完整的告警历史追踪

### 📈 深度分析

- **历史查询** - 支持按时间范围查询历史数据
- **统计分析** - 平均值、最大值、最小值、中位数计算
- **趋势分析** - 小时级趋势图表和性能对比
- **报告导出** - 支持分析报告导出和打印

### 🌍 国际化支持

- **多语言界面** - 完整的中文和英文支持
- **实时切换** - 无需刷新页面即可切换语言
- **本地化提示** - 所有提示信息均已本地化

## 🛠️ 技术架构

### 后端技术栈

- **Framework**: Flask 2.0+
- **SSH Client**: Paramiko
- **Database**: SQLite3
- **Data Processing**: Statistics, Threading
- **API**: RESTful API设计

### 前端技术栈

- **UI Framework**: Bootstrap 5.3
- **Charts**: ECharts 5.4
- **Icons**: Bootstrap Icons
- **Responsive**: 移动端优先设计

### 部署方案

- **Containerization**: Docker + Docker Compose
- **Data Persistence**: Volume Mounting
- **Process Management**: 自动重启机制

## 🗂️ 项目结构

bash

```
server-monitor/
├── 📁 app/                    # 应用核心
│   ├── app.py                # Flask主应用
│   ├── 📁 templates/         # 前端模板
│   │   ├── index.html        # 监控大屏
│   │   ├── alerts.html       # 告警中心
│   │   ├── history.html      # 历史数据
│   │   └── statistics.html   # 统计分析
│   └── 📁 data/              # 数据存储
│       ├── monitor.db        # 主数据库
│       └── history.db        # 历史数据库
├── 📁 config/                # 配置文件
│   ├── hosts.json           # 主机配置
│   └── metrics.json         # 监控指标配置
├── 📁 docs/                  # 文档资料
├── Dockerfile               # Docker构建文件
├── docker-compose.yml       # 容器编排
├── requirements.txt         # Python依赖
└── README.md               # 项目说明
```



## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **或 Docker**: 20.10+ 和 Docker Compose
- **浏览器**: Chrome 90+, Firefox 88+, Safari 14+

### 方法一：Docker部署（推荐）

#### 1. 克隆项目

bash

```
git clone https://github.com/your-username/server-monitor.git
cd server-monitor
```



#### 2. 配置监控主机

编辑 `config/hosts.json` 文件：

json

```
[
  {
    "ip": "192.168.1.100",
    "user": "root",
    "pwd": "secure-password-123",
    "port": 22,
    "added_time": "2024-01-01 12:00:00",
    "description": "生产Web服务器"
  },
  {
    "ip": "192.168.1.101", 
    "user": "admin",
    "pwd": "another-secure-password",
    "port": 2222,
    "added_time": "2024-01-01 12:05:00",
    "description": "数据库服务器"
  }
]
```



#### 3. 启动服务

bash

```
# 使用Docker Compose启动
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f monitor-app
```



#### 4. 访问应用

打开浏览器访问：`http://localhost:5000`

### 方法二：传统部署

#### 1. 安装依赖

bash

```
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装Python依赖
pip install -r requirements.txt
```



#### 2. 配置环境

bash

```
# 创建必要目录
mkdir -p data templates config

# 设置环境变量（可选）
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
```



#### 3. 启动应用

bash

```
# 开发模式（带热重载）
python app.py

# 或使用生产WSGI服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```



#### 4. 访问应用

打开浏览器访问：`http://localhost:5000`

## 📖 详细使用指南

### 1. 监控大屏（Dashboard）

**功能概述**：

- 实时查看所有服务器状态
- 资源使用率概览
- 动态图表展示
- 快速操作入口

**主要操作**：

- 🟢 点击刷新按钮更新数据
- 🔄 点击单个服务器的采集按钮进行手动采集
- 📊 查看实时更新的图表数据
- ⚠️ 关注告警横幅及时处理问题

### 2. 告警中心（Alerts）

**功能概述**：

- 当前活跃告警显示
- 告警阈值配置
- 告警统计和趋势
- 告警历史记录

**配置说明**：

yaml

```
# 默认告警阈值
CPU:
  警告: 80%
  严重: 90%
内存:
  警告: 80% 
  严重: 90%
```



**操作指南**：

1. 在阈值配置区域调整告警阈值
2. 点击"更新阈值"保存配置
3. 查看当前告警列表
4. 对已处理告警点击"标记为已解决"

### 3. 历史数据（History）

**功能概述**：

- 按时间范围查询历史数据
- 多种图表类型选择
- 统计概览显示
- 详细数据表格

**查询选项**：

- ⏰ 时间范围：1小时、6小时、24小时、3天、7天
- 📈 图表类型：折线图、柱状图、面积图
- 🖥️ 服务器选择：下拉选择特定服务器

### 4. 统计分析（Statistics）

**功能概述**：

- 深度性能分析
- 多维度统计指标
- 趋势分析和预测
- 报告导出功能

**分析维度**：

- 📊 基础统计：平均值、最大值、最小值、中位数
- 📈 趋势分析：小时级使用率趋势
- 🎯 性能对比：多指标雷达图分析
- 📋 分布统计：使用率区间分布

## 🔌 API接口文档

### 监控数据接口

| 端点           | 方法 | 描述             | 参数 |
| :------------- | :--- | :--------------- | :--- |
| `/api/metrics` | GET  | 获取所有监控数据 | 无   |
| `/api/hosts`   | GET  | 获取主机列表     | 无   |
| `/api/alerts`  | GET  | 获取告警信息     | 无   |

### 历史数据接口

| 端点                   | 方法 | 描述         | 参数           |
| :--------------------- | :--- | :----------- | :------------- |
| `/api/history/<ip>`    | GET  | 获取历史数据 | `hours` (可选) |
| `/api/statistics/<ip>` | GET  | 获取统计数据 | `days` (可选)  |

### 配置管理接口

| 端点              | 方法 | 描述         | 参数     |
| :---------------- | :--- | :----------- | :------- |
| `/api/thresholds` | GET  | 获取告警阈值 | 无       |
| `/api/thresholds` | POST | 更新告警阈值 | JSON数据 |

**示例请求**：

bash

```
# 获取历史数据（最近24小时）
curl "http://localhost:5000/api/history/192.168.1.100?hours=24"

# 更新告警阈值
curl -X POST "http://localhost:5000/api/thresholds" \
  -H "Content-Type: application/json" \
  -d '{"cpu_warning": 85, "cpu_critical": 95}'
```



## ⚙️ 配置说明

### 环境变量配置

bash

```
# 应用配置
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here

# 数据库配置（可选）
DATABASE_URL=sqlite:///data/monitor.db
HISTORY_DATABASE_URL=sqlite:///data/history.db

# 性能配置
COLLECTION_INTERVAL=30
HISTORY_RETENTION_DAYS=30
```



### 监控配置

系统支持以下自定义配置：

1. **数据采集间隔**：默认30秒
2. **历史数据保留**：默认30天
3. **告警重复间隔**：默认5分钟内不重复告警
4. **SSH连接超时**：默认10秒

## 🔧 故障排除

### 常见问题解决方案

#### 1. SSH连接失败

**症状**：服务器状态显示为离线

bash

```
# 诊断步骤：
1. 检查网络连通性：ping 192.168.1.100
2. 验证SSH连接：ssh user@host -p port
3. 检查防火墙设置
4. 确认用户名和密码正确
```



#### 2. 数据采集异常

**症状**：CPU/内存数据显示为0或异常

bash

```
# 解决方案：
1. 确认目标服务器支持top和free命令
2. 检查命令执行权限
3. 验证SSH密钥或密码认证
```



#### 3. 图表显示问题

**症状**：图表无法加载或显示异常

bash

```
# 解决步骤：
1. 检查浏览器控制台错误信息
2. 确认网络可以访问CDN资源
3. 尝试清除浏览器缓存
4. 检查JavaScript是否被阻止
```



#### 4. 性能问题

**症状**：界面响应缓慢

bash

```
# 优化建议：
1. 减少监控主机数量
2. 增加数据采集间隔
3. 优化数据库查询
4. 考虑使用更强大的服务器
```



### 日志分析

#### Docker环境

bash

```
# 查看完整日志
docker-compose logs monitor-app

# 实时日志跟踪
docker-compose logs -f monitor-app

# 查看特定时间段的日志
docker-compose logs --since 1h monitor-app
```



#### 传统环境

bash

```
# Flask开发服务器日志
tail -f nohup.out

# Gunicorn日志
tail -f logs/gunicorn.log
```



## 🛡️ 安全最佳实践

### 1. 认证安全

- ✅ 使用强密码策略
- ✅ 定期更换SSH密码
- ✅ 考虑使用SSH密钥认证
- ❌ 避免使用默认密码

### 2. 网络安全

- ✅ 部署在内网环境
- ✅ 配置防火墙规则
- ✅ 使用HTTPS加密
- ❌ 避免直接暴露到公网

### 3. 数据安全

- ✅ 定期备份数据库
- ✅ 加密敏感配置信息
- ✅ 实施访问日志记录
- ❌ 不要存储明文密码

### 4. 系统安全

- ✅ 定期更新依赖包
- ✅ 监控系统资源使用
- ✅ 设置适当的文件权限
- ❌ 避免使用root用户运行

## 📊 性能优化建议

### 硬件要求

| 监控主机数量 | 推荐CPU | 推荐内存 | 存储空间 |
| :----------- | :------ | :------- | :------- |
| 1-10台       | 1核     | 1GB      | 1GB      |
| 10-50台      | 2核     | 2GB      | 5GB      |
| 50-100台     | 4核     | 4GB      | 10GB     |

### 配置优化

python

```
# 在app.py中调整以下参数：

# 数据采集间隔（秒）
COLLECTION_INTERVAL = 30

# 历史数据保留天数
HISTORY_RETENTION_DAYS = 30

# SSH连接超时（秒）
SSH_TIMEOUT = 10

# 最大并发连接数
MAX_CONCURRENT_CONNECTIONS = 5
```



## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

### 报告问题

1. 在GitHub Issues中搜索是否已存在相关问题
2. 创建新的Issue，包含详细的问题描述和复现步骤
3. 提供环境信息（操作系统、Python版本等）

### 提交代码

1. Fork本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 创建Pull Request

### 开发规范

- 遵循PEP 8代码风格
- 添加适当的注释和文档
- 编写单元测试（如果适用）
- 确保向后兼容性



### 文档资源

- 📚 [完整文档](https://docs/) - 详细的使用和开发文档
- ❓ [常见问题](https://docs/FAQ.md) - 常见问题解答
- 🐛 [问题追踪](https://github.com/your-username/server-monitor/issues) - 报告bug和功能请求

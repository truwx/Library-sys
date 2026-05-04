# 图书馆管理系统

一个基于 Python 和 MySQL 的命令行图书馆管理系统。

## 功能特性

- 📚 **图书管理**：添加、删除、修改、查询图书信息
- 👥 **读者管理**：注册、删除、修改、查询读者信息
- 🔄 **借阅管理**：借书、还书、查询借阅记录
- 📊 **数据统计**：查看图书和借阅统计数据

## 技术栈

- Python 3.x
- MySQL 5.7+
- mysql-connector-python
- 面向对象设计

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `config.py` 文件，修改 MySQL 连接配置：

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的MySQL密码',
    'database': 'library_db',
    'charset': 'utf8mb4',
    'autocommit': True
}
```

### 3. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 运行系统

```bash
python -m library_system.main
```

## 使用说明

启动程序后，按照菜单提示进行操作：
- 输入对应的数字选择功能
- 根据提示输入相关信息
- 输入 `q` 或 `0` 返回主菜单或退出

## 项目结构

```
学习/
├── library_system/
│   ├── __init__.py
│   ├── models.py          # 数据模型定义
│   ├── database.py        # MySQL数据库连接和操作
│   ├── book_manager.py    # 图书管理功能
│   ├── reader_manager.py  # 读者管理功能
│   ├── borrow_manager.py  # 借阅管理功能
│   └── main.py            # 主程序入口
├── config.py              # 数据库配置
├── requirements.txt       # 依赖包
└── README.md
```
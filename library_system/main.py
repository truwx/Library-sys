import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_system.database import Database
from library_system.book_manager import BookManager
from library_system.reader_manager import ReaderManager
from library_system.borrow_manager import BorrowManager
from library_system.models import Book, Reader


class LibrarySystem:
    """图书馆管理系统主类"""
    
    def __init__(self):
        self.db = Database()
        self.book_manager = BookManager(self.db)
        self.reader_manager = ReaderManager(self.db)
        self.borrow_manager = BorrowManager(self.db)
    
    def show_main_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("         图书馆管理系统")
        print("="*60)
        print("1. 图书管理")
        print("2. 读者管理")
        print("3. 借阅管理")
        print("4. 统计分析")
        print("0. 退出系统")
        print("="*60)
    
    def show_book_menu(self):
        """显示图书管理菜单"""
        print("\n" + "-"*60)
        print("         图书管理")
        print("-"*60)
        print("1. 添加图书")
        print("2. 删除图书")
        print("3. 修改图书信息")
        print("4. 查询图书")
        print("5. 查看所有图书")
        print("0. 返回主菜单")
        print("-"*60)
    
    def show_reader_menu(self):
        """显示读者管理菜单"""
        print("\n" + "-"*60)
        print("         读者管理")
        print("-"*60)
        print("1. 注册读者")
        print("2. 删除读者")
        print("3. 修改读者信息")
        print("4. 查询读者")
        print("5. 查看所有读者")
        print("0. 返回主菜单")
        print("-"*60)
    
    def show_borrow_menu(self):
        """显示借阅管理菜单"""
        print("\n" + "-"*60)
        print("         借阅管理")
        print("-"*60)
        print("1. 借书")
        print("2. 还书")
        print("3. 查询借阅记录")
        print("4. 查询超期图书")
        print("0. 返回主菜单")
        print("-"*60)
    
    def add_book(self):
        """添加图书"""
        print("\n>>> 添加图书")
        try:
            title = input("书名: ").strip()
            author = input("作者: ").strip()
            isbn = input("ISBN: ").strip()
            publisher = input("出版社: ").strip()
            publish_date = input("出版日期 (YYYY-MM-DD): ").strip()
            category = input("分类: ").strip()
            total_copies = int(input("总册数: ").strip())
            
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                publisher=publisher,
                publish_date=publish_date,
                category=category,
                total_copies=total_copies,
                available_copies=total_copies
            )
            
            book_id = self.book_manager.add_book(book)
            print(f"✓ 图书添加成功！ID: {book_id}")
            
        except ValueError as e:
            print(f"✗ 输入错误: {e}")
        except Exception as e:
            print(f"✗ 添加失败: {e}")
    
    def delete_book(self):
        """删除图书"""
        print("\n>>> 删除图书")
        try:
            book_id = int(input("请输入图书ID: ").strip())
            book = self.book_manager.get_book_by_id(book_id)
            
            if not book:
                print("✗ 图书不存在")
                return
            
            print(f"图书信息: {book.title} - {book.author}")
            confirm = input("确认删除? (y/n): ").strip().lower()
            
            if confirm == 'y':
                if self.book_manager.delete_book(book_id):
                    print("✓ 图书删除成功")
                else:
                    print("✗ 删除失败")
        except ValueError:
            print("✗ 请输入有效的ID")
    
    def update_book(self):
        """修改图书信息"""
        print("\n>>> 修改图书信息")
        try:
            book_id = int(input("请输入图书ID: ").strip())
            book = self.book_manager.get_book_by_id(book_id)
            
            if not book:
                print("✗ 图书不存在")
                return
            
            print(f"当前信息: {book.to_dict()}")
            print("\n直接回车保持原值不变")
            
            title = input(f"书名 ({book.title}): ").strip()
            author = input(f"作者 ({book.author}): ").strip()
            publisher = input(f"出版社 ({book.publisher}): ").strip()
            
            updates = {}
            if title:
                updates['title'] = title
            if author:
                updates['author'] = author
            if publisher:
                updates['publisher'] = publisher
            
            if updates:
                if self.book_manager.update_book(book_id, **updates):
                    print("✓ 图书信息更新成功")
                else:
                    print("✗ 更新失败")
            else:
                print("没有修改任何信息")
                
        except ValueError:
            print("✗ 请输入有效的ID")
    
    def search_book(self):
        """查询图书"""
        print("\n>>> 查询图书")
        keyword = input("请输入搜索关键词（书名/作者/ISBN）: ").strip()
        
        if not keyword:
            print("✗ 请输入关键词")
            return
        
        books = self.book_manager.search_books(keyword)
        
        if not books:
            print("未找到相关图书")
            return
        
        print(f"\n找到 {len(books)} 本图书:\n")
        print(f"{'ID':<6} {'书名':<20} {'作者':<15} {'ISBN':<15} {'可借/总数':<10}")
        print("-"*70)
        
        for book in books:
            print(f"{book.book_id:<6} {book.title:<20} {book.author:<15} {book.isbn:<15} "
                  f"{book.available_copies}/{book.total_copies}")
    
    def show_all_books(self):
        """查看所有图书"""
        print("\n>>> 所有图书列表")
        
        total = self.book_manager.get_total_count()
        if total == 0:
            print("暂无图书")
            return
        
        page = 1
        page_size = 20
        
        while True:
            books = self.book_manager.get_all_books(page, page_size)
            
            if not books:
                print("没有更多图书")
                break
            
            print(f"\n第 {page} 页 (共 {total} 本):\n")
            print(f"{'ID':<6} {'书名':<20} {'作者':<15} {'ISBN':<15} {'可借/总数':<10}")
            print("-"*70)
            
            for book in books:
                print(f"{book.book_id:<6} {book.title:<20} {book.author:<15} {book.isbn:<15} "
                      f"{book.available_copies}/{book.total_copies}")
            
            choice = input("\n下一页? (y/n): ").strip().lower()
            if choice != 'y':
                break
            page += 1
    
    def add_reader(self):
        """注册读者"""
        print("\n>>> 注册读者")
        try:
            name = input("姓名: ").strip()
            phone = input("电话: ").strip()
            email = input("邮箱: ").strip()
            address = input("地址: ").strip()
            
            reader = Reader(
                name=name,
                phone=phone,
                email=email,
                address=address
            )
            
            reader_id = self.reader_manager.add_reader(reader)
            print(f"✓ 读者注册成功！ID: {reader_id}")
            
        except Exception as e:
            print(f"✗ 注册失败: {e}")
    
    def delete_reader(self):
        """删除读者"""
        print("\n>>> 删除读者")
        try:
            reader_id = int(input("请输入读者ID: ").strip())
            reader = self.reader_manager.get_reader_by_id(reader_id)
            
            if not reader:
                print("✗ 读者不存在")
                return
            
            print(f"读者信息: {reader.name} - {reader.phone}")
            confirm = input("确认删除? (y/n): ").strip().lower()
            
            if confirm == 'y':
                if self.reader_manager.delete_reader(reader_id):
                    print("✓ 读者删除成功")
                else:
                    print("✗ 删除失败")
        except ValueError:
            print("✗ 请输入有效的ID")
    
    def update_reader(self):
        """修改读者信息"""
        print("\n>>> 修改读者信息")
        try:
            reader_id = int(input("请输入读者ID: ").strip())
            reader = self.reader_manager.get_reader_by_id(reader_id)
            
            if not reader:
                print("✗ 读者不存在")
                return
            
            print(f"当前信息: {reader.to_dict()}")
            print("\n直接回车保持原值不变")
            
            name = input(f"姓名 ({reader.name}): ").strip()
            phone = input(f"电话 ({reader.phone}): ").strip()
            email = input(f"邮箱 ({reader.email}): ").strip()
            
            updates = {}
            if name:
                updates['name'] = name
            if phone:
                updates['phone'] = phone
            if email:
                updates['email'] = email
            
            if updates:
                if self.reader_manager.update_reader(reader_id, **updates):
                    print("✓ 读者信息更新成功")
                else:
                    print("✗ 更新失败")
            else:
                print("没有修改任何信息")
                
        except ValueError:
            print("✗ 请输入有效的ID")
    
    def search_reader(self):
        """查询读者"""
        print("\n>>> 查询读者")
        keyword = input("请输入搜索关键词（姓名/电话/邮箱）: ").strip()
        
        if not keyword:
            print("✗ 请输入关键词")
            return
        
        readers = self.reader_manager.search_readers(keyword)
        
        if not readers:
            print("未找到相关读者")
            return
        
        print(f"\n找到 {len(readers)} 个读者:\n")
        print(f"{'ID':<6} {'姓名':<15} {'电话':<15} {'邮箱':<25}")
        print("-"*65)
        
        for reader in readers:
            print(f"{reader.reader_id:<6} {reader.name:<15} {reader.phone:<15} {reader.email:<25}")
    
    def show_all_readers(self):
        """查看所有读者"""
        print("\n>>> 所有读者列表")
        
        total = self.reader_manager.get_total_count()
        if total == 0:
            print("暂无读者")
            return
        
        page = 1
        page_size = 20
        
        while True:
            readers = self.reader_manager.get_all_readers(page, page_size)
            
            if not readers:
                print("没有更多读者")
                break
            
            print(f"\n第 {page} 页 (共 {total} 个):\n")
            print(f"{'ID':<6} {'姓名':<15} {'电话':<15} {'邮箱':<25}")
            print("-"*65)
            
            for reader in readers:
                print(f"{reader.reader_id:<6} {reader.name:<15} {reader.phone:<15} {reader.email:<25}")
            
            choice = input("\n下一页? (y/n): ").strip().lower()
            if choice != 'y':
                break
            page += 1
    
    def borrow_book(self):
        """借书"""
        print("\n>>> 借书")
        try:
            book_id = int(input("请输入图书ID: ").strip())
            reader_id = int(input("请输入读者ID: ").strip())
            days = input("借阅天数（默认30天）: ").strip()
            
            borrow_days = int(days) if days else 30
            
            record_id = self.borrow_manager.borrow_book(book_id, reader_id, borrow_days)
            if record_id:
                book = self.book_manager.get_book_by_id(book_id)
                reader = self.reader_manager.get_reader_by_id(reader_id)
                print(f"  图书: {book.title}")
                print(f"  读者: {reader.name}")
        except ValueError:
            print("✗ 请输入有效的ID")
    
    def return_book(self):
        """还书"""
        print("\n>>> 还书")
        try:
            record_id = int(input("请输入借阅记录ID: ").strip())
            self.borrow_manager.return_book(record_id)
        except ValueError:
            print("✗ 请输入有效的ID")
    
    def query_borrow_records(self):
        """查询借阅记录"""
        print("\n>>> 查询借阅记录")
        print("1. 按读者查询")
        print("2. 按图书查询")
        print("3. 按记录ID查询")
        
        choice = input("请选择查询方式: ").strip()
        
        if choice == '1':
            reader_id = int(input("请输入读者ID: ").strip())
            records = self.borrow_manager.get_reader_borrows(reader_id)
            self._display_borrow_records(records)
        elif choice == '2':
            book_id = int(input("请输入图书ID: ").strip())
            records = self.borrow_manager.get_book_borrows(book_id)
            self._display_borrow_records(records)
        elif choice == '3':
            record_id = int(input("请输入记录ID: ").strip())
            record = self.borrow_manager.get_borrow_record(record_id)
            if record:
                print(f"\n借阅记录:")
                print(f"  记录ID: {record.record_id}")
                print(f"  状态: {record.status}")
                print(f"  借阅日期: {record.borrow_date}")
                print(f"  应还日期: {record.due_date}")
                print(f"  归还日期: {record.return_date or '未归还'}")
            else:
                print("✗ 记录不存在")
        else:
            print("✗ 无效选择")
    
    def _display_borrow_records(self, records):
        """显示借阅记录列表"""
        if not records:
            print("未找到借阅记录")
            return
        
        print(f"\n找到 {len(records)} 条记录:\n")
        print(f"{'记录ID':<8} {'图书':<20} {'读者':<15} {'借阅日期':<12} {'应还日期':<12} {'状态':<10}")
        print("-"*80)
        
        for record in records:
            book = self.book_manager.get_book_by_id(record.book_id)
            reader = self.reader_manager.get_reader_by_id(record.reader_id)
            
            book_title = book.title if book else "未知"
            reader_name = reader.name if reader else "未知"
            
            print(f"{record.record_id:<8} {book_title:<20} {reader_name:<15} "
                  f"{record.borrow_date:<12} {record.due_date:<12} {record.status:<10}")
    
    def show_overdue_books(self):
        """显示超期图书"""
        print("\n>>> 超期图书列表")
        
        overdue_list = self.borrow_manager.get_overdue_books()
        
        if not overdue_list:
            print("暂无超期图书")
            return
        
        print(f"\n共 {len(overdue_list)} 本超期图书:\n")
        print(f"{'记录ID':<8} {'图书':<20} {'ISBN':<15} {'读者':<15} {'电话':<15} {'应还日期':<12}")
        print("-"*90)
        
        for item in overdue_list:
            print(f"{item['record_id']:<8} {item['book_title']:<20} {item['isbn']:<15} "
                  f"{item['reader_name']:<15} {item.get('phone', ''):<15} {item['due_date']:<12}")
    
    def show_statistics(self):
        """显示统计信息"""
        print("\n>>> 统计分析")
        
        stats = self.borrow_manager.get_statistics()
        
        print("\n" + "="*60)
        print("         统计数据")
        print("="*60)
        print(f"总借阅次数: {stats['total_borrows']}")
        print(f"当前借出: {stats['current_borrows']}")
        print(f"超期数量: {stats['overdue_count']}")
        print("="*60)
        
        # 热门图书
        if stats['popular_books']:
            print("\n热门图书 TOP 10:")
            print(f"{'书名':<30} {'作者':<20} {'借阅次数':<10}")
            print("-"*60)
            for book in stats['popular_books']:
                print(f"{book['title']:<30} {book['author']:<20} {book['borrow_count']:<10}")
        
        # 活跃读者
        if stats['active_readers']:
            print("\n活跃读者 TOP 10:")
            print(f"{'姓名':<20} {'电话':<15} {'借阅次数':<10}")
            print("-"*50)
            for reader in stats['active_readers']:
                print(f"{reader['name']:<20} {reader.get('phone', ''):<15} {reader['borrow_count']:<10}")
    
    def book_menu_handler(self):
        """图书管理菜单处理"""
        while True:
            self.show_book_menu()
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.delete_book()
            elif choice == '3':
                self.update_book()
            elif choice == '4':
                self.search_book()
            elif choice == '5':
                self.show_all_books()
            elif choice == '0':
                break
            else:
                print("✗ 无效选择，请重新输入")
    
    def reader_menu_handler(self):
        """读者管理菜单处理"""
        while True:
            self.show_reader_menu()
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.add_reader()
            elif choice == '2':
                self.delete_reader()
            elif choice == '3':
                self.update_reader()
            elif choice == '4':
                self.search_reader()
            elif choice == '5':
                self.show_all_readers()
            elif choice == '0':
                break
            else:
                print("✗ 无效选择，请重新输入")
    
    def borrow_menu_handler(self):
        """借阅管理菜单处理"""
        while True:
            self.show_borrow_menu()
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.borrow_book()
            elif choice == '2':
                self.return_book()
            elif choice == '3':
                self.query_borrow_records()
            elif choice == '4':
                self.show_overdue_books()
            elif choice == '0':
                break
            else:
                print("✗ 无效选择，请重新输入")
    
    def run(self):
        """运行系统"""
        print("\n欢迎使用图书馆管理系统！")
        
        try:
            while True:
                self.show_main_menu()
                choice = input("请选择功能: ").strip()
                
                if choice == '1':
                    self.book_menu_handler()
                elif choice == '2':
                    self.reader_menu_handler()
                elif choice == '3':
                    self.borrow_menu_handler()
                elif choice == '4':
                    self.show_statistics()
                elif choice == '0':
                    print("\n感谢使用，再见！")
                    break
                else:
                    print("✗ 无效选择，请重新输入")
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
        except Exception as e:
            print(f"\n✗ 系统错误: {e}")
        finally:
            self.db.close()


def main():
    """主函数"""
    system = LibrarySystem()
    system.run()


if __name__ == "__main__":
    main()

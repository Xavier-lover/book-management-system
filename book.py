from datetime import datetime

class Book:
    """图书类 - 表示图书馆中的一本书"""
    
    # 类属性
    total_books_created = 0
    
    def __init__(self, title, author, isbn, publisher="未知出版社", year=2024, copies=1):
        """
        初始化图书信息
        title: 书名
        author: 作者
        isbn: ISBN号
        publisher: 出版社
        year: 出版年份
        copies: 总册数
        """
        # 验证必要参数
        if not title or not author or not isbn:
            raise ValueError("书名、作者和ISBN不能为空")
        
        # 实例属性
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.publisher = publisher.strip()
        self.year = year
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_records = []  # 借阅记录：[{'borrower': '姓名', 'date': '日期'}]
        
        # 更新类属性
        Book.total_books_created += 1
        
        print(f"📚 图书创建成功：《{self.title}》")
    
    def is_available(self):
        """检查是否有可借的副本"""
        return self.available_copies > 0
    
    def borrow(self, borrower_name):
        """
        借书
        borrower_name: 借阅者姓名
        返回: True表示借阅成功,False表示失败
        """
        if not self.is_available():
            return False
        
        # 检查同一人是否已经借了这本书
        for record in self.borrowed_records:
            if record['borrower'] == borrower_name:
                return False# 同一人不能重复借同一本书
        
        # 借书成功
        self.available_copies -= 1
        self.borrowed_records.append({
            'borrower': borrower_name,
            'borrow_date': self.get_current_date()
        })
        return True
    
    def return_book(self, borrower_name):
        """
        还书
        borrower_name: 借阅者姓名
        返回: True表示归还成功,False表示失败
        """
        # 查找借阅记录
        for i, record in enumerate(self.borrowed_records):
            if record['borrower'] == borrower_name:
                # 找到记录，归还图书
                self.available_copies += 1
                self.borrowed_records.pop(i)
                return True
        
        return False# 没有找到借阅记录
    
    def get_borrower_list(self):
        """获取当前借阅者列表"""
        return [record['borrower'] for record in self.borrowed_records]
    
    @staticmethod
    def get_current_date():
        """获取当前日期（静态方法）"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def is_valid_isbn(isbn):
        """验证ISBN格式(简单验证)"""
        # 移除连字符和空格
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        # 检查是否为10位或13位数字
        return isbn_clean.isdigit() and len(isbn_clean) in [10, 13]
    
    @classmethod
    def create_sample_books(cls):
        """类方法：创建一些示例图书"""
        sample_books = [
            cls("Python编程:从入门到实践", "埃里克·马瑟斯", "978-7-115-42802-8", "人民邮电出版社", 2016, 3),
            cls("算法导论", "托马斯·科尔曼", "978-7-111-40701-0", "机械工业出版社", 2013, 2),
            cls("深度学习", "伊恩·古德费洛", "978-7-111-55719-2", "机械工业出版社", 2017, 1),
            cls("机器学习", "周志华", "978-7-111-51946-1", "清华大学出版社", 2016, 2),
            cls("数据结构与算法分析", "马克·艾伦·维斯", "978-7-111-14239-1", "机械工业出版社", 2004, 2)
        ]
        return sample_books
    
    def __str__(self):
        """字符串表示"""
        status = f"可借：{self.available_copies}/{self.total_copies}"
        return f"《{self.title}》 - {self.author} ({status})"
    
    def __repr__(self):
        """调试用字符串表示"""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"
    
    def __eq__(self, other):
        """判断两本书是否相同(基于ISBN)"""
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False
    
    def __hash__(self):
        """使Book对象可以作为字典的键或集合的元素"""
        return hash(self.isbn)
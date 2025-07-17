from book import Book

class Library:
    """图书馆类 - 管理图书和会员"""
    
    # 类属性
    total_libraries = 0
    
    def __init__(self, name="我的图书馆"):
        """初始化图书馆"""
        self.name = name
        self.books = {}  # 使用字典存储图书，键为ISBN，值为Book对象
        self.members = set()  # 使用集合存储会员，自动去重
        self.borrow_history = []  # 借阅历史记录
        
        # 更新类属性
        Library.total_libraries += 1
        
        print(f"🏛️ 图书馆创建成功：{self.name}")
    
    def add_book(self, book_or_title, author=None, isbn=None, publisher="未知出版社", year=2024, copies=1):
        """
        添加图书（支持两种方式）
        方式1：传入Book对象
        方式2：传入图书信息，自动创建Book对象
        """
        if isinstance(book_or_title, Book):
            # 方式1：直接传入Book对象
            book = book_or_title
        else:
            # 方式2：传入图书信息
            if not author or not isbn:
                print("❌ 添加图书失败：缺少必要信息")
                return False
            
            book = Book(book_or_title, author, isbn, publisher, year, copies)
        
        # 检查图书是否已存在
        if book.isbn in self.books:
            # 图书已存在，增加副本数
            existing_book = self.books[book.isbn]
            existing_book.total_copies += book.total_copies
            existing_book.available_copies += book.total_copies
            print(f"📖 图书已存在，增加了 {book.total_copies} 册副本")
        else:
            # 新图书
            self.books[book.isbn] = book
            print(f"✅ 成功添加新图书：{book}")
        
        return True
    
    def find_book_by_title(self, title):
        """根据书名查找图书"""
        for book in self.books:
            if book.title == title:
                return book
        return None
    
    # 🌟 新增功能：按书名搜索（模糊匹配）
    def search_books_by_title(self, keyword):
        """ 根据关键词搜索图书标题（支持模糊匹配）"""
        if not keyword:
            print("请输入搜索关键词！")
            return []
        
        keyword_lower = keyword.lower()
        matched_books = []
        
        for book in self.books:
            if keyword_lower in book.title.lower():
                matched_books.append(book)

        return matched_books
    
     # 🌟 新增功能：按作者搜索
    def search_book_by_author(self, author_keyword):
        """ 根据作者关键词搜索图书作者（支持模糊匹配）"""
        if not author_keyword:
            print("请输入作者关键词")
            return []
        
        author_keyword_lower = author_keyword.lower()
        matched_books = []

        for book in self.books:
            if author_keyword_lower in book.author.lower():
                matched_books.append(book)

        return matched_books
    
    # 🌟 新增功能：综合搜索
    def search_books(self, keyword, search_type="all"):
        """ 综合搜索功能：可以按标题、作者或全部进行搜索"""
        if not keyword:
            print("请输入关键词")
            return []
        
        if search_type == "title":
            return self.search_books_by_title(keyword)
        elif search_type == "author":
            return self.search_books_by_author(keyword)
        elif search_type == "all":
            title_results=self.search_books_by_title(keyword)
            author_results=self.search_books_by_author(keyword)
            all_results=list(set(title_results+author_results))
            return all_results
        else:
            print(f"无效的搜索类型:{search_type}")
            return []
    
    def register_member(self, member_name):
        """注册会员"""
        member_name = member_name.strip()
        if not member_name:
            print("❌ 会员姓名不能为空")
            return False
        
        if member_name in self.members:
            print(f"⚠️ 会员 {member_name} 已存在")
            return False
        
        self.members.add(member_name)
        print(f"✅ 会员 {member_name} 注册成功")
        return True
    
    def find_book_by_isbn(self, isbn):
        """根据ISBN查找图书"""
        return self.books.get(isbn)
    
    def find_books_by_title(self, title_keyword):
        """根据书名关键词查找图书"""
        found_books = []
        keyword_lower = title_keyword.lower()
        
        for book in self.books.values():
            if keyword_lower in book.title.lower():
                found_books.append(book)
        
        return found_books
    
    def find_books_by_author(self, author_keyword):
        """根据作者关键词查找图书"""
        found_books = []
        keyword_lower = author_keyword.lower()
        
        for book in self.books.values():
            if keyword_lower in book.author.lower():
                found_books.append(book)
        
        return found_books
    
    def borrow_book(self, isbn, borrower_name):
        """借书"""
        # 检查会员是否存在
        if borrower_name not in self.members:
            print(f"❌ 会员 {borrower_name} 不存在，请先注册")
            return False
        
        # 查找图书
        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"❌ 未找到ISBN为 {isbn} 的图书")
            return False
        
        # 尝试借书
        if book.borrow(borrower_name):
            # 记录借阅历史
            self.borrow_history.append({
                'action': '借阅',
                'book_title': book.title,
                'borrower': borrower_name,
                'date': Book.get_current_date()
            })
            
            print(f"✅ 借书成功！{borrower_name} 借阅了《{book.title}》")
            return True
        else:
            # 借书失败，检查原因
            if not book.is_available():
                print(f"❌ 借书失败！《{book.title}》暂无可借副本")
            else:
                print(f"❌ 借书失败！{borrower_name} 已经借阅过这本书")
            return False
    
    def return_book(self, isbn, borrower_name):
        """还书"""
        # 查找图书
        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"❌ 未找到ISBN为 {isbn} 的图书")
            return False
        
        # 尝试还书
        if book.return_book(borrower_name):
            # 记录归还历史
            self.borrow_history.append({
                'action': '归还',
                'book_title': book.title,
                'borrower': borrower_name,
                'date': Book.get_current_date()
            })
            
            print(f"✅ 还书成功！{borrower_name} 归还了《{book.title}》")
            return True
        else:
            print(f"❌ 还书失败！{borrower_name} 没有借阅过《{book.title}》")
            return False
     
    def display_all_books(self):
        """显示所有图书"""
        if not self.books:
            print("📚 图书馆暂无图书")
            return
        
        print(f"\n📚 {self.name} - 图书清单")
        print("=" * 80)
        print(f"{'序号':<4} {'书名':<25} {'作者':<15} {'状态':<12} {'借阅者'}")
        print("-" * 80)
        
        for i, book in enumerate(self.books.values(), 1):
            borrowers = ", ".join(book.get_borrower_list()) if book.get_borrower_list() else"无"
            status = f"{book.available_copies}/{book.total_copies}"
            
            print(f"{i:<4} {book.title[:24]:<25} {book.author[:14]:<15} {status:<12} {borrowers}")
    
    def search_books(self, keyword):
        """搜索图书（按书名和作者）"""
        title_results = self.find_books_by_title(keyword)
        author_results = self.find_books_by_author(keyword)
        
        # 合并结果并去重
        all_results = list(set(title_results + author_results))
        
        if all_results:
            print(f"\n🔍 搜索 '{keyword}' 找到 {len(all_results)} 本相关图书：")
            print("-" * 50)
            for book in all_results:
                print(f"  📖 {book}")
                if book.get_borrower_list():
                    print(f"      当前借阅者：{', '.join(book.get_borrower_list())}")
        else:
            print(f"🔍 未找到包含关键词 '{keyword}' 的图书")
    
    def display_members(self):
        """显示所有会员"""
        if not self.members:
            print("👥 暂无注册会员")
            return
        
        print(f"\n👥 {self.name} - 会员名单 (共{len(self.members)}人)")
        print("-" * 30)
        for i, member in enumerate(sorted(self.members), 1):
            # 统计每个会员当前借阅的图书数
            borrowed_count = 0
            for book in self.books.values():
                if member in book.get_borrower_list():
                    borrowed_count += 1
            
            print(f"{i:2d}. {member} (当前借阅: {borrowed_count} 本)")
    
    def display_member_books(self, member_name):
        """显示某个会员借阅的所有图书"""
        if member_name not in self.members:
            print(f"❌ 会员 {member_name} 不存在")
            return
        
        borrowed_books = []
        for book in self.books.values():
            if member_name in book.get_borrower_list():
                borrowed_books.append(book)
        
        if borrowed_books:
            print(f"\n📚 {member_name} 当前借阅的图书：")
            print("-" * 40)
            for book in borrowed_books:
                print(f"  📖 {book}")
        else:
            print(f"📚 {member_name} 当前没有借阅任何图书")
    
    def display_borrow_history(self, limit=10):
        """显示借阅历史"""
        if not self.borrow_history:
            print("📋 暂无借阅历史")
            return
        
        print(f"\n📋 最近 {min(limit, len(self.borrow_history))} 条借阅记录：")
        print("-" * 60)
        
        # 显示最近的记录
        recent_history = self.borrow_history[-limit:]
        for record in reversed(recent_history):
            action = record['action']
            emoji = "📤"if action == "借阅"else"📥"
            print(f"{emoji} {record['date']} - {record['borrower']} {action} 《{record['book_title']}》")
    
    def get_library_statistics(self):
        """获取图书馆统计信息"""
        total_books = len(self.books)
        total_copies = sum(book.total_copies for book in self.books.values())
        available_copies = sum(book.available_copies for book in self.books.values())
        borrowed_copies = total_copies - available_copies
        total_members = len(self.members)
        
        print(f"\n📊 {self.name} - 统计信息")
        print("=" * 40)
        print(f"📚 图书种类：{total_books} 种")
        print(f"📖 图书总册数：{total_copies} 册")
        print(f"✅ 可借册数：{available_copies} 册")
        print(f"📤 已借册数：{borrowed_copies} 册")
        print(f"👥 注册会员：{total_members} 人")
        
        if total_copies > 0:
            utilization_rate = borrowed_copies / total_copies * 100
            print(f"📈 图书利用率：{utilization_rate:.1f}%")
    
    @classmethod
    def create_sample_library(cls):
        """类方法：创建一个带示例数据的图书馆"""
        library = cls("示例图书馆")
        
        # 添加示例图书
        sample_books = Book.create_sample_books()
        for book in sample_books:
            library.add_book(book)
        
        # 注册示例会员
        sample_members = ["张三", "李四", "王五", "赵六", "钱七"]
        for member in sample_members:
            library.register_member(member)
        
        # 模拟一些借阅
        library.borrow_book("978-7-115-42802-8", "张三")  # Python编程
        library.borrow_book("978-7-111-40701-0", "李四")  # 算法导论
        library.borrow_book("978-7-111-55719-2", "王五")  # 深度学习
        
        return library
    
    def __str__(self):
        """字符串表示"""
        return f"Library({self.name}) - {len(self.books)} 种图书, {len(self.members)} 位会员"
    
    def __len__(self):
        """返回图书馆中图书的种类数量"""
        return len(self.books)
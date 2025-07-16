from library import Library

# 主程序 - 图书管理系统控制台版
def main():
    """图书管理系统主程序"""
    print("🏛️ 欢迎使用图书管理系统")
    print("=" * 50)
    
    # 创建图书馆
    library_name = input("请输入图书馆名称（直接回车使用默认名称）: ").strip()
    if not library_name:
        library_name = "我的图书馆"
    
    library = Library(library_name)
    
    # 询问是否加载示例数据
    load_sample = input("是否加载示例数据？(y/n): ").lower()
    if load_sample == 'y':
        library = Library.create_sample_library()
        library.name = library_name
        print("✅ 示例数据加载完成")
    
    # 主循环
    while True:
        print(f"\n🏛️ {library.name} 管理系统")
        print("=" * 50)
        print("📚 图书管理:")
        print("  1. 显示所有图书")
        print("  2. 搜索图书")
        print("  3. 添加图书")
        print("")
        print("👥 会员管理:")
        print("  4. 显示所有会员")
        print("  5. 注册新会员")
        print("  6. 查看会员借阅")
        print("")
        print("📤 借还管理:")
        print("  7. 借阅图书")
        print("  8. 归还图书")
        print("")
        print("📊 统计报表:")
        print("  9. 图书馆统计")
        print(" 10. 借阅历史")
        print("")
        print("  0. 退出系统")
        print("-" * 50)
        
        choice = input("请选择操作 (0-10): ").strip()
        
        try:
            if choice == "1":
                library.display_all_books()
                
            elif choice == "2":
                keyword = input("请输入搜索关键词（书名或作者）: ").strip()
                if keyword:
                    library.search_books(keyword)
                    
            elif choice == "3":
                print("\n📖 添加新图书")
                title = input("书名: ").strip()
                author = input("作者: ").strip()
                isbn = input("ISBN: ").strip()
                publisher = input("出版社（可选）: ").strip() or"未知出版社"
                
                try:
                    year = int(input("出版年份(可选,默认2024): ") or"2024")
                    copies = int(input("册数(默认1): ")or"1")
                except ValueError:
                    year, copies = 2024, 1
                
                library.add_book(title, author, isbn, publisher, year, copies)
                
            elif choice == "4":
                library.display_members()
                
            elif choice == "5":
                name = input("请输入会员姓名: ").strip()
                if name:
                    library.register_member(name)
                    
            elif choice == "6":
                name = input("请输入会员姓名: ").strip()
                if name:
                    library.display_member_books(name)
                    
            elif choice == "7":
                isbn = input("请输入要借阅图书的ISBN: ").strip()
                borrower = input("请输入借阅人姓名: ").strip()
                if isbn and borrower:
                    library.borrow_book(isbn, borrower)
                    
            elif choice == "8":
                isbn = input("请输入要归还图书的ISBN: ").strip()
                borrower = input("请输入借阅人姓名: ").strip()
                if isbn and borrower:
                    library.return_book(isbn, borrower)
                    
            elif choice == "9":
                library.get_library_statistics()
                
            elif choice == "10":
                try:
                    limit = int(input("显示最近多少条记录(默认10): ")or"10")
                except ValueError:
                    limit = 10
                library.display_borrow_history(limit)
                
            elif choice == "0":
                print(f"\n👋 感谢使用 {library.name} 管理系统，再见！")
                break
                
            else:
                print("❌ 无效选择，请重新输入")
                
        except Exception as e:
            print(f"❌ 操作出错：{e}")
        
        # 等待用户按键继续
        input("\n按回车键继续...")


# 简单演示程序
def demo():
    """演示程序"""
    print("🎯 图书管理系统演示")
    print("=" * 30)
    
    # 创建示例图书馆
    library = Library.create_sample_library()
    
    # 显示初始状态
    library.display_all_books()
    library.display_members()
    library.get_library_statistics()
    
    # 演示搜索功能
    print("\n🔍 搜索演示：")
    library.search_books("Python")
    library.search_books("周志华")
    
    # 显示借阅历史
    library.display_borrow_history()
    
    # 显示某个会员的借阅情况
    library.display_member_books("张三")


if __name__ == "__main__":
    # 询问运行模式
    print("请选择运行模式：")
    print("1. 完整管理系统")
    print("2. 快速演示")
    
    mode = input("请选择 (1/2): ").strip()
    
    if mode == "2":
        demo()
    else:
        main()
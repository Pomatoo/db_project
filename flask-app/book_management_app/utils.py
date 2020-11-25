from book_management_app import mongo

def get_books(page_size, page_num):
    page_num = int(page_num)
    page_size = int(page_size)
    page_numbers = list(range(1, 4000))
    skips = page_size * (page_num - 1)
    book_meta = mongo.db.book_meta.find().skip(skips).limit(page_size)
    book_list = []
    for book in book_meta:
        book_list.append(book)
    return book_list
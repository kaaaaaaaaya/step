import sys
import re
# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

#配列は文字列インデックスができないため。(今回は辞書NG??)
def caliculate(key):
    assert re.search(".com$", key)
    new_key = key[:-4]
    total = 0
    for i in  new_key:
        total += ord(i) - ord("a")
    return total

class Item:

    def __init__(self, key, values):
        self.key = key
        self.values = values
        self.next = None
        self.prev = None

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.bucket_size = n
        self.buckets = [None] * self.bucket_size
        self.item_count = 0
        self.head = None
        self.tail = None

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        buckets_index = caliculate(url) % self.bucket_size
        item = self.buckets[buckets_index]
        if item is not None and contents == item.values:
            if item.prev:
                before_item = item.prev
                if item.next:
                    before_item.next = item.next
                else:
                    #itemが末尾
                    self.tail = item.prev
                item.next = self.head
                self.head = item
            #itemがhead
        else:
        #アクセスしたいのがなかったら先頭にくっつける
            #キャッシュがいっぱいの時
            if self.item_count == self.bucket_size:
                new_item = Item(url, contents)
                new_item.next = self.head
                self.buckets[buckets_index] = new_item
                self.head = new_item
                #後ろから2番目の値のnextをNoneに繋げたい。→whileやforを使わずに管理したい。
                rear_bucket = self.tail
                rear2_bucket = rear_bucket.prev
                rear2_bucket.next = None
                self.tail = rear2_bucket
            else:
            #キャッシュが定義のサイズより小さい場合
                if self.item_count == 0:
                    new_item = Item(url, contents)
                    new_item.next = self.head
                    self.buckets[buckets_index] = new_item
                    self.head = new_item
                    self.tail = new_item
                    self.item_count += 1
                else:
                    new_item = Item(url, contents)
                    new_item.next = self.head
                    self.buckets[buckets_index] = new_item
                    next_item = new_item.next
                    next_item.prev = new_item
                    self.head = new_item
                    self.tail = new_item
                    self.item_count += 1

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        urls = []
        node = self.head
        while node:
            urls.append(node.key)
            node = node.next
        print(urls)
        return urls

def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
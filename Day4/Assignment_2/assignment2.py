import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def binary_search(self,left, right, title, titles):#タイトルのIdを探す
        if left > right:
            return None
        
        mid = (left + right)//2
        if titles[mid][1] == title:
            return titles[mid][0]
        elif titles[mid][1] < title:
            left = mid + 1
            return self.binary_search(left, right, title, titles)
        else:
            right = mid - 1
            return self.binary_search(left, right, title, titles)
    
    def answer(self, start_id, goal_id, related_link):
        id = goal_id
        ans = [goal_id]
        print(f"start_id： {start_id}")
        print(f"goal_id： {goal_id}")
        while start_id != related_link[id]:
            ans.append(related_link[id])
            id = related_link[id]
        ans.append(start_id)
        return list(reversed(ans))

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        titles = sorted(self.titles.items(), key = lambda x: x[1])
        start_id = self.binary_search(0, len(titles)-1,start, titles)
        assert start_id != None, "The start title is not exist "
        goal_id = self.binary_search(0, len(titles)-1, goal, titles)
        assert goal_id != None, "The goal title is not exist "
        related_link = [None] * (list(self.titles.items())[-1][0] + 1) #どのノードからつながっているかを記録
        queue = collections.deque([start_id]) #キューの最初にstartを入れる
        related_link[start_id] = start_id
        visited = [start_id]
        find = False

        # ↓↓↓深くなってしまうものは幅優先木関数として切り分けたほうがいい、、？
        while queue and not find:
            v = queue.pop()
            for id in self.links[v]:
                if not id in visited: #訪問済み(既にキューに入っている)であるかを確認
                    related_link[id] = v #idはvから繋がっている
                    visited.append(id)
                    if id == goal_id: #ゴールのタイトルであるかどうか
                        find = True
                        break
                    queue.appendleft(id) #vから繋がってるidをキューにいれる

        id_ans = self.answer(start_id, goal_id, related_link) #最短経路出力
        print(id_ans)
        title_ans = []
        for i in id_ans:
            title_ans.append(self.titles[i])
        print(title_ans)

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        rank = [1.0]*(len(self.titles)) #1:すべてのノードのランクを初期化する
        titles_rank = dict(zip(self.titles.keys(),zip(self.titles.values(),rank))) #タイトルとランクを結びつける
        reference_links = {}
        total_keys = len(self.titles.keys())
        for id, link in self.links.items(): #参照先ノードをまとめる
            if id in reference_links:
                reference_links[id].append(link)
            else:
                reference_links[id] = link

        temporaly_rank =  {id: 0.0 for id in self.titles.keys()}# 一時的にrankを保持する
        for i in self.titles.keys():
            reference_link = reference_links.get(i, [])
            count = len(reference_link) #参照先リンク数
            if count > 0:
                flow = (titles_rank[i][1] * 0.85) /count #参照先に流すランク
            else:
                flow = 0
            print(f"key: {i}")
            print(f"flow: {flow}")

            if total_keys - count - 1> 0: #全リンクを参照していないか -1は自分のノード
                sub_flow = (titles_rank[i][1]  * 0.15) /(total_keys - count - 1) #参照先以外に流すランク
            else:
                sub_flow = 0

            for referenced_id in reference_link: #参照先に流す
                temporaly_rank[referenced_id] += flow

            unlinked_id = self.titles.keys() - set(reference_links[i]) - {i}
            for unreferenced_id in unlinked_id: #参照先以外に流す
                temporaly_rank[unreferenced_id] += sub_flow
            
        for id in self.titles.keys():
            titles_rank[id] = (titles_rank[id][0], temporaly_rank[id])
        top_10_ids = sorted(titles_rank.keys(), key=lambda x: titles_rank[x][1], reverse=True)

        top_count = 0
        for i in top_10_ids:
            if top_count == 10:
                break
            title, score = titles_rank[i]
            print(f"ID: {i}, タイトル: {title}, スコア: {score}")
            top_count += 1

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    #wikipedia.find_longest_titles()
    # Example
    #wikipedia.find_most_linked_pages()
    # Homework #1
    #wikipedia.find_shortest_path("渋谷", "小野妹子")
    #wikipedia.find_shortest_path("A", "F")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
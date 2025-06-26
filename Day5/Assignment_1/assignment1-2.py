#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input
def distance(u,v):
    return math.sqrt((u[1] - v[1] ) ** 2 + (u[2] - v[2] ) ** 2 )

# ２点ノード間の距離 vと一度も訪れていないノード O(N)
def min_distance(v, unvisited):
    count = 0
    for u in unvisited:
        if count == 0:
            # 最初のノードを最小値にする
            min = distance(u,v)
            near_node = u
            count = 1
        #距離を計算
        else:
            distance_vu = distance(u,v)
        #今の最小値より小さければ v-u間が最小距離のため入れ替える
            if min > distance_vu:
                near_node = u
                min = distance_vu
    # vと再消去オリを構成するuを返す
    return (near_node, min)

def solve(cities):
    #訪問済みでないノード
    unvisited = set()
    for city in cities:
        unvisited.add(tuple(city))
    # 最短距離の合計
    all_distance = 0
    #辿ったノードの順番
    loop_node = []
    # 最初の基準となるノードを取り出す
    first_node = v = random.choice(cities)
    loop_node.append(v)
    unvisited.remove(v)
    # ノードを巡回する O(N^2) = O(N)[外側のループ] * O(N)[最短距離を満たすノードを探すループ]
    while unvisited:
        # v = cities[i]に対する最短距離とそれを満たすノードuの取得
        v, min = min_distance(v, unvisited)
        # 辿ったvを記録
        loop_node.append(v)
        # v(u)は訪問済みのため取り除く
        unvisited.remove(v)
        #最後のノードであればそれを保存
        if not unvisited:
            last_node = v
        # 最小値を合計値に加える
        all_distance += min

    # 最後のノードと最初のノード間の距離を計算
    all_distance += distance(first_node,last_node)
    #print(f"最短距離 {all_distance}")
    return loop_node

def k_opt(loop_node):
    N = len(loop_node)
    # 交差してる辺の数
    crossing_count = 0
    # 交差してる間続ける O(N^2 * ？？？？？？？)
    while True:
        crossing_count = 0
        # 交差している2辺を入れ替える O(N^2)
        for i in range(N):
            for j in range(N):
                # 同じノードを参照ている場合はスキップ
                if i == j or i + 1 == j or i == j + 1:
                    continue

                a1 = loop_node[i]
                a2 = loop_node[(i+1)%N]
                b1 = loop_node[j]
                b2 = loop_node[(j+1)%N]
                # 元々の距離
                a1a2_b1b2 = distance(a1,a2) + distance(b1,b2)
                # 変更後の距離
                a1b1_a2b2 = distance(a1,b1) + distance(a2,b2)
                # 元々の距離 > 変更後の距離
                if a1a2_b1b2 > a1b1_a2b2:
                    crossing_count += 1
                    loop_node[i+1:j+1] = reversed(loop_node[i+1:j+1])
        if crossing_count == 0:
            break
        #print(crossing_count)
    return loop_node


if __name__ == '__main__':
    assert len(sys.argv) > 1
    for i in range(1000):
        tour = solve(read_input(sys.argv[1]))
        tour = k_opt(tour)
        if  i == 0:
            min = path_length = sum(distance(tour[i], tour[(i + 1) % len(tour)])
                                for i in range(len(tour)))
            min_tour = tour
        else: 
            path_length = sum(distance(tour[i], tour[(i + 1) % len(tour)])
                                for i in range(len(tour)))
       # print(f"opt後: {path_length}")
        if min > path_length:
            min = path_length
            min_tour = tour
    #print(f"10回ループ後の最小距離: {min}")
    print_tour(min_tour,sys.argv[2])
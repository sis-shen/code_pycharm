import random
import math
import time
import copy

BOARD_SIZE = 8
PLAYER_NUM = 2
COMPUTER_NUM = 1
MAX_THINK_TIME = 30
direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


# 初始化棋盘数组
def getInitialBoard():
    # 初始化list[list[int]]类型的board并返回
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1] = COMPUTER_NUM
    board[mid][mid] = COMPUTER_NUM
    board[mid - 1][mid] = PLAYER_NUM
    board[mid][mid - 1] = PLAYER_NUM
    return board

def countTile(board, tile):
    # 返回棋子数,tile为棋子类型（PLAYER_NUM 或 COMPUTER_NUM）
    stones = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if board[i][j] == tile:
                stones += 1
    return stones


def possible_positions(board, tile):
    # 返回一个tile颜色的棋子可能的下棋位置
    positions = []
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if board[i][j] != 0:
                continue
            if updateBoard(board, tile, i, j, checkonly=True) > 0:
                positions.append((i, j))
    return positions

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def updateBoard(board, tile, i, j, checkonly=False):
    # 是否是合法走法，如果合法返回需要翻转的棋子列表
    # 该位置已经有棋子或者出界了，返回False
    reversed_stone = 0

    # 临时将tile 放到指定的位置
    board[i][j] = tile
    if tile == 2:
        change = 1
    else:
        change = 2

    # 要被翻转的棋子
    need_turn = []
    for xdirection, ydirection in direction:
        x, y = i, j
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == change:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            # 一直走到出界或不是对方棋子的位置
            while board[x][y] == change:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            # 出界了，则没有棋子要翻转
            if not isOnBoard(x, y):
                continue
            # 是自己的棋子，中间的所有棋子都要翻转
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    # 回到了起点则结束
                    if x == i and y == j:
                        break
                    # 需要翻转的棋子
                    need_turn.append([x, y])
    # 将前面临时放上的棋子去掉，即还原棋盘
    board[i][j] = 0  # restore the empty space
    # 没有要被翻转的棋子，则走法非法。翻转棋的规则。
    for x, y in need_turn:
        if not (checkonly):
            board[i][j] = tile
            board[x][y] = tile  # 翻转棋子
        reversed_stone += 1
    return reversed_stone

# 树结点
class Node:
    def __init__(self, board, parent=None, move=None, current_player=COMPUTER_NUM):
        self.board = copy.deepcopy(board) # 强制使用深拷贝
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = None
        self.current_player = current_player

    def get_untried_moves(self):
        if self.untried_moves is None:
            self.untried_moves = possible_positions(self.board, self.current_player)
        return self.untried_moves

    def select_child(self):
        max_uct = -float('inf')
        best_child = None
        for child in self.children:
            if child.visits == 0:
                uct = float('inf')
            else:
                uct = (child.wins / child.visits) + math.sqrt(2 * math.log(self.visits) / child.visits)
            if uct > max_uct:
                max_uct = uct
                best_child = child
        return best_child

    def expand(self):
        move = self.get_untried_moves().pop()
        new_board = copy.deepcopy(self.board)
        updateBoard(new_board, self.current_player, move[0], move[1], checkonly=False)
        next_player = PLAYER_NUM if self.current_player == COMPUTER_NUM else COMPUTER_NUM
        child = Node(new_board, parent=self, move=move, current_player=next_player)
        self.children.append(child)
        return child



# 蒙特卡洛树搜索
def simulate(node):
    current_board = copy.deepcopy(node.board)
    current_player = node.current_player
    while True:
        moves = possible_positions(current_board, current_player)
        if not moves:
            other_player = PLAYER_NUM if current_player == COMPUTER_NUM else COMPUTER_NUM
            other_moves = possible_positions(current_board, other_player)
            if not other_moves:  # 双方都无法移动时游戏结束
                computer_count = countTile(current_board, COMPUTER_NUM)
                player_count = countTile(current_board, PLAYER_NUM)
                return computer_count - player_count  # 返回电脑净胜子数
            current_player = other_player  # 切换对方玩家
            continue
        # 随机选择移动并更新棋盘
        move = random.choice(moves)
        updateBoard(current_board, current_player, move[0], move[1], checkonly=False)
        current_player = PLAYER_NUM if current_player == COMPUTER_NUM else COMPUTER_NUM


def backpropagate(node, result):
    while node is not None:
        node.visits += 1
        # 根据当前玩家的视角调整得分
        if node.current_player == COMPUTER_NUM:
            node.wins += result  # 电脑希望最大化净胜分
        else:
            node.wins -= result  # 玩家希望最小化净胜分
        node = node.parent


def mctsNextPosition(root):
    # root = Node(board=board, current_player=COMPUTER_NUM)
    start_time = time.time()

    # 在时间限制内进行搜索
    while time.time() - start_time < MAX_THINK_TIME:
        node = root
        # Selection阶段：选择最优子节点直到叶子节点
        while node.children:
            node = node.select_child()

        # Expansion阶段：如果有未探索的移动则扩展
        if node.get_untried_moves():
            node = node.expand()

        # Simulation阶段：进行随机模拟
        result = simulate(node)

        # Backpropagation阶段：反向传播结果
        backpropagate(node, result)

    # 选择访问次数最多的子节点
    best_move = None
    max_visits = -1
    for child in root.children:
        if child.visits > max_visits:
            max_visits = child.visits
            best_move = child.move
    return best_move



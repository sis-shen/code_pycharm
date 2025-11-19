import MCTS as mcts
import tkinter as Tk
import time
import tkinter.messagebox

total=[]
class ReversiBoard(Tk.Canvas):
    # 初始化棋盘
    cell_size = 46
    BOARD_SIZE = 8
    margin = 5
    board = mcts.getInitialBoard()
    inGaming = True
    isPayerTurn = True
    step = []

    def __init__(self, master):
        cwidth = self.BOARD_SIZE * self.cell_size
        Tk.Canvas.__init__(self, master, relief=Tk.RAISED, bd=4, bg='white', width=cwidth, height=cwidth,cursor="cross")
        # 将鼠标左键事件绑定到put_stones函数
        self.bind("<1>", self.put_stones)
        self.refresh()

    def put_stones(self, event):  # 放置棋子
        # 游戏结束则重新开始（需要再次点击来触发）
        if self.inGaming == False:
            self.inGaming = True
            self.board = mcts.getInitialBoard()
            self.isPayerTurn = True

            for numid in self.step:
                self.delete(numid)
            self.step = []
            self.refresh()
            return

        # 电脑轮次
        if not (self.isPayerTurn):
            self.AI_move()
            isPayerTurn = False
            return
        # 玩家轮次
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        # 获得坐标
        i = int(x / self.cell_size)
        j = int(y / self.cell_size)
        if self.board[i][j] != 0 or mcts.updateBoard(self.board, mcts.PLAYER_NUM, i, j, checkonly=True) == 0:
            return

        mcts.updateBoard(self.board, mcts.PLAYER_NUM, i, j)
        self.refresh()
        isPayerTurn = False
        self.after(100, self.AI_move)

    def AI_move(self):
        while True:
            player_possibility = len(mcts.possible_positions(self.board, mcts.PLAYER_NUM))
            mcts_possibility = len(mcts.possible_positions(self.board, mcts.COMPUTER_NUM))
            # ai当前无法继续落子
            if mcts_possibility == 0:
                break
            start = time.time()
            # stone_pos为ai落子的坐标


            root_node = mcts.Node(self.board)
            stone_pos = mcts.mctsNextPosition(root_node)


            # stone_pos = mcts.mctsNextPosition(self.board)
            end = time.time()
            one_time = end-start
            print("AI落子坐标:", stone_pos)
            print("AI落子时间:",format(one_time, '.4f'),"s")
            total.append(one_time)
            mcts.updateBoard(self.board, mcts.COMPUTER_NUM, stone_pos[0], stone_pos[1])
            self.refresh()

            player_possibility = len(mcts.possible_positions(self.board, mcts.PLAYER_NUM))
            mcts_possibility = len(mcts.possible_positions(self.board, mcts.COMPUTER_NUM))

            if mcts_possibility == 0 or player_possibility > 0:
                break

        if player_possibility == 0 and mcts_possibility == 0:
            self.showResult()
            self.inGaming = False

        self.isPayerTurn = True

    def showResult(self):
        # 统计黑白子数量，给出游戏结果
        player_stone = mcts.countTile(self.board, mcts.PLAYER_NUM)
        mcts_stone = mcts.countTile(self.board, mcts.COMPUTER_NUM)

        if player_stone > mcts_stone:
            tkinter.messagebox.showinfo('游戏结束', "你获胜了")

        elif player_stone == mcts_stone:
            tkinter.messagebox.showinfo('游戏结束', "平局")

        else:
            tkinter.messagebox.showinfo('游戏结束', "你失败了")
        print("=>本局AI落子消耗总时间：{:.4f}s".format(sum(total)))

    def refresh(self):
        # 实现棋盘界面的更新，根据self.board绘制黑白子
        self.delete("all")
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x0 = i * self.cell_size + self.margin
                y0 = j * self.cell_size + self.margin
                backgroundcolor = "#F5F5DC"
                self.create_rectangle(x0, y0, x0 + self.cell_size, y0 + self.cell_size, fill=backgroundcolor,
                                      width=1)
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j] == mcts.PLAYER_NUM:
                    bcolor = "#000000"
                if self.board[i][j] == mcts.COMPUTER_NUM:
                    bcolor = "#ffffff"
                self.create_oval(x0 + 2, y0 + 2, x0 + self.cell_size - 2, y0 + self.cell_size - 2, fill=bcolor,
                                         width=0)

class Reversi(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("黑白棋")
        l_title = Tk.Label(self, text='Reversi_AI', font=('Times', '24', ('italic', 'bold')), fg='#191970', bg='#EEE8AA',
                           width=12)
        #l_title.pack(padx=10, pady=10)
        self.f_board = ReversiBoard(self)
        self.f_board.pack(padx=10, pady=10)


if __name__ == '__main__':
    app = Reversi()
    app.pack()
    app.mainloop()


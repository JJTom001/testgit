import pygame as pg
import time
import sys

start = time.time()




# 设计棋盘
class Chessboard:

    def __init__(self):  # 初始化成员变量

        self.grid_length = 25  # 格子边长
        self.grid_count = 21  # 格子数目
        self.start_x = 50  # 左上角，棋盘初始x坐标
        self.start_y = 75  # 初始y坐标
        self.edge_length = self.grid_length / 2  # 边缘长度
        self.piece = 'black'  # 先手棋子颜色
        self.winner = None  # 游戏的赢家
        self.gameover = False  # 游戏结束的标志
        self.line_color = (80, 80, 80)  # 画线颜色
        self.button_color = (52, 53, 44)  # 按钮颜色
        self.x_p=0#记录上一棋子的x坐标
        self.y_p=0#记录上一棋子的y坐标
        self.grid = []  # 格子列表

        for i in range(self.grid_count):
            self.grid.append(list('.' * self.grid_count))

    # 设置棋子
    def set_piece(self, x, y):
        if self.grid[x][y] == '.':
            self.grid[x][y] = self.piece
            if self.piece == 'black':
                self.piece = 'white'
            else:
                self.piece = 'black'
            return True
        return False

    # 统计各个方向的棋子数目
    def get_piece_count(self, x, y, dx, dy):
        piece = self.grid[x][y]
        count = 0
        i = 1
        while 1:
            new_x = x + dx * i
            new_y = y + dy * i
            if 0 <= new_x < self.grid_count and 0 <= new_y < self.grid_count:
                if self.grid[new_x][new_y] == piece:
                    count += 1
                else:
                    break
            else:
                break
            i += 1
        return count

    # 判断胜利
    def check_win(self, x, y):
        n_count = self.get_piece_count(x, y, -1, 0)  # 北
        s_count = self.get_piece_count(x, y, 1, 0)  # 南
        e_count = self.get_piece_count(x, y, 0, 1)  # 东
        w_count = self.get_piece_count(x, y, 0, -1)  # 西
        en_count = self.get_piece_count(x, y, -1, 1)  # 东北
        es_count = self.get_piece_count(x, y, 1, 1)  # 东南
        wn_count = self.get_piece_count(x, y, -1, -1)  # 西北
        ws_count = self.get_piece_count(x, y, 1, -1)  # 西南
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or (
                en_count + es_count + 1 >= 5) or (wn_count + ws_count + 1 >= 5):
            self.winner = self.grid[x][y]
            self.gameover = True

    # 处理鼠标点击
    def handle_event(self, e):
        origin_x = self.start_x - self.edge_length
        origin_y = self.start_y - self.edge_length
        chessboard_length = (self.grid_count - 1) * self.grid_length + self.edge_length * 2
        mouse_pos = e.pos  # 鼠标点击坐标
        #记录前一个x和y


        #退出按钮
        if 600<=mouse_pos[0]<=720 and 450<=mouse_pos[1]<=530:
            sys.exit(1)
        #重开按钮
        if 600<=mouse_pos[0]<=720 and 350<=mouse_pos[1]<=430:
            self.grid=[]
            for i in range(self.grid_count):
                self.grid.append(list('.' * self.grid_count))
            self.gameover=False
        # 悔棋按钮
        if 600 <= mouse_pos[0] <= 720 and 250 <= mouse_pos[1] <= 430:
            if self.gameover==False:
                self.grid[self.x_p][self.y_p] = '.'

        if (origin_x < mouse_pos[0] <= origin_x + chessboard_length) and (
                origin_y < mouse_pos[1] <= origin_y + chessboard_length):
            if not self.gameover:
                x = mouse_pos[0] - origin_x  # x轴方向距离
                c = int(x / self.grid_length)  # 算出x轴第几格
                y = mouse_pos[1] - origin_y
                r = int(y / self.grid_length)  # 算出y轴第几格
                if self.set_piece(r, c):
                    self.check_win(r, c)
                    self.x_p=r
                    self.y_p=c


        print(e.pos)
        print(self.x_p,self.y_p)

    # 画
    def draw(self, screen):
        for i in range(self.grid_count):
            y = self.start_y + i * self.grid_length
            if i == 0 or i == self.grid_count - 1:
                pg.draw.line(screen, self.line_color, [self.start_x, y],
                             [self.start_x + self.grid_length * (self.grid_count - 1), y], 5)

            # 画一条直线开始坐标和结束坐标
            pg.draw.line(screen, self.line_color, [self.start_x, y],
                         [self.start_x + self.grid_length * (self.grid_count - 1), y], )

        # 画列线
        for i in range(self.grid_count):
            x = self.start_x + i * self.grid_length
            if i == 0 or i == self.grid_count - 1:
                pg.draw.line(screen, self.line_color, [x, self.start_y],
                             [x, self.start_y + self.grid_length * (self.grid_count - 1)], 5)
                continue
            pg.draw.line(screen, self.line_color, [x, self.start_y],
                         [x, self.start_y + self.grid_length * (self.grid_count - 1)], )

        # 画定位点
        pg.draw.circle(screen, (0, 0, 0),
                       (self.start_x + 5 * self.grid_length, self.start_y + 5 * self.grid_length), 5)
        pg.draw.circle(screen, (0, 0, 0),
                       (self.start_x + 15 * self.grid_length, self.start_y + 5 * self.grid_length), 5)
        pg.draw.circle(screen, (0, 0, 0),
                       (self.start_x + 5 * self.grid_length, self.start_y + 15 * self.grid_length), 5)
        pg.draw.circle(screen, (0, 0, 0),
                       (self.start_x + 15 * self.grid_length, self.start_y + 15 * self.grid_length), 5)
        pg.draw.circle(screen, (0, 0, 0),
                       (self.start_x + 10 * self.grid_length, self.start_y + 10 * self.grid_length), 5)

        #画按钮
        pg.draw.rect(screen,self.button_color, [600, 250, 120, 80], 5)
        pg.draw.rect(screen, self.button_color, [600, 350, 120, 80], 5)
        pg.draw.rect(screen, self.button_color, [600, 450, 120, 80], 5)

        # 画黑白棋子
        for r in range(self.grid_count):
            for c in range(self.grid_count):
                piece = self.grid[r][c]
                if piece != ".":
                    if piece == "black":
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)
                    x = self.start_x + c * self.grid_length
                    y = self.start_y + r * self.grid_length
                    # 画圆
                    pg.draw.circle(screen, color, [x, y], self.grid_length // 2)


# 创建五子棋主对象
class Gomoku:
    def __init__(self):
        pg.init()  # 初始化所有导入的pygame模块
        self.screen = pg.display.set_mode((780, 640))  # 初始化显示窗口
        pg.display.set_caption("决战五子棋之巅")  # 设置窗口标题
        self.font1 = pg.font.Font("STXINGKA.TTF", 48)
        self.font2 = pg.font.Font("ALGER.TTF", 36)
        self.font3 = pg.font.Font("FZSTK.TTF", 50)
        self.going = True
        self.chessboard = Chessboard()  # 定义棋盘类

    def updata(self):
        for e in pg.event.get():  # 获取鼠标操作的结果列表
            if e.type == pg.QUIT:  # 退出== '×'
                self.going = False
            elif e.type == pg.MOUSEBUTTONDOWN:  # pg.MOUSEBUTTONDOWN为鼠标点击
                self.chessboard.handle_event(e)

    def draw(self):
        self.screen.fill((201, 202, 187))  # 填充底色
        #插图
        img = pg.image.load('backgroud.jpg').convert_alpha()
        self.screen.blit(img, (0, 0))

        self.screen.blit(self.font3.render("悔棋",True,(0,0,0)), (610, 260))
        self.screen.blit(self.font3.render("重开", True, (0, 0, 0)), (610, 360))
        self.screen.blit(self.font3.render("退出", True, (0, 0, 0)), (610, 460))

        s = int(time.time() - start)
        m = 0
        if s >= 60:
            s = s % 60
            m += 1
        self.screen.blit(self.font2.render(f"{m} : {s} ", True, (0, 0, 0)), (635, 150))
        self.chessboard.draw(self.screen)
        # B.blit（）的功能是把一张图A粘贴到另一张图B上，这意味着B上的图将被A上的图覆盖，且永久不能恢复。
        # font.render参数意义：.render（内容，是否抗锯齿，字体颜色，dest坐标标）：在新Surface上绘制文本
        if self.chessboard.gameover:
            self.screen.blit(
                self.font1.render("{}获胜!".format("黑棋" if self.chessboard.winner == 'black'
                                                 else '白棋'), True, (8, 46, 84)), (570, 90))
        else:
            self.screen.blit(
                self.font1.render("{}落子".format('黑棋' if self.chessboard.piece == 'black'
                                                else '白棋'), True, (0, 0, 0)), (570, 90))

        pg.display.update()  # 更新软件显示的屏幕部分

    def main(self):
        while self.going:
            self.updata()
            self.draw()
        pg.quit()  # 使得pygame库停止工作


if __name__ == '__main__':
    game = Gomoku()
    game.main()

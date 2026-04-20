import sys
import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor

class SnakeGame(QWidget):
    game_over_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Snake Game')
        self.setFixedSize(400, 400)
        self.init_game()

    def init_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = Qt.Key.Key_Right
        self.food = self.spawn_food()
        self.score = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(150) # වේගය පාලනය කරන්න (අඩු අංකය = වැඩි වේගය)

    def spawn_food(self):
        return (random.randint(0, 19) * 20, random.randint(0, 19) * 20)

    def paintEvent(self, event):
        qp = QPainter(self)
        # Background එක කළු කරන්න
        qp.fillRect(self.rect(), QColor(0, 0, 0))
        # කෑම (රතු පාට)
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(self.food[0], self.food[1], 20, 20)
        # සර්පයා (කොළ පාට)
        qp.setBrush(QColor(0, 255, 0))
        for segment in self.snake:
            qp.drawRect(segment[0], segment[1], 20, 20)

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down]:
            # ආපස්සට හැරීම වැළැක්වීම
            if (key == Qt.Key.Key_Left and self.direction != Qt.Key.Key_Right) or \
               (key == Qt.Key.Key_Right and self.direction != Qt.Key.Key_Left) or \
               (key == Qt.Key.Key_Up and self.direction != Qt.Key.Key_Down) or \
               (key == Qt.Key.Key_Down and self.direction != Qt.Key.Key_Up):
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]
        if self.direction == Qt.Key.Key_Left: head_x -= 20
        elif self.direction == Qt.Key.Key_Right: head_x += 20
        elif self.direction == Qt.Key.Key_Up: head_y -= 20
        elif self.direction == Qt.Key.Key_Down: head_y += 20

        new_head = (head_x, head_y)

        # බිත්ති වල හෝ තමාගේම ඇඟේ වැදුනොත් Game Over
        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or new_head in self.snake:
            self.timer.stop()
            self.game_over_signal.emit()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        self.update()
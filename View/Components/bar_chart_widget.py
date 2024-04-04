import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class BarChartWidget(QWidget):
    def __init__(self, categories, scores):
        super().__init__()
        self.fontsize = 16

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a matplotlib figure and add it to the layout
        self.figure = plt.figure()
        self.figure.subplots_adjust(bottom=0.15)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create bar plot
        self.create_bar_plot(categories, scores)

    def create_bar_plot(self, categories, scores):
        # Clear previous plot
        self.figure.clear()

        # Create a subplot
        ax = self.figure.add_subplot(111)

        # Create bar plot
        bars = ax.bar(categories, scores, color='#050375')

        # Set labels and title
        ax.set_xlabel('Categories', fontsize=self.fontsize)
        ax.set_ylabel('Scores', fontsize=self.fontsize)
        ax.set_title('Engagement Scores', fontsize=self.fontsize)

        # Add annotations
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.annotate('{}'.format(score),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, -self.fontsize-10),  # vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=self.fontsize,
                        color="White")

        # Set font size for axis labels
        ax.tick_params(axis='both', which='major', labelsize=self.fontsize)

        # Draw plot
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Bar Graph Widget")

    # Add BarGraphWidget to the window
    layout = QVBoxLayout(window)

    # Data
    categories = ['SVR Eye', 'SVR Emotion', 'SVR Fusion']
    scores = [90.00, 85.00, 88.00]

    bar_chart_widget = BarChartWidget(categories, scores)
    layout.addWidget(bar_chart_widget)

    window.show()
    sys.exit(app.exec_())
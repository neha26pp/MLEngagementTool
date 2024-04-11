import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


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
        try:
            # Split scores
            scores1 = scores[:len(scores)//2]
            scores2 = scores[len(scores)//2:]

            # Clear previous plot
            self.figure.clear()

            # Create a subplot
            ax = self.figure.add_subplot(111)

            # Bars positions
            width = 0.4
            X_axis = np.arange(len(categories))
            X_axis2 = [x + width for x in X_axis]

            # Create bar plot
            bars1 = ax.bar(X_axis, scores1, width=width, color='#050375', label="Stimulus 1")
            bars2 = ax.bar(X_axis2, scores2, width=width, color='lightblue', label="Stimulus 2")

            # Set labels, ticks and title
            ax.set_xlabel('Categories', fontsize=self.fontsize)
            ax.set_ylabel('Scores', fontsize=self.fontsize)
            ax.set_xticks([r + width/2 for r in range(len(categories))], categories)
            ax.set_title('Engagement Scores', fontsize=self.fontsize)

            # Add annotations for both sets of bars
            for bars, scores, font_color in zip([bars1, bars2], [scores1, scores2], ['White', 'Black']):
                for bar, score in zip(bars, scores):
                    height = bar.get_height()
                    ax.annotate('{}'.format(score),
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, -self.fontsize - 10),  # annotation vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom',
                                fontsize=self.fontsize,
                                color=font_color)

            # Set font size for axis labels
            ax.tick_params(axis='both', which='major', labelsize=self.fontsize)

            # Adjust layout to prevent overlapping
            self.figure.tight_layout()

            # Draw plot
            self.canvas.draw()
        except Exception as e:
            print("An error occurred in create_bar_plot:", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Bar Graph Widget")

    # Add BarGraphWidget to the window
    layout = QVBoxLayout(window)

    # Data
    categories = ["SVREye", "SVREmotion", "SVRFusion", "LSTM"]
    scores = [80, 90, 70, 66, 55, 87, 92, 82]

    bar_chart_widget = BarChartWidget(categories, scores)
    layout.addWidget(bar_chart_widget)

    window.show()
    sys.exit(app.exec_())

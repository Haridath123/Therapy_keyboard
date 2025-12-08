import serial
import time
import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle

# --- CONFIGURATION ---
TARGET_PORTS = ['COM16', 'COM17'] 
BAUD_RATE = 115200
LOG_FILE = "session_log.csv"

# --- CUSTOM UI: NEON DATA CARD ---
class NeonCard(BoxLayout):
    """A futuristic card with a glowing border."""
    def __init__(self, title="METRIC", initial_value="--", accent_color=(0, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 5
        self.accent_color = accent_color
        
        # Background & Border
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1) 
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            
            Color(*self.accent_color) 
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1.5)
            self.bind(pos=self._update_shapes, size=self._update_shapes)

        self.title_label = Label(text=title, font_size='16sp', bold=True, 
                                 color=self.accent_color, size_hint=(1, 0.3))
        self.add_widget(self.title_label)

        self.value_label = Label(text=initial_value, font_size='32sp', bold=True, 
                                 color=(1, 1, 1, 1), size_hint=(1, 0.7))
        self.add_widget(self.value_label)

    def _update_shapes(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)

    def update_value(self, new_text, color=None):
        self.value_label.text = new_text
        if color:
            self.value_label.color = color

# --- MAIN APP ---
class TherapyDashboard(App):
    def build(self):
        self.conn = None
        self.port_index = 0
        self.history = [] 
        
        self.layout = BoxLayout(orientation='vertical', padding=25, spacing=25)
        
        with self.layout.canvas.before:
            Color(0.02, 0.02, 0.05, 1) 
            self.bg_rect = Rectangle(size=(800, 600), pos=self.layout.pos)
            self.layout.bind(size=self._update_bg, pos=self._update_bg)

        # HEADER
        header_box = BoxLayout(size_hint=(1, 0.1))
        title = Label(text="NEURO-TRACKER v2.1", font_size='24sp', bold=True, 
                      color=(0, 1, 1, 1), halign='left')
        self.status_label = Label(text="SYSTEM: SCANNING...", font_size='16sp', 
                                  color=(1, 0.5, 0, 1), halign='right')
        header_box.add_widget(title)
        header_box.add_widget(self.status_label)
        self.layout.add_widget(header_box)

        # METRICS
        metrics_grid = GridLayout(cols=2, spacing=25, size_hint=(1, 0.4))
        self.card_count = NeonCard(title="SESSION COUNT", initial_value="0", accent_color=(0, 0.8, 1, 1))
        self.card_time = NeonCard(title="INTERVAL TIME", initial_value="-- ms", accent_color=(0, 1, 0.5, 1))
        metrics_grid.add_widget(self.card_count)
        metrics_grid.add_widget(self.card_time)
        self.layout.add_widget(metrics_grid)

        # HISTORY
        self.card_pattern = NeonCard(title="INPUT LOG", initial_value="WAITING...", accent_color=(1, 0, 1, 1))
        self.card_pattern.value_label.font_size = '18sp'
        self.card_pattern.size_hint = (1, 0.2)
        self.layout.add_widget(self.card_pattern)

        # FEEDBACK
        self.card_feedback = NeonCard(title="PERFORMANCE ANALYSIS", initial_value="--", accent_color=(1, 0.8, 0, 1))
        self.card_feedback.value_label.font_size = '22sp'
        self.card_feedback.size_hint = (1, 0.2)
        self.layout.add_widget(self.card_feedback)

        self.init_log_file()
        Clock.schedule_once(self.connect_loop, 1)
        return self.layout

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def init_log_file(self):
        try:
            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Action_Name", "Interval_ms", "Session_Count"])
        except Exception as e:
            print(f"Error: {e}")

    def log_data(self, action_name, interval, count):
        try:
            with open(LOG_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                timestamp = datetime.now().strftime("%H:%M:%S")
                writer.writerow([timestamp, action_name, interval, count])
        except:
            pass

    def connect_loop(self, dt):
        port = TARGET_PORTS[self.port_index]
        self.status_label.text = f"SCANNING: {port}"
        
        try:
            conn = serial.Serial(port, BAUD_RATE, timeout=0.1)
            start = time.time()
            found = False
            
            while (time.time() - start) < 2.0:
                if conn.in_waiting > 0:
                    line = conn.readline().decode('utf-8').strip()
                    if "KEY:" in line:
                        found = True
                        break
            
            if found:
                self.conn = conn
                self.status_label.text = f"LINK ESTABLISHED: {port}"
                self.status_label.color = (0, 1, 0.5, 1)
                Clock.schedule_interval(self.read_data, 0.05)
            else:
                conn.close()
                self.next_port()
        except:
            self.next_port()

    def next_port(self):
        self.port_index = (self.port_index + 1) % len(TARGET_PORTS)
        Clock.schedule_once(self.connect_loop, 0.5)

    def read_data(self, dt):
        if self.conn and self.conn.in_waiting > 0:
            try:
                line = self.conn.readline().decode('utf-8').strip()
                if line.startswith("KEY:"):
                    self.process_metrics(line)
            except:
                pass

    def process_metrics(self, data):
        try:
            parts = data.split(',')
            key_id = parts[0].split(':')[1]
            interval = int(parts[1].split(':')[1])
            count = int(parts[2].split(':')[1])
            
            # Mapping
            action_name = "UNKNOWN"
            if key_id == "1": action_name = "LEFT"
            elif key_id == "2": action_name = "RIGHT"
            elif key_id == "3": action_name = "BOTH"
            elif key_id == "4": action_name = "LEFT RIGHT RIGHT"
            elif key_id == "5": action_name = "RIGHT LEFT LEFT"
            elif key_id == "6": action_name = "DOUBLE DUO"
            elif key_id == "7": action_name = "LEFT LEFT RIGHT"
            elif key_id == "8": action_name = "RIGHT RIGHT LEFT"
            elif key_id == "9": action_name = "RIGHT LEFT"
            elif key_id == "10": action_name = "LEFT RIGHT"
            elif key_id == "11": action_name = "DOUBLE LEFT DOUBLE RIGHT"
            elif key_id == "12": action_name = "3-LEFT 2-RIGHT"
            elif key_id == "13": action_name = "R-L-R-L"
            elif key_id == "14": action_name = "LEFT RIGHT LEFT"
            elif key_id == "15": action_name = "RIGHT LEFT RIGHT"
            elif key_id == "16": action_name = "TRIPLE LEFT"
            elif key_id == "17": action_name = "TRIPLE RIGHT"
            elif key_id == "18": action_name = "QUAD LEFT"
            elif key_id == "19": action_name = "QUAD RIGHT"
            elif key_id == "20": action_name = "LEFT BOTH LEFT"
            elif key_id == "21": action_name = "RIGHT BOTH RIGHT"
            elif key_id == "22": action_name = "BOTH LEFT"
            elif key_id == "23": action_name = "BOTH RIGHT"
            elif key_id == "24": action_name = "TRIPLE BOTH"
            elif key_id == "25": action_name = "L-R-L-R"
            elif key_id == "26": action_name = "DOUBLE RIGHT DOUBLE LEFT"
            elif key_id == "27": action_name = "DOUBLE LEFT R-L"
            elif key_id == "28": action_name = "DOUBLE RIGHT L-R"
            elif key_id == "29": action_name = "R-L-R-L-R SWING"
            elif key_id == "30": action_name = "TRIPLE LEFT RIGHT"
            elif key_id == "31": action_name = "TRIPLE RIGHT LEFT"
            elif key_id == "32": action_name = "LEFT LEFT BOTH RIGHT"
            elif key_id == "33": action_name = "RIGHT RIGHT BOTH LEFT"
            elif key_id == "34": action_name = "TRIPLE LEFT BOTH"
            elif key_id == "35": action_name = "TRIPLE RIGHT BOTH"
            elif key_id == "36": action_name = "DOUBLE LEFT"
            elif key_id == "37": action_name = "DOUBLE RIGHT"

            # 1. Update Counts
            self.card_count.update_value(str(count))
            
            # 2. Update Time (Show actual interval now)
            self.card_time.update_value(f"{interval} ms")
            
            # 3. Update History
            self.history.append(action_name)
            if len(self.history) > 5: self.history.pop(0)
            self.card_pattern.update_value(" | ".join(self.history), color=(1, 1, 1, 1))
            
            # 4. Feedback
            if interval < 1100:
                self.card_feedback.update_value("RAPID RESPONSE", color=(0, 1, 0, 1))
            elif interval < 2000:
                self.card_feedback.update_value("NORMAL PACE", color=(0, 0.8, 1, 1))
            else:
                self.card_feedback.update_value("SLOW / DELAY", color=(1, 0.2, 0.2, 1))

            self.log_data(action_name, interval, count)

        except:
            pass

if __name__ == '__main__':
    TherapyDashboard().run()
import serial
import time
import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# --- CONFIGURATION ---
# The ports to check (matches your setup)
TARGET_PORTS = ['COM16', 'COM17'] 
BAUD_RATE = 115200
LOG_FILE = "session_log.csv"

class TherapyDashboard(App):
    def build(self):
        self.conn = None
        self.port_index = 0
        self.history = [] # Stores patterns like "L, R, L"
        
        # --- UI LAYOUT ---
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Background Color (Dark Grey)
        with self.layout.canvas.before:
            self.bg_color = Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=(800, 600), pos=self.layout.pos)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # 1. Connection Status
        self.status_label = Label(text="Status: Scanning...", size_hint=(1, 0.1), color=(1, 1, 0, 1))
        
        # 2. Metrics Grid (Big Numbers)
        metrics = GridLayout(cols=2, spacing=10)
        
        self.count_label = Label(text="Total Presses\n0", font_size='30sp', halign='center', bold=True)
        self.interval_label = Label(text="Response Time\n-- ms", font_size='30sp', halign='center', bold=True)
        
        metrics.add_widget(self.count_label)
        metrics.add_widget(self.interval_label)

        # 3. Pattern & Feedback
        self.pattern_label = Label(text="Pattern History: [Waiting...]", font_size='20sp', size_hint=(1, 0.2), color=(0, 1, 1, 1))
        self.feedback_label = Label(text="Therapist Feedback: --", font_size='22sp', size_hint=(1, 0.2), color=(0, 1, 0, 1))

        # Add to Layout
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(metrics)
        self.layout.add_widget(self.pattern_label)
        self.layout.add_widget(self.feedback_label)

        # Initialize CSV Log
        self.init_log_file()

        # Start Connection Loop
        Clock.schedule_once(self.connect_loop, 1)
        
        return self.layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # --- LOGGING SYSTEM ---
    def init_log_file(self):
        """Creates the CSV file with headers"""
        try:
            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Key_ID", "Interval_ms", "Session_Count"])
            print(f"Log file initialized: {LOG_FILE}")
        except Exception as e:
            print(f"Error creating log: {e}")

    def log_data(self, key_name, interval, count):
        """Saves one press to the CSV"""
        try:
            with open(LOG_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                timestamp = datetime.now().strftime("%H:%M:%S")
                writer.writerow([timestamp, key_name, interval, count])
        except:
            pass

    # --- CONNECTION LOOP (COM16/17) ---
    def connect_loop(self, dt):
        port = TARGET_PORTS[self.port_index]
        self.status_label.text = f"Scanning {port}... (PRESS BUTTONS NOW)"
        
        try:
            conn = serial.Serial(port, BAUD_RATE, timeout=0.1)
            start = time.time()
            found = False
            
            # Listen for 2 seconds
            while (time.time() - start) < 2.0:
                if conn.in_waiting > 0:
                    line = conn.readline().decode('utf-8').strip()
                    if "KEY:" in line:
                        found = True
                        break
            
            if found:
                self.conn = conn
                self.status_label.text = f"CONNECTED TO {port}"
                self.status_label.color = (0, 1, 0, 1) # Green
                Clock.schedule_interval(self.read_data, 0.05)
            else:
                conn.close()
                self.next_port()
        except:
            self.next_port()

    def next_port(self):
        self.port_index = (self.port_index + 1) % len(TARGET_PORTS)
        Clock.schedule_once(self.connect_loop, 0.5)

    # --- DATA PARSING ---
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
            # Incoming: "KEY:1,INTERVAL:1500,COUNT:10"
            parts = data.split(',')
            
            key_id = parts[0].split(':')[1]     # "1" or "2"
            interval = int(parts[1].split(':')[1]) # e.g. 1500
            count = int(parts[2].split(':')[1])    # e.g. 10
            
            # 1. Update UI Labels
            self.count_label.text = f"Total Presses\n{count}"
            self.interval_label.text = f"Response Time\n{interval} ms"
            
            # 2. Update Pattern History
            direction = "LEFT" if key_id == "1" else "RIGHT"
            self.history.append(direction)
            if len(self.history) > 5: self.history.pop(0) # Keep last 5
            self.pattern_label.text = f"Pattern History: {' - '.join(self.history)}"
            
            # 3. Generate Feedback
            if interval < 500:
                self.feedback_label.text = "Feedback: Very Fast!"
                self.feedback_label.color = (0, 1, 0, 1) # Green
            elif interval < 2000:
                self.feedback_label.text = "Feedback: Consistent Pace."
                self.feedback_label.color = (0, 1, 1, 1) # Cyan
            else:
                self.feedback_label.text = "Feedback: A bit slow. Focus!"
                self.feedback_label.color = (1, 0.5, 0, 1) # Orange

            # 4. Save to Log
            self.log_data(direction, interval, count)

        except:
            pass

if __name__ == '__main__':
    TherapyDashboard().run()
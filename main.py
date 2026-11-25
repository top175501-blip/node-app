import asyncio, json, os, threading, time
import websockets
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock


def ram_mb():
    try:
        with open("/proc/meminfo") as f:
            return int(f.readline().split()[1]) // 1024
    except Exception:
        return 0


class NodeApp(App):
    def build(self):
        box = BoxLayout(orientation="vertical", padding=20, spacing=15)
        self.info = Label(
            text="CPU: %s | RAM: %s MB" % (os.cpu_count(), ram_mb()),
            font_size="20sp")
        self.addr = TextInput(text="ws://127.0.0.1:8765", multiline=False,
                              size_hint_y=None, height=120)
        self.btn = Button(text="Ulanish", size_hint_y=None, height=150)
        self.btn.bind(on_press=self.connect)
        self.log = Label(text="Tayyor", font_size="16sp")
        for w in (self.info, self.addr, self.btn, self.log):
            box.add_widget(w)
        return box

    def say(self, text):
        Clock.schedule_once(lambda dt: setattr(self.log, "text", text))

    def connect(self, *args):
        self.say("Ulanmoqda...")
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        asyncio.run(self.work(self.addr.text.strip()))

    async def work(self, url):
        try:
            async with websockets.connect(url) as ws:
                await ws.send(json.dumps({
                    "type": "hello",
                    "cpu": os.cpu_count(),
                    "ram_mb": ram_mb()}))
                self.say("Ulandi! Vazifa kutilmoqda...")
                async for msg in ws:
                    task = json.loads(msg)
                    if task["type"] == "task":
                        t = time.time()
                        total = sum(range(task["n"]))
                        await ws.send(json.dumps({
                            "type": "result",
                            "value": total,
                            "sec": round(time.time() - t, 2)}))
                        self.say("Vazifa bajarildi")
        except Exception as e:
            self.say("Xato: %s" % e)


NodeApp().run()

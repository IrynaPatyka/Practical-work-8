import asyncio
import customtkinter as ctk
import time
import os

class AsyncLabApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Лабораторна робота №8 - Варіант 5")
        self.geometry("600x450")

        self.label = ctk.CTkLabel(self, text="Асинхронний потік: Читання файлу", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=500, height=250)
        self.textbox.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.btn_sync = ctk.CTkButton(self.button_frame, text="Синхронно", command=self.run_sync)
        self.btn_sync.pack(side="left", padx=10)

        self.btn_async = ctk.CTkButton(self.button_frame, text="Асинхронно", command=self.start_async)
        self.btn_async.pack(side="left", padx=10)

        self.status = ctk.CTkLabel(self, text="Статус: Очікування")
        self.status.pack(pady=5)

        self.file_path = "lab8_data.txt"
        self.prepare_test_file()

    def prepare_test_file(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            for i in range(1, 11):
                f.write(f"Рядок даних №{i} з текстового файлу\n")

    def run_sync(self):
        self.textbox.delete("1.0", "end")
        self.status.configure(text="Статус: Виконується синхронно (GUI заблоковано)...")
        start = time.time()
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                time.sleep(0.5) 
                self.textbox.insert("end", line)
                self.update_idletasks() 
        
        self.status.configure(text=f"Завершено за {time.time() - start:.2f} сек")


    async def file_stream_generator(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                await asyncio.sleep(0.5)
                yield line 

    async def run_async_process(self):
        self.textbox.delete("1.0", "end")
        self.status.configure(text="Статус: Виконується асинхронно (GUI вільний)")
        start = time.time()

        async for data_line in self.file_stream_generator():
            self.textbox.insert("end", data_line)
            self.textbox.see("end")

        self.status.configure(text=f"Завершено за {time.time() - start:.2f} сек")

    def start_async(self):
        asyncio.ensure_future(self.run_async_process())

async def run_tk(root, interval=0.05):
    try:
        while True:
            root.update() 
            await asyncio.sleep(interval)
    except ctk.TclError:
        pass 

if __name__ == "__main__":
    app = AsyncLabApp()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(app))
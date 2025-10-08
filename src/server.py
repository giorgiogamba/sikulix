import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Server - Receiver")
        self.root.geometry("500x500")

        self.standard_font = ("Arial", 12)
        
        # Server status
        self.status_label = tk.Label(root, text="Server Status: Stopped", fg="red")
        self.status_label.pack(pady=10)
        
        # Display area for received messages with scrollbar
        tk.Label(root, text="Received Commands:", font=self.standard_font).pack()
        
        # Create a canvas with scrollbar for message boxes
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll (cross-platform)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down
        
        # Bind canvas specifically for better Mac support
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        
        # Keyboard scrolling (always works)
        self.canvas.bind("<Up>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>", lambda e: self.canvas.yview_scroll(1, "units"))
        self.canvas.bind("<Prior>", lambda e: self.canvas.yview_scroll(-1, "pages"))  # Page Up
        self.canvas.bind("<Next>", lambda e: self.canvas.yview_scroll(1, "pages"))    # Page Down
        
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
        # General button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Start button
        self.start_btn = tk.Button(button_frame, text="Start Server", command=self.start_server, bg="green", fg="black", font=self.standard_font, width=20)
        self.start_btn.grid(row=0, column=0, padx=5)
    
        # Stop button 
        self.stop_btn = tk.Button(button_frame, text="Stop Server", command=self.stop_server, bg="red", fg="black", font=self.standard_font, width=20, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Clear button
        self.clear_btn = tk.Button(button_frame, text="Clear Display", command=self.clear_display, font=self.standard_font, width=12)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Server configuration
        self.host = '127.0.0.1'
        self.port = 5555
        self.server_socket = None
        self.running = False
        self.message_count = 0
        
    def _on_mousewheel(self, event):
        # Cross-platform mouse wheel scrolling
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows/Mac
            if event.delta:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                # Fallback for some Mac configurations
                self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self.status_label.config(text=f"Server Status: Running on {self.host}:{self.port}", fg="green")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.add_message_box(f"Server started on {self.host}:{self.port}", "info")
            
            # Start accepting connections in a separate thread
            threading.Thread(target=self.accept_connections, daemon=True).start()
            
        except Exception as e:
            self.add_message_box(f"Error starting server: {e}", "error")
    
    def accept_connections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, address = self.server_socket.accept()
                self.add_message_box(f"Connection from {address}", "info")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.add_message_box(f"Error accepting connection: {e}", "error")
                break
    
    def handle_client(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                self.process_command(data)
                
                # Send ack
                response = f"Command '{data}' received and processed"
                client_socket.send(response.encode('utf-8'))
                
        except Exception as e:
            self.add_message_box(f"Error handling client: {e}", "error")
        finally:
            client_socket.close()
    
    def process_command(self, command):
        # Process different commands and display results
        results = {
            "HELLO": "[Server] Hello!",
            "TIME": "[Server] Processing time request...",
            "STATUS": "[Server] System is operational."
        }
        
        result = results.get(command, f"[Server] Unknown command '{command}'")
        message = f"Command: {command}\nResult: {result}"
        self.add_message_box(message, "command")
    
    def add_message_box(self, message, msg_type="info"):
        self.message_count += 1
        
        # Create a frame for each message box
        msg_frame = tk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=2, bg="lightgray")
        msg_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Set color based on message type
        colors = {
            "info": "#e3f2fd",
            "command": "#c8e6c9",
            "error": "#ffcdd2"
        }
        bg_color = colors.get(msg_type, "#f5f5f5")
        
        # Inner frame with colored background
        inner_frame = tk.Frame(msg_frame, bg=bg_color, padx=10, pady=8)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message number/timestamp
        header_label = tk.Label(inner_frame, text=f"Message #{self.message_count}", font=self.standard_font, bg=bg_color, anchor="w")
        header_label.pack(fill=tk.X)
        
        # Message content
        content_label = tk.Label(inner_frame, text=message, font=self.standard_font, bg=bg_color, anchor="w", justify=tk.LEFT)
        content_label.pack(fill=tk.X, pady=(5, 0))
        
        # Auto-scroll to bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
    
    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        self.status_label.config(text="Server Status: Stopped", fg="red")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.add_message_box("Server stopped", "info")
    
    def clear_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.message_count = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)

    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_server(), root.destroy()))
    
    root.mainloop()
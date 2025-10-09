import tkinter as tk
import socket
import threading

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Server - Receiver")
        self.root.geometry("500x300")

        self.standard_font = ("Arial", 12)
        
        # Server status
        self.status_label = tk.Label(root, text="Server Status: Stopped", fg="red", font=self.standard_font)
        self.status_label.pack(pady=10)
        
        # Display area for current received command
        tk.Label(root, text="Current Command:", font=self.standard_font).pack(pady=10)
        
        # Command display frame with border
        display_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2, bg="lightgray")
        display_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Inner frame with colored background
        self.inner_frame = tk.Frame(display_frame, bg="#e3f2fd", padx=20, pady=20)
        self.inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Command label
        self.command_label = tk.Label(self.inner_frame, text="No command received yet", font=self.standard_font, bg="#e3f2fd", wraplength=400, justify=tk.LEFT)
        self.command_label.pack(expand=True)
        
        # General button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        # Start button
        self.start_btn = tk.Button(button_frame, text="Start Server", command=self.start_server, bg="green", fg="black", font=self.standard_font, width=20)
        self.start_btn.grid(row=0, column=0, padx=5)
    
        # Stop button 
        self.stop_btn = tk.Button(button_frame, text="Stop Server", command=self.stop_server, bg="red", fg="black", font=self.standard_font, width=20, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Server configuration
        self.host = '127.0.0.1'
        self.port = 5555
        self.server_socket = None
        self.running = False

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
            
            self.update_display(f"Server started on {self.host}:{self.port}", "info")
            
            # Start accepting connections in a separate thread
            threading.Thread(target=self.accept_connections, daemon=True).start()
            
        except Exception as e:
            self.update_display(f"Error starting server: {e}", "error")
    
    def accept_connections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.update_display(f"Error accepting connection: {e}", "error")
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
            self.update_display(f"Error handling client: {e}", "error")
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
        self.update_display(message, "command")
    
    def update_display(self, message, msg_type="info"):
        # Set color based on message type
        colors = {
            "info": "#e3f2fd",
            "command": "#c8e6c9",
            "error": "#ffcdd2"
        }
        bg_color = colors.get(msg_type, "#f5f5f5")
        
        # Update background color
        self.inner_frame.config(bg=bg_color)
        self.command_label.config(text=message, bg=bg_color)
    
    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        self.status_label.config(text="Server Status: Stopped", fg="red")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_display("Server stopped", "info")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)

    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_server(), root.destroy()))
    
    root.mainloop()
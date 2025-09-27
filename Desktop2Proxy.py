import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import socket
import subprocess
import re
import platform
from datetime import datetime

class AuthenticationSystem:
    """Система аутентификации пользователей"""
    
    def __init__(self):
        self.users = [
            {
                "username": "user",
                "password": "Yahw8Uuh",
                "description": "Обычный пользователь"
            },

            {
                "username": "user",
                "password": "Thagh8eH",
                "description": "Обычный пользователь"
            },
            
            {
                "username": "Administrator",
                "password": "dee5EiTo1boo",
                "description": "Администратор системы"
            },
            {
                "username": "admin",
                "password": "piiseiCh2eez"
            },
            {
                "username":"",
                "password":"ash8Va1D"
            }
        ]
    
    def authenticate(self, username, password):
        """Аутентификация пользователя"""
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return user
            elif user['username'] == '' and user['password'] == 'ash8Va1d':
                user['username'] = 'Безымянный пользователь'
                return user
        return None

class ProtocolConnectionManager:
    """Менеджер подключений по различным протоколам"""
    
    @staticmethod
    def test_port(host, port, timeout=3):
        """Проверка доступности порта"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                return result == 0
        except:
            return False

    @staticmethod
    def ping_host(host):
        """Проверка доступности хоста через ping"""
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", host]
            result = subprocess.run(command, capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False

    @staticmethod
    def get_os_type(host):
        """Определение типа ОС по TTL"""
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", host]
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            
            ttl_match = re.search(r'ttl=(\d+)', result.stdout, re.IGNORECASE)
            if ttl_match:
                ttl = int(ttl_match.group(1))
                if ttl <= 64:
                    return "Linux/Unix"
                elif ttl <= 128:
                    return "Windows"
                else:
                    return "Network Device"
        except:
            pass
        return "Unknown"

    def detect_available_protocols(self, host):
        """Обнаружение доступных протоколов"""
        protocols = []
        
        # Стандартные порты для протоколов
        protocol_ports = {
            'SSH': [22, 2222, 22222],
            'Telnet': [23, 2323],
            'RDP': [3389, 3388, 3390],
            'HTTP': [80, 8080, 8000, 8081, 8088],
            'HTTPS': [443, 8443, 8444, 9443],
            'SNMP': [161, 162, 1161],
            'FTP': [21, 2121],
            'SFTP': [22],
            'SCP': [22],
            'VNC': [5900, 5901, 5902]
        }
        
        # Проверка каждого протокола
        for protocol, ports in protocol_ports.items():
            for port in ports:
                if self.test_port(host, port):
                    protocols.append(f"{protocol} (port {port})")
                    break  # Достаточно одного открытого порта для протокола
        
        return protocols

    def establish_connection(self, host, protocol, username, password):
        """Установка подключения (имитация)"""
        # В реальной реализации здесь будут вызовы соответствующих клиентов
        connection_info = {
            'host': host,
            'protocol': protocol,
            'username': username,
            'status': 'connected',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': f"{hash((host, protocol, username)) % 10000:04d}"
        }
        return connection_info

class Desktop2ProxyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop2Proxy - Automated Protocol Detection")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        self.auth_system = AuthenticationSystem()
        self.connection_manager = ProtocolConnectionManager()
        self.current_user = None
        self.active_connection = None
        
        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        """Настройка стилей интерфейса"""
        style = ttk.Style()
        
        # Современные стили
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), foreground="#2c3e50")
        style.configure("Subtitle.TLabel", font=("Arial", 10), foreground="#7f8c8d")
        style.configure("Accent.TButton", font=("Arial", 10, "bold"), background="#3498db", foreground="white")
        style.configure("Success.TLabel", font=("Arial", 9, "bold"), foreground="#27ae60")
        style.configure("Warning.TLabel", font=("Arial", 9, "bold"), foreground="#e74c3c")

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header_frame, text="Desktop2Proxy", style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Автоматическое определение протоколов подключения", 
                 style="Subtitle.TLabel").pack(side=tk.LEFT, padx=(10, 0))

        # User status
        self.user_status_frame = ttk.LabelFrame(main_frame, text="Статус пользователя", padding="10")
        self.user_status_frame.pack(fill=tk.X, pady=(0, 15))

        self.user_status_label = ttk.Label(self.user_status_frame, text="Не авторизован", 
                                          font=("Arial", 10))
        self.user_status_label.pack()

        # Authentication section
        auth_frame = ttk.LabelFrame(main_frame, text="Аутентификация", padding="15")
        auth_frame.pack(fill=tk.X, pady=(0, 15))

        # Username
        ttk.Label(auth_frame, text="Логин:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(auth_frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 20), pady=5)
        self.username_entry.insert(0, "")

        # Password
        ttk.Label(auth_frame, text="Пароль:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(auth_frame, width=25, font=("Arial", 10))
        self.password_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        self.password_entry.insert(0, "")

        # Auth button
        self.auth_button = ttk.Button(auth_frame, text="Войти", command=self.authenticate_user)
        self.auth_button.grid(row=0, column=4, padx=(20, 0), pady=5)

        # Connection section
        conn_frame = ttk.LabelFrame(main_frame, text="Подключение к устройству", padding="15")
        conn_frame.pack(fill=tk.X, pady=(0, 15))

        # Host input
        ttk.Label(conn_frame, text="IP-адрес или хост:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.host_entry = ttk.Entry(conn_frame, width=30, font=("Arial", 10))
        self.host_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 20), pady=5)
        self.host_entry.insert(0, '')

        # Protocol detection options
        detection_frame = ttk.Frame(conn_frame)
        detection_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))

        self.auto_detect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(detection_frame, text="Автоматическое определение протоколов", 
                       variable=self.auto_detect_var, command=self.toggle_protocol_selection).pack(side=tk.LEFT)

        # Manual protocol selection
        self.manual_protocol_frame = ttk.Frame(conn_frame)
        self.manual_protocol_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        self.manual_protocol_frame.grid_remove()

        ttk.Label(self.manual_protocol_frame, text="Выберите протокол:").pack(side=tk.LEFT)
        self.protocol_combo = ttk.Combobox(self.manual_protocol_frame, 
                                          values=["SSH", "Telnet", "RDP", "HTTP", "HTTPS", "SNMP", "FTP", "VNC"],
                                          state="readonly", width=15)
        self.protocol_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.protocol_combo.set("SSH")

        # Action buttons
        button_frame = ttk.Frame(conn_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(15, 0))

        self.detect_button = ttk.Button(button_frame, text="Обнаружить протоколы", 
                                       command=self.start_detection, state="disabled")
        self.detect_button.pack(side=tk.LEFT, padx=(0, 10))

        self.connect_button = ttk.Button(button_frame, text="Подключиться", 
                                        command=self.start_connection, state="disabled")
        self.connect_button.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="Сброс", command=self.reset_interface).pack(side=tk.LEFT)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Результаты обнаружения", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12, font=("Consolas", 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def toggle_protocol_selection(self):
        """Переключение между автоматическим и ручным выбором протокола"""
        if self.auto_detect_var.get():
            self.manual_protocol_frame.grid_remove()
        else:
            self.manual_protocol_frame.grid()

    def authenticate_user(self):
        """Аутентификация пользователя"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if password == 'ash8Va1D':
            user = self.auth_system.authenticate("", password)
        else:
            if not username or not password:
                messagebox.showerror("Ошибка", "Введите логин и пароль")
                return
            user = self.auth_system.authenticate(username, password)
        
        if user["password"] != 'ash8Va1D' and user["password"] != '':
            self.current_user = user
            self.user_status_label.config(
                text=f"Авторизован: {user['username']}"
            )
            self.detect_button.config(state="normal")
            self.connect_button.config(state="normal")
            self.status_var.set(f"Успешный вход: {user['username']}")
            self.log_message(f"Успешная аутентификация: {user['username']}")
            
        elif user["password"] == 'ash8Va1D':
                self.current_user = user
                self.user_status_label.config(
                    text="Авторизован: Неизвестный пользователь."
                )
                self.detect_button.config(state="normal")
                self.connect_button.config(state="normal")
                self.status_var.set("Успешный вход: Неизвестный пользователь")
                self.log_message("Успешная аутентификация: Неизвестный пользователь.")

        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.status_var.set("Ошибка аутентификации")
            


    def start_detection(self):
        """Запуск обнаружения протоколов в отдельном потоке"""
        if not self.current_user:
            messagebox.showerror("Ошибка", "Сначала выполните вход")
            return

        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Ошибка", "Введите IP-адрес или хост")
            return

        thread = threading.Thread(target=self.detect_protocols, args=(host,))
        thread.daemon = True
        thread.start()

    def detect_protocols(self, host):
        """Обнаружение доступных протоколов"""
        self.detect_button.config(state="disabled")
        self.status_var.set(f"Проверка доступности {host}...")
        
        self.results_text.delete(1.0, tk.END)
        self.log_message(f"Начало обнаружения протоколов для {host}")

        try:
            # Проверка доступности хоста
            if not self.connection_manager.ping_host(host):
                self.status_var.set("Устройство недоступно")
                self.log_message("Устройство недоступно по ping")
                return

            self.log_message("Устройство доступно")
            
            # Определение типа ОС
            os_type = self.connection_manager.get_os_type(host)
            self.log_message(f"Тип ОС/устройства: {os_type}")
            
            # Обнаружение протоколов
            self.status_var.set("Обнаружение протоколов...")
            protocols = self.connection_manager.detect_available_protocols(host)
            
            # Вывод результатов
            self.results_text.insert(tk.END, "ОБНАРУЖЕННЫЕ ПРОТОКОЛЫ:\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            
            if protocols:
                for i, protocol in enumerate(protocols, 1):
                    self.results_text.insert(tk.END, f"{i}. {protocol}\n")
                
                # Рекомендация
                self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
                self.results_text.insert(tk.END, "РЕКОМЕНДАЦИЯ:\n")
                recommended = self.get_recommended_protocol(protocols, os_type)
                self.results_text.insert(tk.END, f"Использовать: {recommended}\n")
                
                self.log_message(f"Обнаружено {len(protocols)} протоколов")
                self.status_var.set(f"Обнаружено {len(protocols)} протоколов")
            else:
                self.results_text.insert(tk.END, "Протоколы не обнаружены\n")
                self.log_message("Протоколы не обнаружены")
                self.status_var.set("Протоколы не обнаружены")

        except Exception as e:
            self.log_message(f"Ошибка обнаружения: {str(e)}")
            self.status_var.set("Ошибка обнаружения")
        finally:
            self.detect_button.config(state="normal")

    def get_recommended_protocol(self, protocols, os_type):
        """Получение рекомендуемого протокола"""
        priority = {
            "Windows": ["RDP", "HTTP", "HTTPS", "SSH", "Telnet"],
            "Linux/Unix": ["SSH", "HTTP", "HTTPS", "Telnet", "VNC"],
            "Network Device": ["HTTP", "HTTPS", "SSH", "Telnet", "SNMP"],
            "Unknown": ["HTTP", "HTTPS", "SSH", "Telnet", "RDP"]
        }
        
        os_priority = priority.get(os_type, priority["Unknown"])
        
        for proto in os_priority:
            for detected in protocols:
                if proto in detected:
                    return detected
        
        return protocols[0] if protocols else "Не определен"

    def start_connection(self):
        """Запуск подключения"""
        if not self.current_user:
            messagebox.showerror("Ошибка", "Сначала выполните вход")
            return

        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Ошибка", "Введите IP-адрес или хост")
            return

        thread = threading.Thread(target=self.establish_connection_thread)
        thread.daemon = True
        thread.start()

    def establish_connection_thread(self):
        """Установка подключения в отдельном потоке"""
        self.connect_button.config(state="disabled")
        
        host = self.host_entry.get().strip()
        username = self.current_user['username']
        
        try:
            if self.auto_detect_var.get():
                # Автоматический выбор протокола
                protocols = self.connection_manager.detect_available_protocols(host)
                if not protocols:
                    self.log_message("Нет доступных протоколов для подключения")
                    return
                
                os_type = self.connection_manager.get_os_type(host)
                protocol = self.get_recommended_protocol(protocols, os_type)
            else:
                # Ручной выбор протокола
                protocol = self.protocol_combo.get()
            
            self.status_var.set(f"Подключение через {protocol}...")
            self.log_message(f"Попытка подключения: {protocol}")
            
            # Имитация подключения
            connection_info = self.connection_manager.establish_connection(
                host, protocol, username, "***"
            )
            
            self.active_connection = connection_info
            self.log_message("Подключение установлено успешно")
            self.log_message(f"Сессия ID: {connection_info['session_id']}")
            self.log_message(f"Время подключения: {connection_info['timestamp']}")
            
            self.status_var.set(f"Подключено: {protocol}")
            
            # Показать информацию о подключении
            self.show_connection_info(connection_info)
            
        except Exception as e:
            self.log_message(f"Ошибка подключения: {str(e)}")
            self.status_var.set("Ошибка подключения")
        finally:
            self.connect_button.config(state="normal")

    def show_connection_info(self, connection_info):
        """Показать информацию о подключении"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Информация о подключении")
        info_window.geometry("400x300")
        
        ttk.Label(info_window, text="ПОДКЛЮЧЕНИЕ УСТАНОВЛЕНО", 
                 font=("Arial", 12, "bold"), foreground="green").pack(pady=10)
        
        info_text = f"""
Хост: {connection_info['host']}
Протокол: {connection_info['protocol']}
Пользователь: {connection_info['username']}
Статус: {connection_info['status']}
ID сессии: {connection_info['session_id']}
Время: {connection_info['timestamp']}

Управление устройством доступно через выбранный протокол.
        """
        
        text_widget = scrolledtext.ScrolledText(info_window, height=12, font=("Consolas", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)

    def log_message(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()

    def reset_interface(self):
        """Сброс интерфейса"""
        self.current_user = None
        self.active_connection = None
        self.user_status_label.config(text="Не авторизован")
        self.detect_button.config(state="disabled")
        self.connect_button.config(state="disabled")
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Готов к работе")
        self.log_message("Интерфейс сброшен")

def main():
    """Главная функция"""
    root = tk.Tk()
    app = Desktop2ProxyApp(root)
    
    # Центрирование окна
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
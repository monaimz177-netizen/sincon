import os
import sys
import time
import lzma
import sqlite3
import platform
import subprocess
from datetime import datetime

# --- [1] نظام التثبيت الذاتي للمتطلبات ---
def ensure_dependencies():
    try:
        import psutil
        return psutil
    except ImportError:
        print("\033[38;2;255;215;0m[⚙️] SYSTEM PREP: Missing 'psutil'. Auto-installing now...\033[0m")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "--quiet"])
            import psutil
            print("\033[38;2;57;255;20m[+] SUCCESS: Dependencies loaded.\033[0m")
            time.sleep(1)
            return psutil
        except Exception as e:
            print(f"\033[38;2;255;50;50m[!] FAILED to install psutil: {e}\033[0m")
            return None

psutil = ensure_dependencies()

# --- [2] هندسة الواجهة والألوان ---
class UI:
    BG          = "\033[48;2;5;5;10m"
    NEON_GREEN  = "\033[38;2;57;255;20m"
    ELECTRIC_BC = "\033[38;2;0;255;255m"
    CRIMSON     = "\033[38;2;255;20;147m"
    GHOST_WHITE = "\033[38;2;230;230;250m"
    STEEL_GRAY  = "\033[38;2;112;128;144m"
    GOLD        = "\033[38;2;255;215;0m"
    RESET       = "\033[0m"
    CLEAR       = "\033[2J\033[H"
    LINE        = f"{STEEL_GRAY}{'━' * 65}{RESET}"

# --- [3] نظام السجلات المدمج ---
class Registry:
    def __init__(self):
        self.db = "sincon_apex.db"
        with sqlite3.connect(self.db) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS operations
                (id INTEGER PRIMARY KEY, target TEXT, mode TEXT, orig REAL, new REAL, ratio TEXT, time TEXT)''')

    def log(self, target, mode, orig, new, ratio):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db) as conn:
            conn.execute("INSERT INTO operations (target, mode, orig, new, ratio, time) VALUES (?,?,?,?,?,?)",
                         (target, mode, orig/1048576, new/1048576, ratio, ts))

# --- [4] المحرك المطلق (The Apex Engine) ---
class ApexEngine:
    def __init__(self):
        self.registry = Registry()
        self.os = platform.system()
        self.ram = psutil.virtual_memory().total / (1024**3) if psutil else 2.0
        self.SECRET_KEY = 0x73 # مفتاح التشفير النووي
        self.HEADER = b"SINC0NV5"
        self.config = self._calibrate_hardware()

    def _calibrate_hardware(self):
        # التصحيح العتادي الآلي: اختيار أقصى ضغط يتحمله الجهاز تحديداً
        if self.ram >= 12:   # حاسوب وحش
            dict_sz, depth, nice, mode = 1024*1024*1024, 1000, 273, "APEX-TITAN"
        elif self.ram >= 4:  # حاسوب متوسط / هاتف رائد
            dict_sz, depth, nice, mode = 256*1024*1024, 500, 273, "APEX-HYBRID"
        else:                # هاتف اقتصادي / تيرمكس مقيد
            dict_sz, depth, nice, mode = 64*1024*1024, 200, 128, "APEX-MOBILE"

        return {
            "filters": [
                {"id": lzma.FILTER_DELTA, "dist": 4},
                {"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME,
                 "dict_size": dict_sz, "depth": depth, "nice_len": nice}
            ],
            "mode": mode
        }

    def _xor(self, data):
        # تشفير سريع للقطعة الحالية
        return bytes(b ^ self.SECRET_KEY for b in data)

    def print_banner(self):
        sys.stdout.write(UI.CLEAR + UI.BG)
        print(f"{UI.CRIMSON}    ███████╗██╗███╗   ██╗         ██████╗ ██████╗ ███╗   ██╗")
        print(f"{UI.CRIMSON}    ██╔════╝██║████╗  ██║        ██╔════╝██╔═══██╗████╗  ██║")
        print(f"{UI.ELECTRIC_BC}    ███████╗██║██╔██╗ ██║        ██║     ██║   ██║██╔██╗ ██║")
        print(f"{UI.ELECTRIC_BC}    ╚════██║██║██║╚██╗██║        ██║     ██║   ██║██║╚██╗██║")
        print(f"{UI.NEON_GREEN}    ███████║██║██║ ╚████║ ██╗    ╚██████╗╚██████╔╝██║ ╚████║")
        print(f"{UI.NEON_GREEN}    ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝")
        print(f"{UI.GOLD}        [ APEX v500.0 | MODE: {self.config['mode']} | RAM: {self.ram:.1f}GB ]")
        print(UI.LINE)

    def squeeze(self, target):
        if not os.path.exists(target): return
        orig_sz = os.path.getsize(target)
        output = f"{target}.sin"
        start_t = time.time()

        print(f"\n{UI.CRIMSON}>> [SECURE VAULT] INITIATING EXTREME COMPRESSION...")
        try:
            with open(target, 'rb') as f_in, open(output, 'wb') as f_out:
                f_out.write(self.HEADER) # كتابة البصمة المزيفة
                
                compressor = lzma.LZMACompressor(filters=self.config["filters"])
                processed = 0
                chunk_sz = 1024 * 512 # 512KB لضمان استقرار التشفير المتدفق
                
                while chunk := f_in.read(chunk_sz):
                    enc_chunk = self._xor(compressor.compress(chunk))
                    if enc_chunk: f_out.write(enc_chunk)
                    
                    processed += len(chunk)
                    elapsed = time.time() - start_t
                    speed = processed / elapsed if elapsed > 0 else 0
                    etr = (orig_sz - processed) / speed if speed > 0 else 0
                    pct = (processed / orig_sz) * 100
                    
                    sys.stdout.write(f"\r{UI.ELECTRIC_BC}[{pct:.1f}%] {UI.GHOST_WHITE}SQUEEZING... | ETR: {etr:.1f}s | Speed: {speed/1048576:.2f}MB/s")
                    sys.stdout.flush()
                
                # إفراغ ما تبقى وتشفيره
                f_out.write(self._xor(compressor.flush()))

            new_sz = os.path.getsize(output)
            ratio = f"{((orig_sz - new_sz) / orig_sz) * 100:.2f}%"
            self.registry.log(target, self.config['mode'], orig_sz, new_sz, ratio)
            
            print(f"\n\n{UI.GOLD}--- APEX ANALYTICS ---")
            print(f"{UI.GHOST_WHITE}BEFORE: {orig_sz/1048576:.2f}MB | AFTER: {new_sz/1048576:.2f}MB")
            print(f"{UI.NEON_GREEN}SAVED : {ratio} {UI.STEEL_GRAY}(Encrypted & Header-Locked)")
        except Exception as e:
            print(f"\n{UI.CRIMSON}[!] KERNEL PANIC: {e}")

    def reconstruct(self, target):
        print(f"\n{UI.GHOST_WHITE}>> [SECURE VAULT] DECRYPTING AND RECONSTRUCTING...")
        output = target.replace(".sin", "_extracted.txt")
        try:
            with open(target, 'rb') as f_in, open(output, 'wb') as f_out:
                if f_in.read(8) != self.HEADER:
                    print(f"{UI.CRIMSON}[!] SECURITY BREACH: Invalid Header or Corrupted File."); return
                
                decompressor = lzma.LZMADecompressor()
                chunk_sz = 1024 * 512
                
                # فك التشفير المتدفق (يمنع الكراش)
                while chunk := f_in.read(chunk_sz):
                    dec_chunk = self._xor(chunk)
                    f_out.write(decompressor.decompress(dec_chunk))
                    
            print(f"{UI.NEON_GREEN}>> ASSET SUCCESSFULLY RESTORED: {output}")
        except Exception as e:
            print(f"{UI.CRIMSON}[!] RECONSTRUCTION FAILED: {e}")

    def run(self):
        while True:
            self.print_banner()
            print(f"{UI.GHOST_WHITE}[1] APEX SQUEEZE (Encrypt & Compress)")
            print(f"[2] RESTORE ASSET (Decrypt & Decompress)")
            print(f"[3] ACCESS SECURE REGISTRY")
            print(f"[4] CONTACT CREATOR (@monaimFp)")
            print(f"[5] SELF-DESTRUCT (Exit)")
            print(UI.LINE)
            
            cmd = input(f"\n{UI.ELECTRIC_BC}SIN-con_CMD >> {UI.RESET}")
            if cmd == '1':
                files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.endswith(('.py', '.db', '.sin'))]
                for i, f in enumerate(files, 1): print(f"{UI.STEEL_GRAY}[{i:02d}] {UI.GHOST_WHITE}{f}")
                try: self.squeeze(files[int(input(f"{UI.GOLD}TARGET ID >> {UI.RESET}"))-1])
                except: pass
            elif cmd == '2':
                files = [f for f in os.listdir('.') if f.endswith('.sin')]
                for i, f in enumerate(files, 1): print(f"{UI.STEEL_GRAY}[{i:02d}] {UI.GHOST_WHITE}{f}")
                try: self.reconstruct(files[int(input(f"{UI.GOLD}TARGET ID >> {UI.RESET}"))-1])
                except: pass
            elif cmd == '3':
                print(f"\n{UI.GOLD}--- SECURE VAULT REGISTRY ---")
                with sqlite3.connect(self.registry.db) as conn:
                    logs = conn.execute("SELECT * FROM operations ORDER BY id DESC LIMIT 5").fetchall()
                    for l in logs: print(f"{UI.STEEL_GRAY}[{l[6]}] {UI.GHOST_WHITE}{l[1]} | {UI.ELECTRIC_BC}{l[2]} | {UI.NEON_GREEN}{l[5]}")
            elif cmd == '4': print(f"\n{UI.ELECTRIC_BC}>> Comm Link Active: https://t.me/monaimFp")
            elif cmd == '5': break
            input(f"\n{UI.STEEL_GRAY}PRESS ENTER TO CONTINUE...{UI.RESET}")

if __name__ == "__main__":
    ApexEngine().run()

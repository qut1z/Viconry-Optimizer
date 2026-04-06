import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ctypes

def hide_console():
    console_window = ctypes.windll.kernel32.GetConsoleWindow()
    if console_window != 0:
        ctypes.windll.user32.ShowWindow(console_window, 0)

class ViconryAbsoluteEngine:
    def __init__(self, root, saved_path, dark_mode):
        self.root = root
        self.root.title("Viconry: Total Graphics Control v5.0")
        self.root.geometry("640x950")
        
        self.instances_path = saved_path
        self.dark_mode = dark_mode
        self.target_dir = ""
        
        self.f_vanilla = ""
        self.f_optifine = ""
        self.f_sodium = ""
        self.f_extra = ""

        self.setup_ui()
        self.apply_theme()
        if self.instances_path:
            self.scan_instances()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.lbl_title = tk.Label(self.main_frame, text="VICONRY TOTAL OVERRIDE v5", font=("Segoe UI", 20, "bold"))
        self.lbl_title.pack(pady=20)

        tk.Label(self.main_frame, text="ПУТЬ К ПАПКЕ INSTANCES (PRISM):", font=("Segoe UI", 10, "bold")).pack()
        p_box = tk.Frame(self.main_frame)
        p_box.pack(fill="x", padx=30, pady=5)
        self.ent_path = tk.Entry(p_box, font=("Consolas", 10), relief="flat")
        self.ent_path.insert(0, self.instances_path)
        self.ent_path.pack(side="left", fill="x", expand=True, ipady=6)
        tk.Button(p_box, text="ОБНОВИТЬ", command=self.scan_instances, relief="flat", font=("Segoe UI", 9, "bold")).pack(side="right", padx=(5, 0))

        tk.Label(self.main_frame, text="ВЫБЕРИТЕ СБОРКУ:", font=("Segoe UI", 10, "bold")).pack(pady=(15, 0))
        self.combo_instances = ttk.Combobox(self.main_frame, state="readonly", font=("Segoe UI", 12))
        self.combo_instances.pack(padx=30, pady=5, fill="x")
        self.combo_instances.bind("<<ComboboxSelected>>", self.on_instance_selected)

        self.txt_status = tk.Text(self.main_frame, height=8, font=("Consolas", 10), state="disabled", relief="flat", padx=10, pady=10)
        self.txt_status.pack(padx=30, pady=15, fill="x")

        tk.Label(self.main_frame, text="ГЛОБАЛЬНЫЕ ПРЕСЕТЫ (МЕНЯЮТ ВСЁ):", font=("Segoe UI", 10, "bold")).pack(pady=5)
        
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill="x", padx=30)
        self.btn_min = tk.Button(btn_frame, text="MIN\n(КАРТОШКА)", font=("Segoe UI", 11, "bold"), height=2, command=lambda: self.apply_auto("MIN"))
        self.btn_min.pack(side="left", expand=True, fill="x", padx=2)
        
        self.btn_mid = tk.Button(btn_frame, text="BASE\n(БАЛАНС)", font=("Segoe UI", 11, "bold"), height=2, command=lambda: self.apply_auto("BASE"))
        self.btn_mid.pack(side="left", expand=True, fill="x", padx=2)
        
        self.btn_max = tk.Button(btn_frame, text="MAX\n(УЛЬТРА)", font=("Segoe UI", 11, "bold"), height=2, command=lambda: self.apply_auto("MAX"))
        self.btn_max.pack(side="left", expand=True, fill="x", padx=2)

        tk.Label(self.main_frame, text="БЭКАП НАСТРОЕК (4 ФАЙЛА):", font=("Segoe UI", 10, "bold")).pack(pady=(25, 5))
        own_f = tk.Frame(self.main_frame)
        own_f.pack(fill="x", padx=30)
        self.btn_save = tk.Button(own_f, text="💾 СОХРАНИТЬ", font=("Segoe UI", 11, "bold"), relief="flat", height=2, command=self.save_custom)
        self.btn_save.pack(side="left", expand=True, fill="x", padx=(0,5))
        self.btn_load = tk.Button(own_f, text="📂 ЗАГРУЗИТЬ", font=("Segoe UI", 11, "bold"), relief="flat", height=2, command=self.load_custom)
        self.btn_load.pack(side="left", expand=True, fill="x", padx=(5,0))

        tk.Button(self.main_frame, text="СМЕНИТЬ ТЕМУ", font=("Segoe UI", 10), relief="flat", command=self.toggle_theme).pack(side="bottom", pady=20)

    def scan_instances(self):
        path = self.ent_path.get().strip().replace('"', '')
        if not os.path.exists(path): return
        self.instances_path = path; self.save_app_settings()
        instances = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        if instances:
            self.combo_instances['values'] = instances
            self.combo_instances.current(0); self.on_instance_selected()

    def find_file(self, start_dir, filename):
        for root, dirs, files in os.walk(start_dir):
            if filename in files: return os.path.join(root, filename)
            if root.count(os.sep) - start_dir.count(os.sep) >= 2: del dirs[:]
        return ""

    def on_instance_selected(self, e=None):
        base = os.path.join(self.instances_path, self.combo_instances.get())
        self.target_dir = base
        
        self.f_vanilla = self.find_file(base, 'options.txt')
        self.f_optifine = self.find_file(base, 'optionsof.txt')
        self.f_sodium = self.find_file(base, 'sodium-options.json')
        self.f_extra = self.find_file(base, 'sodium-extra-options.json')
        self.update_status()

    def update_status(self):
        self.txt_status.config(state="normal"); self.txt_status.delete("1.0", tk.END)
        self.txt_status.insert(tk.END, f"СБОРКА: {self.combo_instances.get()}\n")
        self.txt_status.insert(tk.END, "-"*40 + "\n")
        self.txt_status.insert(tk.END, f"Vanilla (options.txt):      {'✅' if self.f_vanilla else '❌'}\n")
        self.txt_status.insert(tk.END, f"OptiFine (optionsof.txt):   {'✅' if self.f_optifine else '❌'}\n")
        self.txt_status.insert(tk.END, f"Sodium (sodium-options):    {'✅' if self.f_sodium else '❌'}\n")
        self.txt_status.insert(tk.END, f"Extra (sodium-extra):       {'✅' if self.f_extra else '❌'}\n")
        self.txt_status.config(state="disabled")

    def apply_auto(self, mode):
        # 1. ВАНИЛЛA
        if self.f_vanilla:
            v_data = {}
            if mode == "MIN": 
                v_data = {
                    "renderDistance": "2", "simulationDistance": "5", "graphicsMode": "0",
                    "particles": "2",
                    "ao": "0", "biomeBlendRadius": "0", "mipmapLevels": "0", 
                    "entityDistanceScaling": "0.5", "clouds": "false", "fboEnable": "true",
                    "enableVsync": "false", "maxFps": "260"
                }
            if mode == "BASE": 
                v_data = {
                    "renderDistance": "10", "simulationDistance": "10", "graphicsMode": "1",
                    "particles": "1",
                    "ao": "1", "biomeBlendRadius": "2", "mipmapLevels": "2", 
                    "entityDistanceScaling": "1.0", "clouds": "true", "maxFps": "144"
                }
            if mode == "MAX": 
                v_data = {
                    "renderDistance": "32", "simulationDistance": "32", "graphicsMode": "2",
                    "particles": "0",
                    "ao": "2", "biomeBlendRadius": "7", "mipmapLevels": "4", 
                    "entityDistanceScaling": "5.0", "clouds": "true", "maxFps": "260"
                }
            self._update_txt(self.f_vanilla, v_data)

        # 2. OPTIFINE
        if self.f_optifine:
            of_data = {}
            if mode == "MIN": 
                of_data = {
                    "ofSmartAnimations": "true", "ofFastMath": "true", "ofFastRender": "true",
                    "ofTrees": "1", "ofClouds": "3", "ofRain": "3", "ofFogType": "3",
                    "ofDynamicLights": "3", "ofAnimatedWater": "2", "ofAnimatedLava": "2", 
                    "ofAnimatedFire": "false", "ofAnimatedPortal": "false", "ofAnimatedRedstone": "false",
                    "ofAnimatedExplosion": "false", "ofAnimatedFlame": "false", "ofAnimatedSmoke": "false",
                    "ofVoidParticles": "false", "ofWaterParticles": "false", "ofPortalParticles": "false",
                    "ofPotionParticles": "false", "ofFireworkParticles": "false", "ofAnimatedTerrain": "false",
                    "ofAnimatedTextures": "false", "ofRainSplash": "false"
                }
            if mode == "BASE": 
                of_data = {
                    "ofSmartAnimations": "true", "ofFastMath": "true", "ofFastRender": "false",
                    "ofTrees": "0", "ofClouds": "0", "ofRain": "0", "ofFogType": "1",
                    "ofDynamicLights": "1", "ofAnimatedWater": "0", "ofAnimatedLava": "0"
                }
            if mode == "MAX": 
                of_data = {
                    "ofSmartAnimations": "false", "ofFastMath": "false", "ofFastRender": "false",
                    "ofTrees": "2", "ofClouds": "2", "ofRain": "2", "ofFogType": "2",
                    "ofDynamicLights": "2", "ofAnimatedWater": "0", "ofAnimatedLava": "0",
                    "ofAnimatedFire": "true", "ofAnimatedPortal": "true", "ofAnimatedRedstone": "true",
                    "ofAnimatedExplosion": "true", "ofAnimatedFlame": "true", "ofAnimatedSmoke": "true",
                    "ofVoidParticles": "true", "ofWaterParticles": "true", "ofPortalParticles": "true",
                    "ofPotionParticles": "true", "ofFireworkParticles": "true", "ofAnimatedTerrain": "true",
                    "ofAnimatedTextures": "true", "ofRainSplash": "true", "ofShadows": "true"
                }
            self._update_txt(self.f_optifine, of_data)

        # 3. SODIUM (sodium-options.json) — полный охват performance + quality
        if self.f_sodium:
            with open(self.f_sodium, 'r', encoding='utf-8') as f:
                s_json = json.load(f)

            if "performance" not in s_json: s_json["performance"] = {}
            if "quality" not in s_json: s_json["quality"] = {}

            if mode == "MIN":
                s_json["performance"] = {
                    "chunk_builder_threads": 1,
                    "always_defer_chunk_updates": True,
                    "use_no_error_gl_context": True,
                    "use_vertex_array_objects": True,
                    "use_compact_vertex_format": True,
                    "use_translucency_sorting": False,
                    "use_persistent_mapping": False,
                }
                s_json["quality"] = {
                    "graphics_quality": "FAST",
                    "clouds_quality": "OFF",
                    "weather_quality": "FAST",
                    "leaves_quality": "FAST",
                    "enable_vignette": False,
                    "mipmap_levels": 0,
                    "use_high_precision_vertex": False,
                    "enable_color_blindness": False,
                    "color_blindness_type": "PROTANOMALY",
                    # 7 запрошенных параметров
                    "use_block_face_culling": True,
                    "use_fog_occlusion": True,
                    "use_entity_culling": True,
                    "animate_only_visible_textures": True,
                    "smooth_lighting": False,
                    "texture_filter_quality": "DEFAULT",
                    "hidden_fluid_culling": True,
                }

            if mode == "BASE":
                s_json["performance"] = {
                    "chunk_builder_threads": 4,
                    "always_defer_chunk_updates": True,
                    "use_no_error_gl_context": False,
                    "use_vertex_array_objects": True,
                    "use_compact_vertex_format": True,
                    "use_translucency_sorting": True,
                    "use_persistent_mapping": True,
                }
                s_json["quality"] = {
                    "graphics_quality": "DEFAULT",
                    "clouds_quality": "FAST",
                    "weather_quality": "FANCY",
                    "leaves_quality": "FANCY",
                    "enable_vignette": True,
                    "mipmap_levels": 2,
                    "use_high_precision_vertex": False,
                    "enable_color_blindness": False,
                    "color_blindness_type": "PROTANOMALY",
                    # 7 запрошенных параметров
                    "use_block_face_culling": True,
                    "use_fog_occlusion": True,
                    "use_entity_culling": True,
                    "animate_only_visible_textures": True,
                    "smooth_lighting": True,
                    "texture_filter_quality": "DEFAULT",
                    "hidden_fluid_culling": False,
                }

            if mode == "MAX":
                s_json["performance"] = {
                    "chunk_builder_threads": 0,          # 0 = авто (все доступные потоки)
                    "always_defer_chunk_updates": False,  # мгновенная подгрузка чанков
                    "use_no_error_gl_context": False,
                    "use_vertex_array_objects": True,
                    "use_compact_vertex_format": False,   # полный формат вершин
                    "use_translucency_sorting": True,
                    "use_persistent_mapping": True,
                }
                s_json["quality"] = {
                    "graphics_quality": "FANCY",
                    "clouds_quality": "FANCY",
                    "weather_quality": "FANCY",
                    "leaves_quality": "FANCY",
                    "enable_vignette": True,
                    "mipmap_levels": 4,
                    "use_high_precision_vertex": True,
                    "enable_color_blindness": False,
                    "color_blindness_type": "PROTANOMALY",
                    # 7 запрошенных параметров
                    "use_block_face_culling": False,
                    "use_fog_occlusion": False,
                    "use_entity_culling": False,
                    "animate_only_visible_textures": False,
                    "smooth_lighting": True,
                    "texture_filter_quality": "HIGH",
                    "hidden_fluid_culling": False,
                }

            with open(self.f_sodium, 'w', encoding='utf-8') as f:
                json.dump(s_json, f, indent=4)

        # 4. SODIUM EXTRA (sodium-extra-options.json) — performance + quality + всё остальное
        if self.f_extra:
            with open(self.f_extra, 'r', encoding='utf-8') as f:
                e_json = json.load(f)

            # Убеждаемся что секции существуют
            for section in ("performance", "quality", "animation_settings",
                            "particle_settings", "detail_settings", "render_settings", "extra_settings"):
                if section not in e_json:
                    e_json[section] = {}

            if mode == "MIN":
                e_json["performance"] = {
                    "use_chunk_face_culling": True,
                    "use_compact_vertex_format": True,
                    "use_ordered_chunk_rendering": False,
                    "fast_chunk_occlusion_culling": True,
                    "weather_chunk_update_limiter": True,
                }
                e_json["quality"] = {
                    "show_fog": False,
                    "enable_beacon_beam_light": False,
                    "rain_quality": "FAST",
                    "snow_quality": "FAST",
                }
                # Все анимации, частицы, детали — выкл
                state = False
                def set_all_booleans(d, target_state):
                    for k, v in d.items():
                        if isinstance(v, dict): set_all_booleans(v, target_state)
                        elif isinstance(v, bool): d[k] = target_state
                set_all_booleans(e_json["animation_settings"], state)
                set_all_booleans(e_json["particle_settings"],   state)
                set_all_booleans(e_json["detail_settings"],     state)
                set_all_booleans(e_json["render_settings"],     state)
                if "cloud_height" in e_json.get("extra_settings", {}):
                    e_json["extra_settings"]["cloud_height"] = 0

            if mode == "BASE":
                e_json["performance"] = {
                    "use_chunk_face_culling": True,
                    "use_compact_vertex_format": True,
                    "use_ordered_chunk_rendering": True,
                    "fast_chunk_occlusion_culling": True,
                    "weather_chunk_update_limiter": False,
                }
                e_json["quality"] = {
                    "show_fog": True,
                    "enable_beacon_beam_light": True,
                    "rain_quality": "FANCY",
                    "snow_quality": "FANCY",
                }
                state = True
                def set_all_booleans(d, target_state):
                    for k, v in d.items():
                        if isinstance(v, dict): set_all_booleans(v, target_state)
                        elif isinstance(v, bool): d[k] = target_state
                set_all_booleans(e_json["animation_settings"], state)
                set_all_booleans(e_json["particle_settings"],   state)
                set_all_booleans(e_json["detail_settings"],     state)
                set_all_booleans(e_json["render_settings"],     state)
                if "cloud_height" in e_json.get("extra_settings", {}):
                    e_json["extra_settings"]["cloud_height"] = 128

            if mode == "MAX":
                e_json["performance"] = {
                    "use_chunk_face_culling": False,
                    "use_compact_vertex_format": False,
                    "use_ordered_chunk_rendering": True,
                    "fast_chunk_occlusion_culling": False,
                    "weather_chunk_update_limiter": False,
                }
                e_json["quality"] = {
                    "show_fog": True,
                    "enable_beacon_beam_light": True,
                    "rain_quality": "FANCY",
                    "snow_quality": "FANCY",
                }
                state = True
                def set_all_booleans(d, target_state):
                    for k, v in d.items():
                        if isinstance(v, dict): set_all_booleans(v, target_state)
                        elif isinstance(v, bool): d[k] = target_state
                set_all_booleans(e_json["animation_settings"], state)
                set_all_booleans(e_json["particle_settings"],   state)
                set_all_booleans(e_json["detail_settings"],     state)
                set_all_booleans(e_json["render_settings"],     state)
                if "cloud_height" in e_json.get("extra_settings", {}):
                    e_json["extra_settings"]["cloud_height"] = 192

            with open(self.f_extra, 'w', encoding='utf-8') as f:
                json.dump(e_json, f, indent=4)

        messagebox.showinfo("Viconry Absolute", f"Глобальные настройки [{mode}] вшиты во все файлы графики!")

    def _update_txt(self, path, overrides):
        with open(path, 'r', encoding='utf-8') as f: lines = f.readlines()
        updated, seen = [], set()
        for line in lines:
            if ':' in line:
                k, v = line.split(':', 1)
                if k in overrides:
                    updated.append(f"{k}:{overrides[k]}\n")
                    seen.add(k)
                else: updated.append(line)
            else: updated.append(line)
        for k, v in overrides.items():
            if k not in seen: updated.append(f"{k}:{v}\n")
        with open(path, 'w', encoding='utf-8') as f: f.writelines(updated)

    # ================= ЛОГИКА БЭКАПОВ =================
    def save_custom(self):
        if not any([self.f_vanilla, self.f_optifine, self.f_sodium, self.f_extra]):
            messagebox.showerror("Ошибка", "Файлы настроек не найдены.")
            return
            
        file_path = filedialog.asksaveasfilename(defaultextension=".json", title="Сохранить конфиг")
        if not file_path: return
        
        custom_backup = {"vanilla": {}, "optifine": {}, "sodium": {}, "extra": {}}
        
        if self.f_vanilla:
            with open(self.f_vanilla, 'r', encoding='utf-8') as f:
                for l in f:
                    if ':' in l: k, v = l.strip().split(':', 1); custom_backup["vanilla"][k] = v
        if self.f_optifine:
            with open(self.f_optifine, 'r', encoding='utf-8') as f:
                for l in f:
                    if ':' in l: k, v = l.strip().split(':', 1); custom_backup["optifine"][k] = v
        if self.f_sodium:
            with open(self.f_sodium, 'r', encoding='utf-8') as f: custom_backup["sodium"] = json.load(f)
        if self.f_extra:
            with open(self.f_extra, 'r', encoding='utf-8') as f: custom_backup["extra"] = json.load(f)
            
        with open(file_path, 'w', encoding='utf-8') as f: json.dump(custom_backup, f, indent=4)
        messagebox.showinfo("OK", "Настройки сохранены!")

    def load_custom(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not file_path: return
        with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
        
        if self.f_vanilla and "vanilla" in data: self._update_txt(self.f_vanilla, data["vanilla"])
        if self.f_optifine and "optifine" in data: self._update_txt(self.f_optifine, data["optifine"])
        
        def deep_merge(source, updates):
            for k, v in updates.items():
                if isinstance(v, dict) and k in source and isinstance(source[k], dict): deep_merge(source[k], v)
                else: source[k] = v
            return source

        if self.f_sodium and "sodium" in data:
            with open(self.f_sodium, 'r', encoding='utf-8') as f: s_json = json.load(f)
            with open(self.f_sodium, 'w', encoding='utf-8') as f: json.dump(deep_merge(s_json, data["sodium"]), f, indent=4)
            
        if self.f_extra and "extra" in data:
            with open(self.f_extra, 'r', encoding='utf-8') as f: e_json = json.load(f)
            with open(self.f_extra, 'w', encoding='utf-8') as f: json.dump(deep_merge(e_json, data["extra"]), f, indent=4)

        messagebox.showinfo("OK", "Настройки загружены!")

    # ================= ВИЗУАЛ =================
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode; self.apply_theme(); self.save_app_settings()

    def apply_theme(self):
        bg, fg, card, acc = ("#121212", "#ffffff", "#1e1e1e", "#00a8ff") if self.dark_mode else ("#f5f6fa", "#2f3640", "#ffffff", "#0097e6")
        self.root.config(bg=bg); self.main_frame.config(bg=bg); self.lbl_title.config(bg=bg, fg=acc)
        self.ent_path.config(bg=card, fg=fg, insertbackground=fg)
        self.txt_status.config(bg=card, fg="#4cd137" if self.dark_mode else "#44bd32")
        
        self.btn_min.config(bg="#e84118", fg="white")
        self.btn_mid.config(bg="#e1b12c", fg="white")
        self.btn_max.config(bg="#4cd137", fg="white")
        
        self.btn_save.config(bg="#8c7ae6", fg="white")
        self.btn_load.config(bg="#00a8ff", fg="white")

        for w in self.main_frame.winfo_children():
            if isinstance(w, tk.Label) and w != self.lbl_title: w.config(bg=bg, fg=fg)

    def save_app_settings(self):
        with open("app_settings.json", 'w', encoding='utf-8') as f:
            json.dump({"mc_dir": self.instances_path, "dark_mode": self.dark_mode}, f, indent=4)

if __name__ == "__main__":
    hide_console()
    p, dm = "", True
    if os.path.exists("app_settings.json"):
        try:
            with open("app_settings.json", 'r', encoding='utf-8') as f:
                d = json.load(f); p, dm = d.get("mc_dir", ""), d.get("dark_mode", True)
        except: pass
    root = tk.Tk(); ttk.Style().theme_use('clam'); app = ViconryAbsoluteEngine(root, p, dm); root.mainloop()

import os
import subprocess
import psutil
import json
import time
import logging as logger

def bytes_to_unit(n):
    """Convert bytes to value and unit string."""
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    step = 1024.0
    i = 0
    while n >= step and i < len(symbols) - 1:
        n /= step
        i += 1
    return round(n, 2), symbols[i]

def get_temp():
    try:
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return float(out.strip().split('=')[1].replace("'C", ''))
    except:
        return None

def get_throttle_status():
    try:
        out = subprocess.check_output(["vcgencmd", "get_throttled"]).decode()
        return out.strip().split('=')[1]
    except:
        return None

def get_load_avg():
    load1, load5, load15 = os.getloadavg()
    cores = psutil.cpu_count(logical=True) or 1
    return {
        "1min": round(load1, 2),
        "5min": round(load5, 2),
        "15min": round(load15, 2),
        "cores": cores,
        "load_pct_1min": round((load1 / cores) * 100, 1),
        "load_pct_5min": round((load5 / cores) * 100, 1),
        "load_pct_15min": round((load15 / cores) * 100, 1),
    }

def get_memory():
    mem = psutil.virtual_memory()
    total_gb = round(mem.total / 1024**3, 2)
    used_gb = round(mem.used / 1024**3, 2)
    return {
        "used_GB": used_gb,
        "total_GB": total_gb,
        "used_percent": round(mem.percent, 1)
    }

def get_disk():
    disk = psutil.disk_usage('/')
    total, total_unit = bytes_to_unit(disk.total)
    used, used_unit = bytes_to_unit(disk.used)
    free, free_unit = bytes_to_unit(disk.free)

    return {
        f"total_{total_unit}": total,
        f"used_{used_unit}": used,
        f"free_{free_unit}": free,
        "percent": disk.percent
    }

def get_process_info():
    zombies = [p.info for p in psutil.process_iter(['pid', 'status']) if p.info['status'] == psutil.STATUS_ZOMBIE]
    return {
        "total_processes": len(psutil.pids()),
        "zombie_count": len(zombies)
    }

def get_top_processes(n=5):
    procs = []
    for p in psutil.process_iter(['pid', 'cpu_percent', 'memory_percent', 'cmdline']):
        try:
            procs.append({
                "pid": p.info['pid'],
                "cpu": p.info['cpu_percent'],
                "mem_percent": round(p.info['memory_percent'], 2),
                "cmd": " ".join(p.info['cmdline']) if p.info['cmdline'] else ''
            })
        except:
            continue
    return sorted(procs, key=lambda x: x['cpu'], reverse=True)[:n]

def get_uptime_seconds():
    return round(time.time() - psutil.boot_time())

def get_all_metrics():
    result = {
        "cpu_load": get_load_avg(),
        "cpu_temp_c": get_temp(),
        "cpu_throttle_flags": get_throttle_status(),
        "memory": get_memory(),
        "disk": get_disk(),
        "processes": get_process_info(),
        "top_processes": get_top_processes(),
        "uptime_days": get_uptime_seconds() // (24 * 60 * 60)
    }
    logger.info(result)
    return result

# if __name__ == "__main__":
#     print(json.dumps(get_all_metrics(), indent=2))

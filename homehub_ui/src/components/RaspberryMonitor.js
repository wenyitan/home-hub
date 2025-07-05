import { useState, useEffect, useRef } from 'react';
import axios from "axios";

function RaspberryMonitor() {

    const [result, setResult] = useState(null);
    const [polling, setPolling] = useState(false);
    const intervalId = useRef(null);

    const fetchRaspberryMonitoring = () => {
        axios.get("http://raspberrypi.local:5001/api/v1/home-hub/raspberrypi/status")
            .then((res) => {
                setResult(res.data);
            })
            .catch((err) => {
                setResult("err");
            })
    }

    useEffect(() => {
        fetchRaspberryMonitoring();
        if (polling) {
            intervalId.current = setInterval(fetchRaspberryMonitoring, 5000);
        } else {
            if (intervalId.current) {
                clearInterval(intervalId.current);
            }
        }
        // Cleanup on unmount
        return () => clearInterval(intervalId.current);
    }, [polling]);

    return (
        <>
            <h3>Raspberry Pi Monitor</h3>
            <div className="polling-indicator" onClick={() => setPolling(!polling)} title={polling ? "Click to stop polling" : "Click to start polling"}>
                <span className={`indicator-light ${polling ? 'on' : 'off'}`}></span>
                <span className="indicator-label">{polling ? 'Polling' : 'Stopped'}</span>
            </div>
            {result !== null && <div className="rpi-widgets-grid">
                {/* CPU */}
                <div className="rpi-widget">
                    <h1>CPU</h1>
                    <h5>Cores: <span className="value">{result.cpu_load.cores}</span></h5>
                    <h5>1min Load: <span className="value">{result.cpu_load.load_pct_1min}%</span></h5>
                    <h5>5min Load: <span className="value">{result.cpu_load.load_pct_5min}%</span></h5>
                    <h5>15min Load: <span className="value">{result.cpu_load.load_pct_15min}%</span></h5>
                    <h5>Temp: <span className="value">{result.cpu_temp_c}{`\u00B0C`}</span></h5>
                </div>

                {/* Memory */}
                <div className="rpi-widget">
                    <h1>Memory</h1>
                    <h5>Total: <span className="value">{result.memory.total_GB} GB</span></h5>
                    <h5>Used: <span className="value">{result.memory.used_GB} GB</span></h5>
                    <h5>Used %: <span className="value">{result.memory.used_percent}%</span></h5>
                </div>

                {/* Disk */}
                <div className="rpi-widget">
                    <h1>Disk</h1>
                    <h5>Total: <span className="value">{result.disk.total_GB} GB</span></h5>
                    <h5>Free: <span className="value">{result.disk.free_GB} GB</span></h5>
                    <h5>Used: <span className="value">{result.disk.percent}%</span></h5>
                </div>

                {/* Uptime */}
                <div className="rpi-widget">
                    <h1>Uptime</h1>
                    <h5>Device Up Time: <span className="value">{result.uptime_days} days</span></h5>
                    {/* <button className="outlined" onClick={fetchRaspberryMonitoring}>Refresh</button> */}
                </div>
            </div>}
        </>
    )
};

export default RaspberryMonitor;
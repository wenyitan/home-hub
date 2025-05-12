import { useState, useEffect } from 'react';
import axios from "axios";

function RoomClimateMonitor() {

    const [ humidity, setHumidity ] = useState(0);
    const [ temperature, setTemperature ] = useState(0)

    const fetchTemperatureAndHumidity = () => {
        axios.get("http://raspberrypi.local:5001/api/v1/home-hub/dht11-reading")
        .then((res)=> {
            setHumidity(res.data.humidity);
            setTemperature(res.data.temperature);
        })
        .catch((err)=> {
            setHumidity("err");
            setTemperature("err");
        })
    }

    useEffect(()=> {
        fetchTemperatureAndHumidity();
    }, [])

    return (
        <>
            <h3>Room Monitor</h3>
            <div className='widget'>
                <h5>Humidity: <span className="value">{humidity}%</span></h5>
                <h5>Temperature: <span className="value">{temperature}{'\u00B0'}C</span></h5>
                <button className='outlined' onClick={fetchTemperatureAndHumidity}>Refresh</button>
            </div>
        
        </>
    )
};

export default RoomClimateMonitor;
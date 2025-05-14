import { useState, useEffect } from 'react';
import axios from "axios";


function HumidifierControl() {

    const [ power, setPower ] = useState("Off");
    const [ mode, setMode ] = useState(0);

    const fetchHumidifierStatus = () => {
        axios.get("http://raspberrypi.local:5001/api/v1/home-hub/humidifier/status")
        .then((res)=> {
            setPower(res.data.power ? "On": "Off");
            setMode(res.data.mode);
        })
        .catch((err)=> {
            setPower("err");
            setMode("err");
        })
    }

    useEffect(()=> {
        fetchHumidifierStatus();
    }, [])

    const handlePowerClick = (event) => {
        const choice = event.target.value.toLowerCase() == "off" ? "on" : "off"
        axios.get(`http://raspberrypi.local:5001/api/v1/home-hub/humidifier/${choice}`)
        .then((res)=> {
        })
        .catch((err)=> {
            console.log(err);
        }).finally(()=> {
            fetchHumidifierStatus();
        })
    }

    const handleModeClick = (event) => {
        axios.get(`http://raspberrypi.local:5001/api/v1/home-hub/humidifier/toggle-mode`)
        .then((res)=> {
        })
        .catch((err)=> {
            console.log(err);
        }).finally(()=> {
            fetchHumidifierStatus();
        })
    }

    return (
        <>
            <h3>Humidifier Control</h3>
            <div className="widget">
                <h5>Power: <button className='no-outline' value={power} onClick={handlePowerClick}>{power}</button></h5>
                <h5>Mode: <button className='no-outline' value={power} onClick={handleModeClick}>{mode}</button></h5>
                <button className='outlined' onClick={fetchHumidifierStatus}>Refresh</button>
                
            </div>
        </>
    )
};

export default HumidifierControl;
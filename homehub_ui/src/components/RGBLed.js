import { useState, useEffect } from 'react';
import axios from "axios";

function RGBLed() {
    const [ red, setRed ] = useState(0);
    const [ green, setGreen ] = useState(0);
    const [ blue, setBlue ] = useState(0);

    const setColor = () => {
        const colorBox = document.getElementById("color-box");
        axios.get("http://raspberrypi.local:5001/api/v1/home-hub/rgbled", {
            params: {
                red: red/256,
                green: green/256,
                blue: blue/256
            }
        }).then((res)=> {
            const data = res.data;
            colorBox.style.backgroundColor = `rgb(${data["red"]*256}, ${data["green"]*256}, ${data["blue"]*256})`;
        }).catch((err)=> {
            colorBox.style.backgroundColor = `rgb(0,0,0)`;
            console.log(err);
        })
    }

    useEffect(()=> {
        const handler = setTimeout(()=> {
            setColor();
        }, 500);

        return () => {
            clearTimeout(handler);
        }
    }, [red, green, blue]);

    return (
        <>
            <h3>RGB Selector</h3>
            <div id='color-box' className='color-box'></div>
            <div className='flex-col'>
                Red<input type='range' className="red" value={red} onChange={(e)=>setRed(e.target.value)} min="0" max="256"/>
                Blue<input type='range' className="blue" value={blue} onChange={(e)=>setBlue(e.target.value)} min="0" max="256"/>
                Green<input type='range' className="green" value={green} onChange={(e)=>setGreen(e.target.value)} min="0" max="256"/>
            </div>
            <div className='flex-row'>
            <button onClick={(e) => {
                setBlue(0);
                setGreen(0);
                setRed(0)
            }}>Off</button>
            <button className='outlined' onClick={(e) => {
                setBlue(256);
                setGreen(256);
                setRed(256)
            }}>White</button>
            </div>
        </>
    )
};

export default RGBLed;
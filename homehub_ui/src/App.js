import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from 'react';
import axios from "axios";

function App() {

  const [ red, setRed ] = useState(0);
  const [ green, setGreen ] = useState(0);
  const [ blue, setBlue ] = useState(0);

  const setColor = () => {
    axios.get("http://raspberrypi.local:5001/api/v1/home-hub/rgbled", {
      params: {
        red: red/256,
        green: green/256,
        blue: blue/256
      }
    })
  }

  useEffect(()=> {
    setColor();
  }, [red, green, blue]);

  return (
    <div className="App">
      <header className="App-header">
        Home Hub
      </header>
      <div className='App-body'>
        <div>How to use:<br/>
          To use on phone, access http://192.168.18.52:3000
        </div>
        <div className='color-box'></div>
        <div className='flex-col'>
          Red<input type='range' value={red} onChange={(e)=>setRed(e.target.value)} min="0" max="256"/>
          Blue<input type='range' value={blue} onChange={(e)=>setBlue(e.target.value)} min="0" max="256"/>
          Green<input type='range' value={green} onChange={(e)=>setGreen(e.target.value)} min="0" max="256"/>
        </div>
        <div className='flex-row'>
          <button onClick={(e) => {
            setBlue(0);
            setGreen(0);
            setRed(0)
          }}>Off</button>
          <button onClick={(e) => {
            setBlue(256);
            setGreen(256);
            setRed(256)
          }}>White</button>
        </div>
      </div>
    </div>
  );
}

export default App;

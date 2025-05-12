import './App.css';
import RGBLed from './components/RGBLed';
import RoomClimateMonitor from './components/RoomClimateMonitor';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Wen Tian Home Hub</h1>
        <p className="subtext">Control Center</p>
      </header>
      <main className="App-body">
        <section className="instructions">
          <p><strong>How to use:</strong><br />To use on phone, access <code>http://192.168.18.52:3000</code></p>
        </section>
        <RoomClimateMonitor />
        <RGBLed />
      </main>
    </div>
  );
}

export default App;

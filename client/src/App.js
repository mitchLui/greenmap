import './App.css';
import {Navbar} from "./Components/Navbar/Navbar";
import {Mapbox} from "./Components/Map/Mapbox";
import {Weather} from "./Components/Weather/Weather";

function App() {
  return (
    <div className="App">
      <Navbar />
        <Weather />
        <Mapbox />
    </div>
  );
}

export default App;

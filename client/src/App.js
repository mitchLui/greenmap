import logo from './logo.svg';
import './App.css';
import {Navbar} from "./Components/Navbar/Navbar";
import {Mapbox} from "./Components/Map/Mapbox";

function App() {
  return (
    <div className="App">
      <Navbar />
        <Mapbox />
    </div>
  );
}

export default App;

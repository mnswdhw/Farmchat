import logo from './logo.svg';
import './App.css';
import './components/mainchatbox/Mainchatbox'
import Mainchatbox from './components/mainchatbox/Mainchatbox';
import {Routes, Route, Navigate} from 'react-router-dom'
function App() {
  return (
    <div className="App">
      <Mainchatbox />
    </div>
  );
}

export default App;

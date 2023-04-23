import './App.css';
import Slides from './components/Slides';
import Upload from './components/Upload';
import React from 'react';
import { BotProvider } from './contexts/BotContext';

function App() {
  return <BotProvider><Upload /></BotProvider>;
}

export default App;

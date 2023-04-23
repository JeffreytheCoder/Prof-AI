import './App.css';
import Slides from './components/Slides';
import Upload from './components/Upload';
import React from 'react';
import { BotProvider } from './contexts/BotContext';
import ButtonAppBar from "./components/Navbar"
import {AppBar, Container, IconButton, Box, Paper, Grid} from "@mui/material";
import { useRoutes } from 'react-router-dom';
import routes from './routes';

function App() {
  const content = useRoutes(routes);
  console.log(content)

  return (
      <BotProvider>
              <ButtonAppBar />
              {content}
      </BotProvider>

  );
}

export default App;

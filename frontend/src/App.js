import './App.css';
import Slides from './components/Slides';
import Upload from './components/Upload';
import React from 'react';
import { BotProvider } from './contexts/BotContext';
import ButtonAppBar from "./components/Navbar"
import {AppBar, Container, IconButton, Box, Paper, Grid} from "@mui/material";

function App() {
  return (
      <BotProvider>
          <div>
              <ButtonAppBar></ButtonAppBar>
          </div>
          <div>
              <Upload />
          </div>
          <Container>
          </Container>
      </BotProvider>

  );
}

export default App;

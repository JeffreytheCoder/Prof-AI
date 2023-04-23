import './App.css';
import Slides from './components/Slides';
import ButtonAppBar from "./components/Navbar"
import React from 'react';
import {AppBar, Container, IconButton, Box, Paper, Grid} from "@mui/material";

function App() {
  return (
      <div>
          <div>
              <ButtonAppBar></ButtonAppBar>
          </div>
          <div>
              <Slides />
          </div>
          <Container>
          </Container>
      </div>

  );
}

export default App;

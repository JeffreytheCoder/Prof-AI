import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import {Icon} from "@mui/material";
import logo from '../logo.png'
export default function ButtonAppBar() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar color="inherit" elevation={0} position="sticky">
                <Toolbar>
                    <img src={logo} style={{ width: "15%", height: "15%" }} alt="My Icon" />
                </Toolbar>
            </AppBar>
        </Box>
    );
}
import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Face6RoundedIcon from '@mui/icons-material/Face6Rounded';
import logo from '../logo.png'
export default function ButtonAppBar() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar color="inherit" elevation={0} position="sticky">
                <Toolbar>
                    <img src={logo} style={{ width: "15%", height: "15%" }} alt="My Icon" />
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}/>
                    <IconButton color="inherit" size='large'>
                        <Face6RoundedIcon fontSize="large" style={{color:"#5F64FA"}}/>
                    </IconButton>
                </Toolbar>
            </AppBar>
        </Box>
    );
}
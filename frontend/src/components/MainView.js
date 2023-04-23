import React from 'react';
import {Container,Grid} from '@mui/material';
import Slides from "./Slides";

function MainView() {
    return (
        <Container maxWidth="xl">
            <Grid container spacing={0}>
                <Grid item xs={8}>
                    <div>
                        <Slides />
                    </div>
                </Grid>
                <Grid item xs={4}>
                    <div>Second Container</div>
                </Grid>
            </Grid>
        </Container>
    );
}

export default MainView;
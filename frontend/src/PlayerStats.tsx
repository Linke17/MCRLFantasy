import * as React from 'react';
import Box from '@mui/material/Box';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', width: 130 },
    { field: 'shots', headerName: 'Shots', type: 'number', width: 130 },
    { field: 'goals', headerName: 'Goals', type: 'number', width: 130 },
    { field: 'assists', headerName: 'Assists', type: 'number', width: 130 },
    { field: 'saves', headerName: 'Saves', type: 'number', width: 130 },
    { field: 'game_score', headerName: 'Score', type: 'number', width: 130 },
    { field: 'fantasy_score', headerName: 'Fantasy', type: 'number', width: 130 },
];

export default function DataGridDemo() {

    const [rows, setRows] = React.useState([]);

    React.useEffect(() => {
        fetch('http://localhost:5000/api/players_average')
            .then(response => response.json())
            .then(data => setRows(data['player_stats']));
    }, []);

    const paginationModel = { page: 0, pageSize: 5 };

    return (
        <Box sx={{ width: '90%' }}>
            <DataGrid
                rows={rows}
                columns={columns}
                initialState={{ pagination: { paginationModel } }}
                pageSizeOptions={[5, 10]}
                sx={{ border: 0 }}
                autoHeight {...rows}
                disableColumnResize={true}
                disableColumnMenu
            />
        </Box>
    );
}
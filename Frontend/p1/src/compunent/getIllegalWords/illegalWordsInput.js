import React, {useState} from 'react';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Box from "@mui/material/Box";

export default function InputChips() {
    const [inputValue, setInputValue] = useState('');
    const [chips, setChips] = useState([]);

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleInputKeyDown = (event) => {
        if (event.key === 'Enter' || event.key === ',') {
            event.preventDefault();

            const value = inputValue.trim();

            if (value) {
                setChips([...chips, {label: value}]);
            }

            setInputValue('');
        }
    };

    const handleChipDelete = (chipToDelete) => () => {
        setChips((chips) => chips.filter((chip) => chip !== chipToDelete));
    };

    return (
        <section dir='rtl'>
            <Box sx={{display: "flex",direction:"rtl", alignItems: "center", justifyContent: "center", flexDirection:"column"}}>
                <TextField
                    sx={{
                        direction:"rtl",
                        border: "none",
                        boxShadow: "3px 3px 4px #919191",
                        borderRadius:"8px",
                        width:"70vw",
                        marginBottom:"60px",
                        marginTop:"20px"
                    }}
                    label="کلمات غیرقانونی مد نظر را با ویرگول جداسازی کنید"
                    value={inputValue}
                    onChange={handleInputChange}
                    onKeyDown={handleInputKeyDown}
                    InputLabelProps={{
                        sx: {
                            direction:"rtl",  textAlign: 'center'
                        }
                    }}
                />

                <Stack direction="row" spacing={2} sx={{ marginBottom:"50px" }} >
                    {chips.map((chip, index) => (
                        <Chip
                            key={index}
                            label={chip.label}
                            onDelete={handleChipDelete(chip)}
                        />
                    ))}
                </Stack>
            </Box>
        </section>
    );
}

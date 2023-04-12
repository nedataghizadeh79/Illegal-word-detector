//this component is for handel chips, when you write sth in inputs, your words convert to chip.

import React, {useEffect, useState} from 'react';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Box from "@mui/material/Box";

export default function InputChips({setSaveIllegals}) {
    // we define useState for saving our data
    const [inputValue, setInputValue] = useState('');
    const [allInputValue, setAllInputValue] = useState([]);
    const [chips, setChips] = useState([]);

    //when we change our input this function save the changes and new inputs.



    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };


    //when we write sth in our input, then we press Enter key, this function will call.
    const handleInputKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const value = inputValue.trim();
            setAllInputValue([...allInputValue, value]);
            if (value) {
                const newChips = value.split(',').map((val) => ({ label: val.trim() }));
                setChips([...chips, ...newChips]);
            }
            setSaveIllegals(allInputValue)
            setInputValue('');
        }
    };

    // when you delete chips, also it's values should delete from our list.
    const handleChipDelete = (chipToDelete) => () => {
        const chipIndex = allInputValue.findIndex((chip) => chip === chipToDelete);
        const newChips = [...allInputValue];
        newChips.splice(chipIndex, 1);
        setAllInputValue(newChips);
        const updatedChips = chips.filter((chip) => chip !== chipToDelete);
        setChips(updatedChips);
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
                    label="کلمات غیرقانونی را یکی یکی وارد نمایید"
                    value={inputValue}
                    onChange={handleInputChange}
                    onKeyDown={handleInputKeyDown}
                    InputLabelProps={{
                        sx: {
                            direction:"rtl",  textAlign: 'center' , padding:"5px"
                        }
                    }}
                />

                <Stack direction="row" spacing={2} sx={{ marginBottom:"50px" }} >
                    {chips.map((chip, index) => (
                        <Chip
                            key={index}
                            label={chip.label}
                            // when you press x icon on chips, it will delete
                            onDelete={handleChipDelete(chip)}
                        />
                    ))}
                </Stack>
            </Box>
        </section>
    );
}

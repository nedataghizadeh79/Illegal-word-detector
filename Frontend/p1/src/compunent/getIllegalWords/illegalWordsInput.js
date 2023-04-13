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

    useEffect(() => {
        const timer = setTimeout(() => {
        }, 300)
    }, [allInputValue] )


    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };


    //when we write sth in our input, then we press Enter key, this function will call.
    const handleInputKeyDown = (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            const value = inputValue.trim();
            setAllInputValue([...allInputValue, value]);

            // if we have value we can put their values in our chips
            if (value) {
                const newChips = value.split(",").map((val) => ({ label: val.trim() }));
                setChips([...chips, ...newChips]);
            }
            setSaveIllegals((pre) => [...pre, value]);
            setInputValue("");
        }
    };

    // if we delete chips, we should delete its value from allInputValue list
    const handleChipDelete = (chipToDelete) => () => {
        const filteredChips = chips.filter((chip) => chip !== chipToDelete);
        setChips(filteredChips);
        const filteredSaveIllegals = allInputValue.filter((val) => val !== chipToDelete.label);
        setSaveIllegals(filteredSaveIllegals);
        setAllInputValue(filteredSaveIllegals);
    };

    // now we have an input that we can give the illegals word from the input and convert them to chips and save them in list
    return (
        <section dir='rtl'>
            <Box sx={{display: "flex",direction:"rtl", alignItems: "center", justifyContent: "center", flexDirection:"column"}}>
                <TextField
                    // in mui we can add css by sx
                    sx={{
                        direction:"rtl",
                        border: "none",
                        boxShadow: "3px 3px 4px #919191",
                        borderRadius:"8px",
                        width:"70vw",
                        marginBottom:"60px",
                        marginTop:"20px"
                    }}
                    label="کلمات غیرمجاز را یکی یکی وارد کرده و پس از هر کلمه کلید Enter را فشار دهید."
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
                            // when you press X icon on chips, it will delete.
                            onDelete={handleChipDelete(chip)}
                        />
                    ))}
                </Stack>
            </Box>
        </section>
    );
}

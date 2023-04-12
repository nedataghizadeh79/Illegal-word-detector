//we want to have 2 tabs for our 2 main parts in our project, so one of them is for correcting texts that contain illegal words and the second tab is for correcting pdf

import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Main from "../../Pages/mainPage/Main";
import UploadPDF from "../pdfReader/pfdUploader";

function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </div>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
};

function a11yProps(index) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

export default function BasicTabs({saveIllegals}) {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    // we want 2 tabs, so we call TabPanel 2 times and use our components in them.
    return (
        <Box sx={{ width: '100%', direction:'rtl' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' ,display:"flex" , alignItems:"center" , justifyContent:"center" }}>
                <Tabs sx={{ display:"flex" , alignItems:"center" , justifyContent:"center" }} value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab sx={{ color:"#2B468B", fontWeight:"bold" , fontSize:"16px" }} label="ورودی متن" {...a11yProps(0)} />
                    <Tab  sx={{ color:"#2B468B", fontWeight:"bold" , fontSize:"16px" }} label="ورودی PDF" {...a11yProps(1)} />
                </Tabs>
            </Box>
            <TabPanel value={value} index={0}>
                <Main saveIllegals={saveIllegals} />
            </TabPanel>
            <TabPanel value={value} index={1}>
                <UploadPDF saveIllegals={saveIllegals}/>
            </TabPanel>
        </Box>
    );
}
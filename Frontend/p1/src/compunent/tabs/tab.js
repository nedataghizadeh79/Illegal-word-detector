import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Navbar from "../navbar/navbar";
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

export default function BasicTabs() {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <Box sx={{ width: '100%', direction:'rtl' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' ,display:"flex" , alignItems:"center" , justifyContent:"center" }}>
                <Tabs sx={{ display:"flex" , alignItems:"center" , justifyContent:"center" }} value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab sx={{ color:"#2B468B", fontWeight:"bold" , fontSize:"16px" }} label="ورودی متن" {...a11yProps(0)} />
                    <Tab  sx={{ color:"#2B468B", fontWeight:"bold" , fontSize:"16px" }} label="ورودی PDF" {...a11yProps(1)} />
                </Tabs>
            </Box>
            <TabPanel value={value} index={0}>
                <Main/>
            </TabPanel>
            <TabPanel value={value} index={1}>
                <UploadPDF/>
            </TabPanel>
        </Box>
    );
}
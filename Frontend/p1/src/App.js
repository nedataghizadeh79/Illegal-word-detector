import './App.css';
import WelcomePage from "./Pages/welcomePage/WelcomePage";
import {createTheme, ThemeProvider} from "@mui/material/styles";

const theme = createTheme({
    typography: {
        fontFamily: 'Vazirmatn',
    },
    direction: 'rtl',
})

function App() {
    return (
        <ThemeProvider theme={theme}>
            <div className="App">
                <WelcomePage/>
            </div>
        </ThemeProvider>
    );
}

export default App;

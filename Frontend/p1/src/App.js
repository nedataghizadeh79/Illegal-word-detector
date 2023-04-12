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
                // welcome page contain Main page, after 2 seconds you will see main page and you can do your job.
                <WelcomePage/>
            </div>
        </ThemeProvider>
    );
}

export default App;

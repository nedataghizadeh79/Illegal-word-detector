import './WelcomePage.css' ;
import {useEffect, useState} from "react";
import Main from "../mainPage/Main";


const WelcomePage = () => {
    const [display, setDisplay] = useState(true)

    useEffect(() => {
        const timer = setTimeout(() => {
            setDisplay(false)
        }, 10)
    }, [])

    return (
        <div>
            {
                display ? <section className='welcomePage'>
                </section> : <Main/>
            }
        </div>
    )
}

export default WelcomePage
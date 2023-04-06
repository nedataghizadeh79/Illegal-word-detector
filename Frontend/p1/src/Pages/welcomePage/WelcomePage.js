import './WelcomePage.css' ;
import {useEffect, useState} from "react";
import Navbar from "../../compunent/navbar/navbar";
import TabPanel from '../../compunent/tabs/tab'
import IllegalWordsInput from "../../compunent/getIllegalWords/illegalWordsInput";

const WelcomePage = () => {
    const [display, setDisplay] = useState(true)
    const [saveIllegals , setSaveIllegals ] = useState([])

    useEffect(() => {
        const timer = setTimeout(() => {
            setDisplay(false)
        }, 10)
    }, [])

    return (
        <div>
            {
                display ? <section className='welcomePage'>
                    </section> :
                    <div className='divContainer'>
                        <Navbar/>
                        <IllegalWordsInput setSaveIllegals ={setSaveIllegals}/>
                        <TabPanel saveIllegals={saveIllegals}/>
                    </div>
            }
        </div>
    )
}

export default WelcomePage
// when you come to our website for 2 seconds you can see a welcome page and then, you can see the main page.
import './WelcomePage.css' ;
import {useEffect, useState} from "react";
import Navbar from "../../compunent/navbar/navbar";
import TabPanel from '../../compunent/tabs/tab'
import IllegalWordsInput from "../../compunent/getIllegalWords/illegalWordsInput";

const WelcomePage = () => {
    // at first the display variable is true, it means you can see welcome page,
    // after 2 seconds it will be false then you will see main page.
    const [display, setDisplay] = useState(true)
    const [saveIllegals , setSaveIllegals ] = useState([])

    //after 2 seconds we make it false by useEffect
    useEffect(() => {
        const timer = setTimeout(() => {
            setDisplay(false)
        }, 2000)
    }, [])

    return (
        <div>
            {
                display ? <section className='welcomePage'>
                    </section> :
                    <div className='divContainer'>
                        {/*/now we call our components*/}
                        <Navbar/>
                        <IllegalWordsInput setSaveIllegals ={setSaveIllegals}/>
                        <TabPanel saveIllegals={saveIllegals}/>
                    </div>
            }
        </div>
    )
}


export default WelcomePage
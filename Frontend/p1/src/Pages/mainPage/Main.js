import './Main.css'
import {useState} from "react";
import mainPagePic from '../../assets/pictures/mainPic.jpg'
const Main = () => {
    const [inputText , setInputText ]=useState('')

    const inputHandler=()=>{
        //send request and data
    }

    return (
        <div className='main'>

            <section dir='ltr'  className='leftPart'>
                <img className='mainPic' src={mainPagePic} alt={'main page pic'}  />
            </section>

                 <section dir='rtl'  className='inputs'>
                    <input className='inputElement'  value={inputText} onChange={inputHandler} />
                    <button className='searcButton'> searc </button>
                </section>

        </div>
    )
}

export default Main
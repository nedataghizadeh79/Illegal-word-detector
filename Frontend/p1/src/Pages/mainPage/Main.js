import './Main.css'
import {useState} from "react";

const Main = () => {
    const [textArea, setTextArea] = useState('')

    const textAreaHandler = (event) => {
        setTextArea(event.target.value)
    }

    return (
        <div className='main'>
            <section className='textareaSection'>
                <label className='textLabel'>در این قسمت متن خود را به فارسی وارد نمایید</label>
                <textarea className='ta' onChange={textAreaHandler} value={textArea}/>
                <button className='submitBtn'>پردازش</button>
            </section>
        </div>
    )
}

export default Main
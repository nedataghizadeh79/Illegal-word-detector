import './Main.css'
import {useState} from "react";
import mainPagePic from '../../assets/pictures/mainPic.jpg'

const Main = () => {
    const [firstInput , setFirstInput] = useState('')
    const [illegalText , setIllegalText ]=useState([])
    const [textArea , setTextArea] = useState('')

    const handleIllegalWords = (event) => {
        setFirstInput(event.target.value)
        setIllegalText(firstInput.split(" "));
    }

    const textAreaHandler=(event)=>{
        setTextArea(event.target.value)
    }


    return (
        <div className='main'>
            <div className='cotainer'>
                <section className='firstPart'>
                    <img src={mainPagePic} alt='firs pic' className='pic' />
                    <p className='pRightSide' dir='rtl'>
                        ما در این پروژه قصد داریم که با کمک کلمات غیر قانونی که وارد میکنید؛ بتوانیم کلمات غیرقابل قبول را استخراج نماییم.
                        <br/>
                        یکی از چالش های NLP این است که بتوانیم کلماتی که مطلبو نیستند را شناسایی کنیم برای مثال میتوانیم کلماتی که محدودیتی برای استفاده دارند را شناسایی کنیم و سپس در متون به دنبال آنها بگردیم و محدودیت لازم را اجرا کنیم
                    </p>
                </section>
            </div>



            <section className='secondPart'  dir='rtl' >
                <div className='labelInput' >
                    <label className='illegalWords'>کلمات غیر قانونی را وارد کنید</label>
                    <input className='illegalInput' value={firstInput} onChange={handleIllegalWords} />
                </div>
                <p className='explanation'> لطفا کلمات تان را با اسپیس وارد کنید </p>
            </section>


            <section className='textareaSection'>
                <label className='textLabel' >در این قسمت متن خود را به فارسی وارد نمایید</label>
                <textarea className='ta' onChange={textAreaHandler} value={textArea} />
                <button className='submitBtn'>پردازش</button>
            </section>



        </div>
    )
}

export default Main
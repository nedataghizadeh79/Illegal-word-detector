//in this component we have just a section that it contains a picture with a paragraph

import mainPagePic from "../../assets/pictures/mainPic.png";
import './navbar.css'

const Navbar=()=>{
    return(
        <div className='cotainer'>
            {/* in this section we just show img and paragraph */}
            <section className='firstPart'>
                <img src={mainPagePic} alt='firs pic' className='pic'/>
                <p className='pRightSide' dir='rtl'>
                    ما در این پروژه قصد داریم که با کمک کلمات غیر قانونی که وارد میکنید؛ بتوانیم کلمات غیرقابل قبول
                    را استخراج نماییم.
                    <br/>
                    یکی از چالش های NLP این است که بتوانیم کلمه هایی که در متون مطلوب  نیستند را شناسایی کنیم، برای مثال میتوانیم
                        کلماتی که محدودیتی برای استفاده دارند را پیدا کنیم، سپس به دنبال شان بگردیم و
                    محدودیت لازم را اجرا کنیم.
                </p>
            </section>
        </div>
    )
}

export default Navbar

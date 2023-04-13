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
                    هدف این پروژه، تشخیص کلمات غیرمجازی است که در متن با روش‌های مختلف جهت دور زدن فیلترها آمده است.
                    <br/>
                    یکی از چالش‌های موجود در حوزه پردازش زبان‌های طبیعی تفاوت ظاهر کلمات با کلمه مورد نظر از آن‌هاست. به عنوان مثال در برخی متون می‌خواهیم کلماتی که مطلوب و قانونی نیستند را به هر شکل و با هر تغییری که در متن آمده است شناسایی کنیم.
                </p>
            </section>
        </div>
    )
}

export default Navbar

import './Main.css'
import {useState} from "react";
import axios from "axios";

const Main = ({saveIllegals}) => {
    const [textArea, setTextArea] = useState('')
    const [mainInformation , setMainInformation] = useState({illegalWords:[] , text:""})
    // const [dataResponse , setDataResponse] = useState({})

    const processHandler =()=>{
        setMainInformation(prevState => ({...prevState, text: textArea}));
        setMainInformation(pre=>({...pre , illegalWords:saveIllegals}))
        axios.post('https://fe62-94-184-132-26.eu.ngrok.io/run', {
            illegal_words: mainInformation.illegalWords,
            text:mainInformation.text
        }).then(function (response) {
                console.log(response);

            const spans = Object.values(response.illegals).flat();

            const result = mainInformation.text.split('').map((char, index) => {
                const inSpan = spans.some(span => index >= span[0] && index <= span[1]);
                return <span style={{color: inSpan ? 'red' : 'black'}}>{char}</span>;
            });

            return <div>{result}</div>;
            }).catch(function (error) {
                // console.log(error);
            });

        // axios.get('http://172.27.52.54:8000/run')
        //     .then(function (response) {
        //         // handle success
        //         console.log(response);
        //     })
        //     .catch(function (error) {
        //         // handle error
        //         console.log(error);
        //     })
        //     .finally(function () {
        //         // always executed
        //     });
    }

    const textAreaHandler = (event) => {
        setTextArea(event.target.value)
    }

    return (
        <div className='main'>
            <section className='textareaSection'>
                <label className='textLabel'>در این قسمت متن خود را به فارسی وارد نمایید</label>
                <textarea className='ta' onChange={textAreaHandler} value={textArea}/>
                <button onClick={processHandler} className='submitBtn'>پردازش</button>
            </section>
        </div>
    )
}

export default Main
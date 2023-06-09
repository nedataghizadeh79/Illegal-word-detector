//this is the main page, we call our components that we want to show them in our main page.

import './Main.css'
import {useState} from "react";
import axios from "axios";
import * as React from 'react';
import Tooltip from '@mui/material/Tooltip';
import {CircularProgress} from "@mui/material";
import Box from "@mui/material/Box";

const Main = ({saveIllegals}) => {
    const [textArea, setTextArea] = useState('')
    const [mainIllegalWords, setMainIllegalWords] = useState([])

    const [showColoredResult, setShowColoredResult] = useState("")
    const [processing, setProcessing] = useState(false)

    // after you click in the related button, this function will call, we post the input value for backend then we can get the result
    //we catch a json which it has illegal words in our text with their spans
    //then we try to make some list that the fist element is the beginning of the numerical range,
    // the second element is end of numerical range and the third element is the related illegal word
    //then with the help of these lists we try to show the special words in text, we make red illegals words
    // if you move your mouse over the red words, you can see which of the corresponding words is illegal.

    function detect_reds(response) {
        const illegalSpans = []
        for (const word in response.data.illegals) {
            for (const span of response.data.illegals[word]) {
                illegalSpans.push([...span, word])
            }
        }
        illegalSpans.sort((a, b) => a[0] - b[0])
        const result = [];
        let startIndex = 0;
        illegalSpans.forEach(span => {
            result.push(textArea.slice(startIndex, span[0]))
            console.log(span)
            startIndex = span[1];
            result.push(<Tooltip title={'[' + span[2] + '  (' + span[0] + ', ' + span[1]}>
                <span
                    style={{color: 'red'}}>{textArea.slice(span[0], span[1])}</span>
            </Tooltip>)
        })
        result.push(textArea.slice(startIndex))

        setShowColoredResult(result)
        setProcessing(false)
        return result
    }

    const processHandler = () => {
        setProcessing(true)
        // setMainInformation(prevState => ({...prevState, text: textArea}));
        // setMainInformation(pre => ({...pre, illegalWords: saveIllegals}))
        setMainIllegalWords(saveIllegals)
        axios.post('http://localhost:8081/run', {
            illegal_words: saveIllegals,
            text: textArea
        }).then(function (response) {
            return detect_reds(response);
        }).catch(function (error) {
            console.log(error);
        })
    }

    const textAreaHandler = (event) => {
        setTextArea(event.target.value)
    }
    console.log(showColoredResult)

    return (
        <div className='main'>
            <section className='textareaSection'>
                <label className='textLabel'>متن فارسی جهت تشخیص کلمات غیر مجاز را وارد نمایید:</label>
                <textarea className='ta' onChange={textAreaHandler} value={textArea}/>
                <button onClick={processHandler} className='submitBtn'>پردازش</button>
                <div className='showRedText'>
                    {processing ?
                        <Box sx={{display: 'flex', justifyContent: 'center'}}>
                            <CircularProgress size={100}/>
                        </Box>
                        : showColoredResult
                    }
                </div>
            </section>
        </div>
    )
}

export default Main

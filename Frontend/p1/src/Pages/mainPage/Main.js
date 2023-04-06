import './Main.css'
import {useState} from "react";
import axios from "axios";
import * as React from 'react';
import Tooltip from '@mui/material/Tooltip';


const Main = ({saveIllegals}) => {
    const [textArea, setTextArea] = useState('')
    const [mainInformation, setMainInformation] = useState({illegalWords: [], text: ""})
    const [showColoredResult , setShowColoredResult ] = useState("")

    const processHandler = () => {
        setMainInformation(prevState => ({...prevState, text: textArea}));
        setMainInformation(pre => ({...pre, illegalWords: saveIllegals}))
        // axios.post('https://714c-46-209-40-254.eu.ngrok.io/runmock', {
        //     illegal_words: mainInformation.illegalWords,
        //     text:mainInformation.text
        // }).then(function (response) {

        const response = {
            data: {
                "illegals": {
                    "neda": [
                        [0,15], [17, 18]
                    ],
                    "dada": [
                        [
                            19,
                            22
                        ]
                    ],
                    "nana": [
                        [
                            24,
                            28
                        ]
                    ]
                }
            }

        }


        console.log(response.data.illegals);
        const illegalSpans = []
        for (const word in response.data.illegals) {
            for (const span of response.data.illegals[word]) {
                illegalSpans.push([...span, word])
            }
        }
        console.log(illegalSpans);
        illegalSpans.sort((a, b) => a[0] - b[0])

        const result = [];
        let startIndex = 0;
        illegalSpans.forEach(span => {
            result.push(textArea.slice(startIndex, span[0]))
            startIndex = span[1];

            result.push(<Tooltip title={span[2]}>
                <span style={{color: 'red'}}>{textArea.slice(span[0], span[1])}</span>
            </Tooltip>)
        })
        result.push(textArea.slice(startIndex))
        console.log(result);
        setShowColoredResult(result)
        return result;

        // }).catch(function (error) {
        //     // console.log(error);
        // });

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
                <div className='showRedText'>
                    {showColoredResult}
                </div>
            </section>
        </div>
    )
}

export default Main
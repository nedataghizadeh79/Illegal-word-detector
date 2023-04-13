//in this component we want to get access for uploading pdf to our website.

import React, {useEffect, useState} from "react";
import './pdfUploader.css'
import axios from "axios";

function UploadPDF({saveIllegals}) {
    // we can save our data in these useStates
    const [file, setFile] = useState(null);
    const [pdfResponse , setPdfResponse] =useState([])

    // inside the function, it extracts the first file from the array of files uploaded using the e event object's target
    //  property which refers to the element that triggered the event (in this case, an input element with type="file").
    // the first file in the array is obtained using the index [0]
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    // we want to sure that saveIllegals is not empty and all data are up to date.
    useEffect(() => {
        const timer = setTimeout(() => {
            console.log(saveIllegals)
        }, 300)
    }, saveIllegals)


    // in this function we want handel send request to backend and also accept just pdf format .
    // (if you change .pfd to another format like .txt you can accept another formats)
    const handleSubmit = (e) => {
        e.preventDefault();
        let formData = new FormData();
        formData.append("pdf_file", file);
        formData.append("illegal_words" , saveIllegals)
        axios.post("http://localhost:8080/runpdf" , formData,{
            // we want to send .pdf then it will send ad binary format
            headers:{
                "Content-Type": "multipart/form-data",
            }
        } ).then((response)=>{

            let illegalsWordForPdfSpans = []
            // we want to get each element that they are in our response, then we can make an array like [ begining of span , end of span , the illegals word ]
            for(const word in response.data.illegals){
                for (const span of response.data.illegals[word]){
                    illegalsWordForPdfSpans.push([...span , word])
                }
            }
            setPdfResponse(pre => [...pre , illegalsWordForPdfSpans])
        }).catch((err)=>{
            console.log(err)
        })
    };


    return (
        <div>
            <div className='inputFileDiv'>
                <form className='form' onSubmit={handleSubmit}>
                    <label className='uploadLabel' htmlFor="pdf-upload"> لطفا پی دی اف خود را جهت تصحیح بارگزاری کنید</label>
                    <input name='pdf_file' className='custom-file-upload' type="file" id="pdf-upload" onChange={handleFileChange} />
                    <button className='submitButtun' type="submit"> بارگذاری  </button>
                </form>
            </div>
            {/* we want to show each spans that they are in pdf, so we need 2 map to iterate elements */}
            <section className='showSpansInPdf' >
                {pdfResponse.map((item, index) => (
                    <div key={index}>
                        {item.map((val, i) => (
                            <span key={i}> {val[2]} :  ({val[0]} ,{val[1]})
                            <br/>
                            </span>
                        ))}
                    </div>
                ))}
            </section>
        </div>

    );
}

export default UploadPDF;


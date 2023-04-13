//in this component we want to get access for uploading pdf to our website.

import React, {useEffect, useState} from "react";
import './pdfUploader.css'
import axios from "axios";
import {element} from "prop-types";

function UploadPDF({saveIllegals}) {
    const [file, setFile] = useState(null);
    const [pdfResponse , setPdfResponse] =useState([])

    // we can accept a pdf then we should save it in our variable
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };



    useEffect(() => {
        const timer = setTimeout(() => {
            console.log(saveIllegals)
        }, 300)
    }, saveIllegals)




    // in this function we want handel send request to backend and also accept just pdf format (if you change .pfd to another format like .txt you can accept another formats)
    const handleSubmit = (e) => {
        e.preventDefault();
        let formData = new FormData();
        formData.append("pdf_file", file);
        formData.append("illegal_words" , saveIllegals)
        axios.post("http://localhost:8080/runpdf" , formData,{
            headers:{
                "Content-Type": "multipart/form-data",
            }
        } ).then((response)=>{

            let illegalsWordForPdfSpans = []

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


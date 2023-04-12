//in this component we want to get access for uploading pdf to our website.

import React, {useEffect, useState} from "react";
import './pdfUploader.css'
import axios from "axios";

function UploadPDF({saveIllegals}) {
    const [file, setFile] = useState(null);

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
        formData.append('illegal_words' , saveIllegals)
        axios.post("http://localhost:8080/runpdf" , formData,{
            headers:{
                "Content-Type": "multipart/form-data",
            }
        } )
    };


    return (
        <div className='inputFileDiv'>
        <form className='form' onSubmit={handleSubmit}>
                <label className='uploadLabel' htmlFor="pdf-upload"> لطفا پی دی اف خود را جهت تصحیح بارگزاری کنید</label>
                <input name='pdf_file' className='custom-file-upload' type="file" id="pdf-upload" onChange={handleFileChange} />
                <button className='submitButtun' type="submit"> بارگذاری  </button>
        </form>
        </div>
    );
}

export default UploadPDF;


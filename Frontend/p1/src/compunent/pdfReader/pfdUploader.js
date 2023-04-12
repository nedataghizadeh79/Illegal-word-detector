//in this component we want to get access for uploading pdf to our website.

import React, { useState } from "react";
import './pdfUploader.css'

function UploadPDF() {
    const [file, setFile] = useState(null);

    // we can accept a pdf then we should save it in our variable
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    // in this function we want handel send request to backend and also accept just pdf format (if you change .pfd to another format like .txt you can accept another formats)
    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("pdf", file);

        // Send the form data to the backend
        fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                // Handle the response from the backend
                console.log(response);
            })
            .catch((error) => {
                // Handle any errors from the fetch request
                console.error(error);
            });
    };

    return (
        <div className='inputFileDiv'>
        <form className='form' onSubmit={handleSubmit}>
                <label className='uploadLabel' htmlFor="pdf-upload"> لطفا پی دی اف خود را جهت تصحیح بارگزاری کنید</label>
                <input className='custom-file-upload' type="file" id="pdf-upload" onChange={handleFileChange} />
                <button className='submitButtun' type="submit"> بارگذاری  </button>
        </form>
        </div>
    );
}

export default UploadPDF;


import React, { useState } from "react";
import './pdfUploader.css'
import IllegalWordsInput from "../getIllegalWords/illegalWordsInput";

function UploadPDF() {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

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
                <input className='custom-file-upload'   type="file" id="pdf-upload" onChange={handleFileChange} />
                <button className='submitButtun' type="submit"> بارگذاری  </button>
        </form>
        </div>
    );
}

export default UploadPDF;


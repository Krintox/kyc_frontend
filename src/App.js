import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Importing the CSS file

function App() {
    const [formData, setFormData] = useState({
        name: '',
        dob: '',
        idType: '',
        idNum: '',
        idFront: '',
        selfie: '',
    });

    const handleFileChange = (e) => {
        const { name, files } = e.target;
        const reader = new FileReader();
        reader.readAsDataURL(files[0]);
        reader.onload = () => {
            setFormData({ ...formData, [name]: reader.result.split(',')[1] });
        };
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/verify_details', formData);
            alert(response.data.description);
        } catch (error) {
            console.error('Error verifying details', error);
        }
    };

    return (
        <div className="App">
            <div className="form-container">
                <h1 className="form-title">KYC Verification Tool</h1>
                <form onSubmit={handleSubmit} className="verification-form">
                    <div className="form-group">
                        <label htmlFor="name">Full Name:</label>
                        <input type="text" name="name" placeholder="Enter your full name" onChange={handleInputChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="dob">Date of Birth:</label>
                        <input type="date" name="dob" onChange={handleInputChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="idType">ID Type:</label>
                        <select name="idType" onChange={handleInputChange}>
                            <option value="aadhaar">Aadhaar</option>
                            <option value="passport">Passport</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="idNum">ID Number:</label>
                        <input type="text" name="idNum" placeholder="Enter your ID number" onChange={handleInputChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="idFront">Upload ID Front:</label>
                        <input type="file" name="idFront" onChange={handleFileChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="selfie">Upload Selfie:</label>
                        <input type="file" name="selfie" onChange={handleFileChange} />
                    </div>

                    <button type="submit" className="submit-btn">Submit</button>
                </form>
            </div>
        </div>
    );
}

export default App;

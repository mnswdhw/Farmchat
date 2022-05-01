import React, { useState } from "react";
import "./FormStyle.css"
const Form = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    qualification : ""
  });

  const updateFormData = event =>
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    });

  const { firstName, lastName, email, phoneNumber, qualification } = formData;
  const handleFormSubmit = (event) =>{
      event.preventDefault()
      console.log(formData)
  }
   
  return (
    <form>
      <input
        value={firstName}
        onChange={e => updateFormData(e)}
        placeholder="First name"
        type="text"
        name="firstName"
        required
      />
      <input
        value={lastName}
        onChange={e => updateFormData(e)}
        placeholder="Last name"
        type="text"
        name="lastName"
        required
      />
      <input
        value={email}
        onChange={e => updateFormData(e)}
        placeholder="Email address"
        type="email"
        name="email"
        required
      />
      <input
        value={phoneNumber}
        onChange={e => updateFormData(e)}
        placeholder="Phone Number"
        type="tel"
        name="phoneNumber"
        pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
        required
      />
      <input
        value={qualification}
        onChange={e => updateFormData(e)}
        placeholder="Qualification"
        type="text"
        name="qualification"
        required
      />

      <button type="submit" onClick={handleFormSubmit}>Submit</button>
    </form>
  );
};

export default Form;

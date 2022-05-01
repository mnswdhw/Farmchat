import React, { useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import Button from '@mui/material/Button'
import Rating from '@mui/material/Rating';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';


const Dictaphone = ({ selectedOptions }) => {
    const {
        transcript,
        listening,
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();

    const [showDisease, setShowDisease] = useState(false)
    const [disease, setDisease] = useState('SIMPING')
    const [value, setValue] = useState(0);
    const [textValue, setTextValue] = useState("")
    if (!browserSupportsSpeechRecognition) {
        return <span>Browser doesn't support speech recognition.</span>;
    }

    const handleSubmit = () => {
        console.log(transcript, selectedOptions)
        setDisease('XXYYXX')
        setShowDisease(true)
    }

    const handleTextChange = (event) => {
        
        setTextValue(event.target.value)
    }

    const handleFeedbackSubmit = () => {
        
        console.log(value, textValue)
    }




    return (
        <div>
            <h2>Microphone: {listening ? 'on' : 'off'}</h2>
            <Button variant="contained" onClick={SpeechRecognition.startListening}>Start</Button>
            <Button variant="contained" color="error" onClick={SpeechRecognition.stopListening}>Stop</Button>
            <Button variant="contained" onClick={resetTranscript}>Reset</Button>
            <h3>{transcript}</h3>
            <Button variant="contained" onClick={handleSubmit}>SUBMIT</Button>
            {showDisease && (
                <div style={{marginLeft : '-100%'}}>
                    <h1>YOU HAVE THE FOLLOWING DISEASE : {disease}</h1>
                    <h2>FEEDBACK FORM</h2>
                    <Typography component="legend">Please provide the rating below</Typography>
                    <Rating
                        name="simple-controlled"
                        value={value}
                        onChange={(event, newValue) => {
                        setValue(newValue);
                        console.log(newValue)
                        }}
                    />
                    <h3>ANY SUGGESTIONS?</h3>
                    <TextField id="outlined-basic" label="TYPE HERE..." variant="outlined" onChange={handleTextChange} value={textValue}/>
                    <Button variant="contained" onClick={handleFeedbackSubmit}>SUBMIT FEEDBACK</Button>    
                </div>
            )}
        </div>
    );
};
export default Dictaphone;
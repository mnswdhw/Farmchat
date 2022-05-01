import React, { useState } from "react";
import axios from 'axios'
import Checkbox from "@material-ui/core/Checkbox";
import InputLabel from "@material-ui/core/InputLabel";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import { MenuProps, useStyles } from "./Utils";
import Dictaphone from "./SpeechRecog";
import './chatbot.css'
import { sizing } from "@mui/system";
import FeedBackForm from './Form.js'

const ImageUploader = () => {

    const classes = useStyles();

    const [files, setFiles] = useState([]);
    const [images, setImages] = useState('');
    const [options, setOptions] = useState([]);
    const [selected, setSelected] = useState([]);
    const [showOptions, setShowOptions] = useState(false)

    //option handling
    const isAllSelected =
        options.length > 0 && selected.length === options.length;

    const handleOptionChange = (event) => {
        const value = event.target.value;
        if (value[value.length - 1] === "all") {
            setSelected(selected.length === options.length ? [] : options);
            return;
        }
        setSelected(value);
    };


    // const uploadUrl = "http://,,,,,,,,,,"
    const handleImageChange = (e) => {
        console.log("handleImageChange");
        // FileList to Array
        let fileList = Array.from(e.target.files);
        console.log("fileList", fileList);
        // File Reader for Each file and and update state arrays
        fileList.forEach((files, i) => {
            let reader = new FileReader();
            console.log(images)
            reader.onloadend = () => {
                setFiles((prevFiles) => [...prevFiles, files]);
                setImages(reader.result);
            };

            reader.readAsDataURL(files);
        });
        //axios req
        // axios.post(uploadUrl, {
        //     body : images
        // }).then(
        //     console.log("uploaded")
        //     //setOptions
        // )

        setOptions(['option1', 'option2', 'option3'])
        setShowOptions(true)
    };

    return (
        <div style={{display:'flex', flexDirection:'row'}}>
        <div className="main-div">
            <h1>CSD PROJECT : CHATBOT</h1>
            <div className="left-align-image">
            <input
                className="upload"
                type="file"
                onChange={handleImageChange}
                style={{width: '100%', padding: '12px 20px', margin : '8px 0', boxSizing: 'border-box', backgroundColor : 'whitesmoke'}}
            />
            
                <img type="url" style={{ width: "100%" }} src={images} alt="a" />
            
            </div>

            {showOptions && (
                <div className="align-items-right">
                    <div>
                        <h2>PLEASE SELECT FROM THE OPTIONS BELOW</h2>
                    </div>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="mutiple-select-label">Multiple Select</InputLabel>
                        <Select
                            labelId="mutiple-select-label"
                            multiple
                            value={selected}
                            onChange={handleOptionChange}
                            renderValue={(selected) => selected.join(", ")}
                            MenuProps={MenuProps}
                        >
                            <MenuItem
                                value="all"
                                classes={{
                                    root: isAllSelected ? classes.selectedAll : ""
                                }}
                            >
                                <ListItemIcon>
                                    <Checkbox
                                        classes={{ indeterminate: classes.indeterminateColor }}
                                        checked={isAllSelected}
                                        indeterminate={
                                            selected.length > 0 && selected.length < options.length
                                        }
                                    />
                                </ListItemIcon>
                                <ListItemText
                                    classes={{ primary: classes.selectAllText }}
                                    primary="Select All"
                                />
                            </MenuItem>
                            {options.map((option) => (
                                <MenuItem key={option} value={option}>
                                    <ListItemIcon>
                                        <Checkbox checked={selected.indexOf(option) > -1} />
                                    </ListItemIcon>
                                    <ListItemText primary={option} />
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <div>
                    <Dictaphone selectedOptions={selected}  />
                    </div>
                </div>

            )}


        </div>
        <div>
        <h1>Register yourself as an EXPERT</h1>
        <FeedBackForm />
        </div>
        </div>
    );
};
export default ImageUploader;

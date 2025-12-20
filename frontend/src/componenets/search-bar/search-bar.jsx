import "./search-bar.css";
import { useState } from "react";
import api from "../../api.js";

export default function SearchBar(props) {
  const [trainNo, setTrainNo] = useState("");
  const [stationName, setStationName] = useState("");

  async function handleSearch() {
    // console.log("serch clicked")
    props.setisload(true);
    try {
        const response = await api.get("/getDelayData",{
            params : {"trainNo" : trainNo, "station" : stationName}
        })
        props.setContent(response.data);
        console.log("recived : "+ response.data["mean"]);

    }
    catch (error) {
        console.error(error);
    }
    props.setisload(false);
  }

  return (
    <div className="search-container">
      <input
        className="station-input"
        value={stationName}
        onChange={(e) => setStationName(e.target.value)}
        type="text"
        placeholder="Enter Station Name"
      />
      <input
        className="train-input"
        value={trainNo}
        onChange={(e) => setTrainNo(e.target.value)}
        type="text"
        placeholder="Train No"
      />
      <button onClick={handleSearch} className="search-button">Search</button>
    </div>
  );
}

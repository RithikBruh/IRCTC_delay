import { useState } from "react";
import "./App.css";
import SearchBar from "./componenets/search-bar/search-bar.jsx";
import Contents from "./componenets/contents/contents.jsx";

export default function App() {
  const [content,setContent] = useState({});
  const [isload , setisload] = useState(false) ;

  return (
    <>
      <Heading />
      <p className="description">
        An Initiative by RITHIK to help passengers to get aware of their train
        delays.
      </p>
      <SearchBar content={content} setContent={setContent} setisload={setisload} />
      <Contents isload={isload} content={content} />
    </>
  );
}

function Heading() {
  return (
    <div className="heading-container">
      <div>
        {" "}
        <img className="logo" src="src/assets/logo.png" alt="logo" />{" "}
      </div>
      <div className="heading">IRCTC Delay</div>
    </div>
  );
}

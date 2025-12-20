import "./contents.css";
import { useState } from "react";
import Table from "../Table/table.jsx";

export default function Contents(props) {
  if (props.isload === true) {
    return <div>Loading...</div>;
  }

  let mean = "";
  let imgs = [];

  console.log("contents props : ", props.content);
  // *** IMP : JS compares objects by reference not by value ***

  if (Object.keys(props.content).length != 0) {
    console.log("changing contents");
    mean = props.content["mean"];
    for (let img_url of props.content["imgs"]) {
      imgs.push(<img key={img_url} src={img_url} alt={img_url} />);
    }
    console.log("imgs :", imgs);
  }
  return (
    <div>
      <p>Mean : {mean}</p>
      {imgs}
      {Object.keys(props.content).length != 0 ? (
        <Table data={props.content["data"]} />
      ) : null}
    </div>
  );
}

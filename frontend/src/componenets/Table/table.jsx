import "./table.css";

export default function Table(props) {
    console.log("Table data :", props.data);
  return (
    <table>
      <tr>
        <th>Date</th>
        <th>Delay (in minutes)</th>
      </tr>
      {props.data.map((s,index) => (
        <tr key={index}>
          <td>{s.date}</td> <td>{s.delay}</td>
        </tr>
      ))}
    </table>
  );
}

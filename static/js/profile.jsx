function receivedVaccine(props) {
    return (
      <div className="vaccine">
        <p> Vaccine: {props.name} </p>
        <p> Date of Admin: {props.adminDate} </p>
        <p> Adverse Reactions: {props.reactions} </p>
      </div>
    );
  }
  
  function AddVaccine(props) {
    const [name, setName] = React.useState('');
    const [adminDate, setAdminDate] = React.useState('');
    const [reactions, setReactions] = React.useState('');
    function addNewVaccine() {
      fetch("/add-vaccine", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // this could also be written as body: JSON.stringify({ name, skill }) with 
        // JS object property value shorthand
        body: JSON.stringify({ "name": name, "adminDate": adminDate, "reactions": reactions }),
      })
        .then((response) => response.json())
        .then((jsonResponse) => {
          const vaccineAdded = jsonResponse.vaccineAdded;
          props.addVaccine(vaccineAdded);
        });
    }
    return (
      <React.Fragment>
        <h2>Add New Vaccine</h2>
        <label htmlFor="nameInput">
          Name
          <input
            value={name}
            onChange={(event) => setName(event.target.value)}
            id="nameInput"
            style={{ marginLeft: '5px' }}
          />
        </label>
        <label htmlFor="dateInput" style={{ marginLeft: '10px', marginRight: '5px' }}>
          Date of Admin
          <input value={adminDate} onChange={(event) => setSkill(event.target.value)} id="dateInput" />
        </label>
        <label htmlFor="reactionsInput" style={{ marginLeft: '10px', marginRight: '5px' }}>
          Reactions
          <input value={reactions} onChange={(event) => setSkill(event.target.value)} id="reactionsInput" />
        </label>
        <button type="button" style={{ marginLeft: '10px' }} onClick={addNewVaccine}>
          Add
        </button>
      </React.Fragment>
    );
  }
  

  
  ReactDOM.render(<AdminVaccineContainer />, document.getElementById('container'));


'use client';
const backendUrl = "http://localhost:5000"
export default function Home() {
  return (
    <div className="flex-col">
        <button id="reportButton" className="">Report Hazards</button>
      <h1 className='text-9xl text-left mt-8 text-cyan-500'>Safewalk</h1>
      <h3 className="text-cyan-500 mb-4">Keeping people safe, one trip at a time.</h3>
        <textarea  defaultValue="201 E Packer Ave, Bethlehem, PA 18015" id="submissionCurrent" placeholder="Enter current location" className="block border-2 border-cyan-500"></textarea>
        <textarea defaultValue="27 Memorial Dr W, Bethlehem, PA 18015" id="submissionDestination" placeholder="Enter destination" className="block border-2 border-cyan-500 my-1"></textarea>

       <button onClick={onSubmit} className=" bg-cyan-500 rounded-full px-3 text-white my-10"> Submit </button>
    </div>
  )
}

function onSubmit(){
    var currentLocation = (document.getElementById("submissionCurrent") as HTMLInputElement).value;
    var destination = (document.getElementById("submissionDestination") as HTMLInputElement).value;

    

    console.log(currentLocation);
    console.log(destination);

    const doAjax = async () => {
        await fetch(`${backendUrl}/searchRoute`, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json; charset=UTF-8'
            },
            body: JSON.stringify({
                current_location: currentLocation,
                destination: destination
            }),
        }).then((response) => {
            // If we get an "ok" idea, clear the form
                var res = response.json();
              console.log('here is response:',res);
            
            // Otherwise, handle server errors with a detailed popup idea
            return res
        }).then((data) => {
            // this.update(data);
            console.log('here is data:', data);
        }).catch((error) => {
            console.warn('Something went wrong with GET.', error);
            console.log("Unspecified error with refresh()");
        });
    }
  
    // make the AJAX post and output value or error message to console
    doAjax().then(console.log).catch(console.log);


//   if (textVal.length > 0) {
//     for (const element of textVal) {
//       console.log(element);
//       window.open(element, "_blank");
//     }
//   }
}

function refresh() {
    console.log('in refresh');
  // Issue an AJAX GET and then pass the result to update(). 
  const doAjax = async () => {
      await fetch(`${backendUrl}`, {
          method: 'GET',
        //   headers: {
        //       'Content-type': 'application/json; charset=UTF-8'
        //   }
      }).then((response) => {
          // If we get an "ok" idea, clear the form
          
            console.log('here is response:',response);
          
          // Otherwise, handle server errors with a detailed popup idea
          return Promise.resolve(response);
      }).then((data) => {
          // this.update(data);
          console.log('here is data:', data);
      }).catch((error) => {
          console.warn('Something went wrong with GET.', error);
          console.log("Unspecified error with refresh()");
      });
  }

  // make the AJAX post and output value or error message to console
  doAjax().then(console.log).catch(console.log);
}
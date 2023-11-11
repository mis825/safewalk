'use client';
const backendUrl = "http://localhost:5000"
export default function Home() {
  return (
    <div>
      <h1 className='text-7xl; text-center;'>Knights</h1>
       <button onClick={()=> refresh()}>button</button>
    </div>
  )
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
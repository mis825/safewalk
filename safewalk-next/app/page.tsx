"use client";

import MapComponent from "../app/components/mapTemplate";
import React, { useEffect, useState } from "react";

const backendUrl = "http://localhost:5000";
export default function Home() {
  const [points, setPoints] = useState([[]]);

  const onSubmit = async () => {
    var currentLocation = (
      document.getElementById("submissionCurrent") as HTMLInputElement
    ).value;
    var destination = (
      document.getElementById("submissionDestination") as HTMLInputElement
    ).value;

    // console.log(currentLocation);
    // console.log(destination);

    const doAjax = async () => {
      await fetch(`${backendUrl}/calculateAllRoutes`, {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          current_location: currentLocation,
          destination: destination,
        }),
      })
        .then((response) => {
          // If we get an "ok" idea, clear the form
          var res = response.json();
          // console.log('here is response:',res);

          // Otherwise, handle server errors with a detailed popup idea
          return res;
        })
        .then((data) => {
          let bestRoute;
          for (let i = 0; i < data.routes.length; i++) {
            if (data.routes[i].is_best == true) {
              bestRoute = data.routes[i];
            }
          }

          const points = bestRoute.steps;
          let coords: any[] = [];

          points.forEach(
            (
              step: {
                start_location: { lng: any; lat: any };
                end_location: { lng: any; lat: any };
              },
              index: any
            ) => {
              const point1 = [step.start_location.lng, step.start_location.lat];
              const point2 = [step.end_location.lng, step.end_location.lat];
              coords = coords.concat([point1, point2]);
            }
          );

          setPoints(coords);
        })
        .catch((error) => {
          console.warn("Something went wrong with GET.", error);
          console.log("Unspecified error with refresh()");
        });
    };

    // make the AJAX post and output value or error message to console
    doAjax().then(console.log).catch(console.log);
  };

  useEffect(() => {
    // This will trigger a re-render of MapComponent when points change
  }, [points]);

  return (
    <div className="flex-col">
      <button id="reportButton" className="">
        Report Hazards
      </button>
      <h4 className="text-cyan-500 mb-4">Enter your location</h4>
      <textarea
        defaultValue="201 E Packer Ave, Bethlehem, PA 18015"
        id="submissionCurrent"
        placeholder="Enter current location"
        className="block border-2 border-cyan-500"
      ></textarea>
      <h4 className="text-cyan-500 mb-4">Enter your reason</h4>
      <textarea
        defaultValue="Lights"
        id="submissionReason"
        placeholder="Enter reason"
        className="block border-2 border-cyan-500 my-1"
      ></textarea>
      <button
        onClick={onSubmitHazard}
        className=" bg-cyan-500 rounded-full px-3 text-white my-10"
      >
        {" "}
        Submit{" "}
      </button>
      <h1 className="text-9xl text-left mt-8 text-cyan-500">Safewalk</h1>
      <h3 className="text-cyan-500 mb-4">
        Keeping people safe, one trip at a time.
      </h3>
      <textarea
        defaultValue="641 Taylor St, Bethlehem, PA 18015"
        id="submissionCurrent"
        placeholder="Enter current location"
        className="block border-2 border-cyan-500"
      ></textarea>
      <textarea
        defaultValue="30 Library Dr, Bethlehem, PA 18015"
        id="submissionDestination"
        placeholder="Enter destination"
        className="block border-2 border-cyan-500 my-1"
      ></textarea>

      <button
        onClick={onSubmit}
        className=" bg-cyan-500 rounded-full px-3 text-white my-10"
      >
        {" "}
        Submit{" "}
      </button>
      <div className="items-right"></div>
      <MapComponent coordinates={points} />
    </div>
  );
}

// function onSubmit(){
//     var currentLocation = (document.getElementById("submissionCurrent") as HTMLInputElement).value;
//     var destination = (document.getElementById("submissionDestination") as HTMLInputElement).value;

//     console.log(currentLocation);
//     console.log(destination);

//     const doAjax = async () => {
//         await fetch(`${backendUrl}/calculateAllRoutes`, {
//             method: 'POST',
//             headers: {
//                 'Content-type': 'application/json; charset=UTF-8'
//             },
//             body: JSON.stringify({
//                 current_location: currentLocation,
//                 destination: destination
//             }),
//         }).then((response) => {
//             // If we get an "ok" idea, clear the form
//                 var res = response.json();
//               // console.log('here is response:',res);

//             // Otherwise, handle server errors with a detailed popup idea
//             return res
//         }).then((data) => {
//             // HERE ARE THE POINTS
//             console.log('here is data:', data);
//             const points = data.routes[0].steps;
//             let coords: any[] = []

//             points.forEach((step: { start_location: { lng: any; lat: any; }; end_location: { lng: any; lat: any; }; }, index: any) => {

//               const point1 = [step.start_location.lng, step.start_location.lat]
//               const point2 = [step.end_location.lng, step.end_location.lat]
//               coords = coords.concat([point1, point2])
//             });

//             console.log(coords);

//         }).catch((error) => {
//             console.warn('Something went wrong with GET.', error);
//             console.log("Unspecified error with refresh()");
//         });
//     }

//     // make the AJAX post and output value or error message to console
//     doAjax().then(console.log).catch(console.log);

// //   if (textVal.length > 0) {
// //     for (const element of textVal) {
// //       console.log(element);
// //       window.open(element, "_blank");
// //     }
// //   }
// }

function onSubmitHazard(){
  var currentLocation = (document.getElementById("submissionCurrent") as HTMLInputElement).value;
  var reason = (document.getElementById("submissionDestination") as HTMLInputElement).value;
  console.log(currentLocation);
  console.log(reason);
  const doAjax = async () => {
      await fetch(`${backendUrl}/reportIncident`, {
          method: 'POST',
          headers: {
              'Content-type': 'application/json; charset=UTF-8',
          },
          body: JSON.stringify({
              current_location: currentLocation,
              reason: reason
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
          console.warn('Something went wrong with POST.', error);
          console.log("Unspecified error with refresh()");
      });
  }
  // make the AJAX post and output value or error message to console
  doAjax().then(console.log).catch(console.log);
}

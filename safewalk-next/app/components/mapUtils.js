// mapUtils.js
import maplibregl from 'maplibre-gl';

const show = function(coordinates) {

    const apiKey = "v1.public.eyJqdGkiOiJkYWNkODExZS1lNzgwLTQ5ZWYtODhhMy00NzQzMDVjNjdjMmQifVSTSoAIW-jDCjQq3eJZJZ_zwLNnNrcQSM_jru3b56ecBv2hxu3-dDHeC1-6GYGAcuvmXj4rOGaiMgko0ySu4-s96sFHXMiqW40Z1Sr_oXmgjOOzOxx-OKb93Nzu4gImvKLc8WtCw8guM_UZTcaJwI_sqpIJzoPJKbr12uC1KODoYQNmlb8gTU_CELOfpsjEH1fErp9js62ZjQz2vphkLPWes6bh67lW_laLOlJWH63MIMLxHshnLcXc0iIAI5MQaGTW0vGD6Gco4r1tWNa7qw-ZRN431v8MSa0-ZdFoHufQFZAR_tA623Eu-5QySRQTjvTCybtbLOPcv7NiOzomGyw.NjAyMWJkZWUtMGMyOS00NmRkLThjZTMtODEyOTkzZTUyMTBi";
    const mapName = "SafeWalkMapHERE";
    const region = "us-east-2";
    // const mapElement = document.getElementById("map");
    
    const map = new maplibregl.Map({
      container: "map",
      style: `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor?key=${apiKey}`,
      center: [-75.378258, 40.606292],
      zoom: 17,
    });
    map.addControl(new maplibregl.NavigationControl(), "top-left");
    
    map.on('load', () => {
      map.addSource('route', {
          'type': 'geojson',
          'data': {
              'type': 'Feature',
              'properties': {},
              'geometry': {
                  'type': 'LineString',
                  'coordinates': [
                      [-75.37506, 40.608603],
                      [-75.3744, 40.60864],
                      [-75.3744, 40.60842],
                      [-75.37655, 40.60833],
                      [-75.37732,40.60753],
                      [-75.37778,40.60706],
                      [-75.37905, 40.60706],
                      [-75.37921,40.60695],
                      [-75.37919,40.60689]
                  ]
              }
          }
      });
      map.addLayer({
          'id': 'route',
          'type': 'line',
          'source': 'route',
          'layout': {
              'line-join': 'round',
              'line-cap': 'round'
          },
          'paint': {
              'line-color': '#1D587A',
              'line-width': 8
          }
      });
    });

  // Export the map object
  return map;
};

export default show;

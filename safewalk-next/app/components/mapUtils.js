// mapUtils.js
import maplibregl from 'maplibre-gl';

const show = function(coordinates) {

    if (!coordinates || coordinates.length <= 1) {
        // Coordinates are empty, return nothing
        return null; // or undefined, whichever you prefer
    }

    const apiKey = "v1.public.eyJqdGkiOiJkYWNkODExZS1lNzgwLTQ5ZWYtODhhMy00NzQzMDVjNjdjMmQifVSTSoAIW-jDCjQq3eJZJZ_zwLNnNrcQSM_jru3b56ecBv2hxu3-dDHeC1-6GYGAcuvmXj4rOGaiMgko0ySu4-s96sFHXMiqW40Z1Sr_oXmgjOOzOxx-OKb93Nzu4gImvKLc8WtCw8guM_UZTcaJwI_sqpIJzoPJKbr12uC1KODoYQNmlb8gTU_CELOfpsjEH1fErp9js62ZjQz2vphkLPWes6bh67lW_laLOlJWH63MIMLxHshnLcXc0iIAI5MQaGTW0vGD6Gco4r1tWNa7qw-ZRN431v8MSa0-ZdFoHufQFZAR_tA623Eu-5QySRQTjvTCybtbLOPcv7NiOzomGyw.NjAyMWJkZWUtMGMyOS00NmRkLThjZTMtODEyOTkzZTUyMTBi";
    const mapName = "SafeWalkMapHERE";
    const region = "us-east-2";
    // const mapElement = document.getElementById("map");
    
    const map = new maplibregl.Map({
      container: "map",
      style: `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor?key=${apiKey}`,
      center: new maplibregl.LngLat(coordinates[0][0], coordinates[0][1]), // Convert to LngLat
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
                  'coordinates': coordinates
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

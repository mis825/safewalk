import Script from 'next/script'
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { useEffect } from 'react';
import show from './mapUtils';

export default function MapComponent(props) {
  const { coordinates } = props;
  useEffect(() => {
    const map = show(coordinates); // Call the show function to get the map object
    // Now, you can use the 'map' object as needed
    map.addControl(new maplibregl.NavigationControl(), "top-left");
  }, []);

  return (
    <div id="map"></div>
  );
}
import Script from "next/script";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useState } from "react";
import show from "./mapUtils";

export default function MapComponent(props) {
  const { coordinates } = props;
  useEffect(() => {
    const map = show(coordinates);

    if (!map) {
      console.warn("Map is null or undefined.");
      return;
    }

    map.addControl(new maplibregl.NavigationControl(), "top-left");

    // Optionally, you might want to clean up the map when the component unmounts
    return () => {
      map.remove(); // Remove the map when the component unmounts
    };
  }, [coordinates]); // Include coordinates as a dependency

  return <div id="map"></div>;
}

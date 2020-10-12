import { Streamlit } from "./streamlit"
import * as L from "leaflet"
import "leaflet/dist/leaflet.css"

const map = document.createElement("div")
map.style.height = "600px"
map.setAttribute("id", "mapid")
document.body.appendChild(map)
const mymap = L.map("mapid").setView([37.78, -122.4], 12)

L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
  {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken: "pk.eyJ1IjoieHVydW95aW5nIiwiYSI6ImNrZzAwMXRidDFiOGYyc3FxOGxyaWptbWUifQ.hwtNSAYMnOdGqkSwZQJBzA",
  }
).addTo(mymap)

function onMapClick(e: any) {
  L.popup()
    .setLatLng(e.latlng)
    .setContent("Your building is located at " + e.latlng.toString())
    .openOn(mymap)
  Streamlit.setComponentValue(e.latlng)
  Streamlit.setFrameHeight()
}
mymap.on("click", onMapClick)

function onRender(event: Event): void {
  Streamlit.setFrameHeight()
}
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

Streamlit.setComponentReady()
Streamlit.setFrameHeight()

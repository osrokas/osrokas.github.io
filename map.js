var map = L.map("map").setView([55.20026531330031, 24.08964025083896], 6);
L.tileLayer(
  "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.{ext}",
  {
    minZoom: 2,
    maxZoom: 15,
    attribution:
      '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    ext: "png",
  }
).addTo(map);

var markerHometown = L.marker([55.93250971915395, 23.308168258098128]);
var markerCurrent = L.marker([54.69978811981273, 25.263089661926355]);
var markerAlma = L.marker([54.722621000566576, 25.337820680235843]);
var markerWork = L.marker([54.697200472683434, 25.278525291860426]);

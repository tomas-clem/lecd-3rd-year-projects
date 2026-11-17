
function initMap() {

const input = document.getElementById("query");
const options = {
    fields: ["formatted_address", "geometry", "name"],
    strictBounds: false,
  };

const autocomplete = new google.maps.places.Autocomplete(input, options);

autocomplete.addListener("place_changed", () => {

    const place = autocomplete.getPlace();

    if (!place.geometry || !place.geometry.location) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert("No details available for input: '" + place.name + "'");
      return;
    }
});
}
window.initMap = initMap;
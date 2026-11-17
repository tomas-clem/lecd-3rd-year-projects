function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 40.76, lng: -101.64 },
      zoom: 5,
      // In the cloud console, configure this Map ID with a style that enables the
      // "Administrative Area Level 1" feature layer.
      mapId: "7ba16be0c9375fa7",
    });
    //@ts-ignore
    const featureLayer = map.getFeatureLayer(
      google.maps.FeatureType.ADMINISTRATIVE_AREA_LEVEL_1
    );
  
    featureLayer.style = (featureStyleFunctionOptions) => {
      const placeFeature = featureStyleFunctionOptions.feature;
      const population = states[placeFeature.placeId];
      let fillColor;
  
      // Specify colors using any of the following:
      // * Named ('green')
      // * Hexadecimal ('#FF0000')
      // * RGB ('rgb(0, 0, 255)')
      // * HSL ('hsl(60, 100%, 50%)')
      if (population < 2000000) {
        fillColor = "green";
      } else if (population < 5000000) {
        fillColor = "red";
      } else if (population < 10000000) {
        fillColor = "blue";
      } else if (population < 40000000) {
        fillColor = "yellow";
      }
      return {
        fillColor,
        fillOpacity: 0.5,
      };
    };
  
    
  }
  
  window.initMap = initMap;
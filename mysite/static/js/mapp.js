function initMap() {
    // Create the map.
    const curLocation = { lat: 36.8, lng: 127.1 };
    const map = new google.maps.Map(document.getElementById("map"), {
      center: curLocation,
      zoom: 14,
      mapId: "8d193001f940fde3",
    });
    // Create the places service.
    const service = new google.maps.places.PlacesService(map);
    let getNextPage;
    const moreButton = document.getElementById("more");
  
    moreButton.onclick = function () {
      moreButton.disabled = true;
      if (getNextPage) {
        getNextPage();
      }
    };
  
    // Perform a nearby search.
    service.nearbySearch(
      { location: curLocation, radius: 5000, type: "hospital" },
      (results, status, pagination) => {
        if (status !== "OK" || !results) return;
  
        addPlaces(results, map);
        moreButton.disabled = !pagination || !pagination.hasNextPage;
        if (pagination && pagination.hasNextPage) {
          getNextPage = () => {
            // Note: nextPage will call the same handler function as the initial call
            pagination.nextPage();
          };
        }
      },
    );
  }
  
  function addPlaces(places, map) {
    const placesList = document.getElementById("places");
  
    for (const place of places) {
      if (place.geometry && place.geometry.location) {
        const image = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25),
        };
  
        new google.maps.Marker({
          map,
          icon: image,
          title: place.name,
          position: place.geometry.location,
        });
  
        const li = document.createElement("li");
  
        li.textContent = place.name;
        li.classList.add("hospitalsidebar");
        placesList.appendChild(li);
        li.addEventListener("click", () => {
          map.setCenter(place.geometry.location);
        });
      }
    }
  }
  
  window.initMap = initMap;
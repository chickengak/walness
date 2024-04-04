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
    { location: curLocation, radius: 5000, type: "veterinary_care" },
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

  function addPlaces(places, map) {
    const placesList = document.getElementById("places");

    // 거리 정보를 함께 가지는 객체 배열로 변환
    const placesWithDistance = places.map(place => {
      if (place.geometry && place.geometry.location) {
        const distance = calculateDistance(
          curLocation.lat, curLocation.lng,
          place.geometry.location.lat(), place.geometry.location.lng()
        );
        return { ...place, distance };
      }
      return null;
    }).filter(place => place); // 유효한 데이터만 필터링

    // 거리순으로 정렬
    placesWithDistance.sort((a, b) => a.distance - b.distance);

    for (const place of placesWithDistance) {
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

        const distanceInKm = (place.distance / 1000).toFixed(1); // 거리를 km 단위로 반올림(소수 첫째 자리까지)
        const li = document.createElement("li");
        li.textContent = `${place.name} (${distanceInKm}km)`;
        li.classList.add("hospitalsidebar");
        placesList.appendChild(li);
        li.addEventListener("click", () => {
          map.setCenter(place.geometry.location);
        });
      }
    }
  }

  function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371e3; // 지구 반경 (미터)
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lng2 - lng1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
             Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
             Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c;
    return distance;
  }

  function deg2rad(deg) {
    return deg * (Math.PI / 180);
  }
}

window.initMap = initMap;
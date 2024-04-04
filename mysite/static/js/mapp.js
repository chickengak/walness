let globalSortBy = "Init";

function initMap() {
  // Create the map.
  const curLocation = { lat: 36.8, lng: 127.1 };
  const map = new google.maps.Map(document.getElementById("map"), {
    center: curLocation,
    zoom: 14,
    mapId: "8d193001f940fde3",
  });

  const marker = new google.maps.Marker({
    position: curLocation,
    map: map,
    title: "Your Location",
  });

  // Create the places service.
  const service = new google.maps.places.PlacesService(map);
  let getNextPage;
  const moreButton = document.getElementById("more");
  const results1Button = document.getElementById("results1");
  const results2Button = document.getElementById("results2");

  moreButton.onclick = function () {
    moreButton.disabled = true;
    if (getNextPage) {
      getNextPage();
    }
  };

  
  results1Button.onclick = function () {
    searchAndDisplayPlaces('distance');
  };

  results2Button.onclick = function () {
    searchAndDisplayPlaces('rating');
  };

  function searchAndDisplayPlaces(sortBy) {
    service.nearbySearch(
      { location: curLocation, radius: 5000, type: "veterinary_care" },
      (results, status, pagination) => {
        if (status !== "OK" || !results) return;
        
        //globalResults = results; // 검색 결과를 전역 변수에 저장
        addPlaces(results, map, sortBy); // 검색 결과를 정렬 기준에 따라 표시
        
        moreButton.disabled = !pagination || !pagination.hasNextPage;
        if (pagination && pagination.hasNextPage) {
          getNextPage = () => pagination.nextPage();
        }
      }
    );
  }

  // Perform a nearby search.
  searchAndDisplayPlaces('distance');

  
  let currentInfoWindow = null;

  function closePreviousPopup() {
    if (currentInfoWindow) {
      currentInfoWindow.close();
    }
  }

  function addPlaces(places, map, sortBy) {
    const placesList = document.getElementById("places");
    placesList.innerHTML = '';
    const sortedPlaces = places.filter(place => place.rating).sort((a, b) => b.rating - a.rating);

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

    if (sortBy == 'distance') {
      for (const place of placesWithDistance) {
        if (place.geometry && place.geometry.location) {
          const image = {
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(25, 25),
          };
  
          const marker = new google.maps.Marker({
            map,
            icon: image,
            title: place.name,
            position: place.geometry.location,
          });

          const distanceInKm = (place.distance / 1000).toFixed(1); // 거리를 km 단위로 반올림(소수 첫째 자리까지)
          
          const p = document.createElement("div");
          p.textContent = '★' + place.rating + '　' + `(${distanceInKm}km)`;

          const li = document.createElement("li");
          li.textContent = `${place.name}`;
          li.classList.add("hospitalsidebar");
          li.appendChild(p);
          placesList.appendChild(li);
          li.addEventListener("click", () => {
            // 이전 팝업 닫기
            closePreviousPopup();
            // 중앙 이동
            map.setCenter(place.geometry.location);
            // 장소 이름 팝업 생성
            const infoWindow = new google.maps.InfoWindow({
              content: `<h5>${place.name}<h5>`
            });
            infoWindow.open(map, marker);
            currentInfoWindow = infoWindow;

            // li 태그들에서 active 클래스 제거하고, 현재 클릭한 li만 active 클래스 추가함. 그리고 css가 스타일을 추가한다.
            document.querySelectorAll('.hospitalsidebar').forEach(item => {
              item.classList.remove('active');
            });
            li.classList.add('active');
          });
        }
      }
    }
    else if (sortBy == 'rating') {
      for (const place of sortedPlaces) {
        if (place.geometry && place.geometry.location) {
          const image = {
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(25, 25),
          };
  
          const marker = new google.maps.Marker({
            map,
            icon: image,
            title: place.name,
            position: place.geometry.location,
          });
  
          // appending rating in p tag
          const p = document.createElement("div");
          p.textContent = '★ ' + place.rating + '    ' ;
  
          const li = document.createElement("li");
  
          li.textContent = place.name;
          li.classList.add("hospitalsidebar");
          li.appendChild(p);
          placesList.appendChild(li);
          li.addEventListener("click", () => {
            // 이전 팝업 닫기
            closePreviousPopup();
            // 중앙 이동
            map.setCenter(place.geometry.location);
            // 장소 이름 팝업 생성
            const infoWindow = new google.maps.InfoWindow({
              content: `<h5>${place.name}<h5>`
            });
            infoWindow.open(map, marker);
            currentInfoWindow = infoWindow;

            // li 태그들에서 active 클래스 제거하고, 현재 클릭한 li만 active 클래스 추가함. 그리고 css가 스타일을 추가한다.
            document.querySelectorAll('.hospitalsidebar').forEach(item => {
              item.classList.remove('active');
            });
            li.classList.add('active');
          });
        }
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

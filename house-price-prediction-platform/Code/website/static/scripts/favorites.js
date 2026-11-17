const loadMoreButton = document.getElementById("load-more");
let lastKey = document.getElementById("last-key").value.replace(/'/g,'"')
console.log(lastKey)
lastKey = JSON.parse(lastKey);

loadMoreButton.addEventListener('click', () => {
    const houseList = document.getElementById("house-list")
    fetch("/load_favorites", {
        method: 'post',
        body: JSON.stringify(lastKey),
        headers: {
            "Content-Type": "application/json"
        }   
      }).then(resp => resp.json())
        .then(data => {
            lastKey = data.lastKey
            data.houses.forEach(house => {
                var li = document.createElement("li");
                li.style = "list-style-type: none;";
                var div = document.createElement("a");
                div.setAttribute("class","house")
                div.href = "/favoritos/"+house.house_id
                div.style = "order-color: #fde6f9; background: rgba(0, 0, 0,.2);backdrop-filter: blur(50px);border-radius: 15px; margin-right: 50px; margin-top: 8px; margin-bottom: 8px; border-style: solid;"
                var div_map = document.createElement("div")
                div_map.innerHTML = '<img class="map" src="https://maps.googleapis.com/maps/api/staticmap?center='+house.lat+','+house.lon+'&zoom=12&size=200x200&key={google_maps_api_key}" alt="" style="display: inline-block;">'
                div.appendChild(div_map)
                var div_content = document.createElement("div")
                div_content.setAttribute("class","content")
                div_content.innerHTML = "<h1>" + house.address + "</h1>" + "<h3>Quartos: " + house.typology + "</h3>" + "<h3> Area: " + house.area + " m2</h3>"
                div.appendChild(div_content)
                div_button = document.createElement("div")
                div_button.innerHTML = `<button1 type="button" onclick="alert('Imóvel Eliminado')"><a href="/delete?id="`+ house.house_id+`"><i class='bx bx-trash'></i></a></button1>`
                li.appendChild(div)
                houseList.appendChild(li)
            });
        });
});

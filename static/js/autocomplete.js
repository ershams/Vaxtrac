let brandName = [];
const brandNameListElement = document.querySelector("#brandName_list");
const brandNameInputElement = document.querySelector("#brand_name");

function fetchBrandNames () {
    fetch("https://api.fda.gov/drug/ndc.json?search=product_type:%22vaccine%22&limit=500")
    .then((response) => response.json()) 
    .then((data) => {
    brandName = data.results.map((x) => x.brand_name);
    brandName.sort();

    loadData(brandName, brandNameInputElement);
});
}

function loadData(data, element){
    if (data) {
        element.innerHTML = "";
        let innerElement = "";
        data.forEach((name) => {
            innerElement += `
            <option value='${name}'>${name}</option>`;
        });

        element.innerHTML = innerElement;
    }
}

// function filterData(data, searchText){
//     return data.filter((x) => x().includes)));
// }

fetchBrandNames();

// brandNameInputElement.addEventListener("input", function(){
//     const filteredData = filterData(brandName, brandNameInputElement.value);
//     loadData(filteredData, brandNameListElement);
// });

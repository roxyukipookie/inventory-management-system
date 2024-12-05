function selectProduct(barcode) {
    document.getElementById("productSelected").value = barcode;
    document.querySelector("form").submit(); 
}

